import redis
import json
import time
import threading
import os
import uuid
from influxdb_client import InfluxDBClient, Point
from influxdb_client.client.write_api import SYNCHRONOUS

STREAM_KEY = 'rala:sensors:stream_v2'
PUBSUB_CHANNEL = 'rala:sensors:ui_v2'
REGISTRY_KEY = 'rala:sensors:registry'

# Connect to Redis to listen to the fire-hose of raw data
REDIS_HOST = os.getenv("REDIS_HOST", "localhost")
redis_client = redis.Redis(host=REDIS_HOST, port=6379, decode_responses=True)

# Cooldown: 3600 for production (1 alert per sensor-attribute per hour)
last_alert_time = {}
ALERT_COOLDOWN = 3600  # seconds

# Influx configuration for Persisting Alerts (Phase 18)
INFLUX_URL = os.getenv("INFLUX_URL", "http://localhost:8086")
influx_client = InfluxDBClient(url=INFLUX_URL, token="raala-super-secret-token", org="raala")
write_api = influx_client.write_api(write_options=SYNCHRONOUS)

# default fallback boundaries
DEFAULT_THRESHOLDS = {
    'temperature': {'min': 19, 'max': 22},
    'humidity': {'min': 40, 'max': 60},
    'pressure': {'min': 1000, 'max': 1020},
    'vpd': {'min': 0.8, 'max': 1.2},
    'ambient_light': {'min': 2000, 'max': 4000},
    'color_temp': {'min': 4000, 'max': 6000},
    'ppfd': {'min': 400, 'max': 800},
    'eco2': {'min': 400, 'max': 800},
    'tvoc': {'min': 0, 'max': 100},
    'moisture': {'min': 30, 'max': 60},
    'soil_temp': {'min': 15, 'max': 22}
}

# ─────────────────────────────────────────────────────────────
# Phase 15: Heartbeat Watcher
# Runs in a background thread every 5 seconds.
# Checks rala:heartbeat:{sensor_id} TTL keys set by mock_sensors.py.
# A missing key means the sensor has been silent for >12 seconds.
# Publishes { type: "offline" } or { type: "online" } on state transitions.
# ─────────────────────────────────────────────────────────────
offline_sensors = set()   # tracks currently-offline sensor IDs

def heartbeat_watcher():
    watcher_client = redis.Redis(host=REDIS_HOST, port=6379, decode_responses=True)
    print("Phase 15: Heartbeat watcher started (polling every 5s)...")
    while True:
        try:
            # Get all registered sensor IDs from the Phase 14 registry
            sensor_ids = list(watcher_client.hkeys(REGISTRY_KEY))

            for sensor_id in sensor_ids:
                key_exists = watcher_client.exists(f"rala:heartbeat:{sensor_id}")

                if not key_exists and sensor_id not in offline_sensors:
                    # Transition: Live → Offline
                    offline_sensors.add(sensor_id)
                    event = {
                        "type": "offline",
                        "sensor_id": sensor_id,
                        "timestamp": time.strftime('%Y-%m-%dT%H:%M:%SZ', time.gmtime())
                    }
                    watcher_client.publish(PUBSUB_CHANNEL, json.dumps(event))
                    print(f"[HEARTBEAT] OFFLINE detected: {sensor_id}")

                elif key_exists and sensor_id in offline_sensors:
                    # Transition: Offline → Live
                    offline_sensors.discard(sensor_id)
                    event = {
                        "type": "online",
                        "sensor_id": sensor_id,
                        "timestamp": time.strftime('%Y-%m-%dT%H:%M:%SZ', time.gmtime())
                    }
                    watcher_client.publish(PUBSUB_CHANNEL, json.dumps(event))
                    print(f"[HEARTBEAT] ONLINE restored: {sensor_id}")

        except redis.ConnectionError:
            print("[HEARTBEAT] Redis unavailable, retrying...")
        except Exception as e:
            print(f"[HEARTBEAT] Watcher error: {e}")

        time.sleep(5)  # poll every 5 seconds

# Start watcher in a daemon thread (exits automatically when main process exits)
watcher_thread = threading.Thread(target=heartbeat_watcher, daemon=True)
watcher_thread.start()

print("RAALA Automation Rule Engine Started. Tuning into data streams...")
last_id = '$'

while True:
    try:
        messages = redis_client.xread({STREAM_KEY: last_id}, count=100, block=2000)
        
        if not messages:
            continue
            
        for _, message_list in messages:
            for message_id, message_data in message_list:
                last_id = message_id
                
                payload_str = message_data.get('data')
                if not payload_str:
                    continue
                    
                try:
                    payload = json.loads(payload_str)
                    
                    # Skip Phase 14 HELLO registration packets—not sensor readings
                    if payload.get('type') == 'HELLO':
                        continue
                    
                    sensor_id = payload.get("sensor_id")
                    
                    # Phase 17: Load active thresholds dynamically from Redis
                    raw_t = redis_client.get(f"rala:thresholds:{sensor_id}")
                    active_thresholds = json.loads(raw_t) if raw_t else DEFAULT_THRESHOLDS
                    
                    # Phase 13: Generic Threshold Evaluation mapping all dimensions
                    for key, val in payload.items():
                        if key in active_thresholds:
                            t = active_thresholds[key]
                            if val < t["min"] or val > t["max"]:
                                alert_key = f"{sensor_id}_{key}"
                                current_time = time.time()
                                
                                # Check the 1-Hour Cooldown per sensor-attribute pair
                                if current_time - last_alert_time.get(alert_key, 0) > ALERT_COOLDOWN:
                                    direction = "HIGH" if val > t["max"] else "LOW"
                                    alert_id = str(uuid.uuid4())
                                    msg = f"WARNING: {sensor_id} {key.upper()} is {direction} ({val:.2f})!\nSafe range: {t['min']} - {t['max']}."
                                    
                                    alert = {
                                        "type": "alert",
                                        "alert_id": alert_id,
                                        "sensor_id": sensor_id,
                                        "attribute": key,
                                        "level": "error",
                                        "message": msg
                                    }
                                    
                                    # Phase 18: Write persistent alert to InfluxDB
                                    pt = Point("alerts") \
                                        .tag("sensor_id", sensor_id) \
                                        .tag("attribute", key) \
                                        .tag("level", "error") \
                                        .field("alert_id", alert_id) \
                                        .field("value", float(val)) \
                                        .field("direction", direction) \
                                        .field("message", msg)
                                    write_api.write(bucket="raala", org="raala", record=pt)
                                    
                                    # Push the synthesized alert directly down the WebSocket TCP pipeline
                                    redis_client.publish(PUBSUB_CHANNEL, json.dumps(alert))
                                    print(f"FIRED RULE: {alert['message']}")
                                    last_alert_time[alert_key] = current_time

                except json.JSONDecodeError:
                    continue

    except redis.ConnectionError:
        print("Redis unavailable, retrying in 5 seconds...")
        time.sleep(5)
    except Exception as e:
        print(f"Rule Engine Runtime Error: {e}")
        time.sleep(1)
