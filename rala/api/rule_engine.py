import redis
import json
import time
import threading
import os

STREAM_KEY = 'rala:sensors:stream_v2'
PUBSUB_CHANNEL = 'rala:sensors:ui_v2'
REGISTRY_KEY = 'rala:sensors:registry'

# Connect to Redis to listen to the fire-hose of raw data
REDIS_HOST = os.getenv("REDIS_HOST", "localhost")
redis_client = redis.Redis(host=REDIS_HOST, port=6379, decode_responses=True)

# Cooldown: 3600 for production (1 alert per sensor-attribute per hour)
last_alert_time = {}
ALERT_COOLDOWN = 3600  # seconds

# Phase 13 Mathematical Boundaries
THRESHOLDS = {
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
                    
                    # Phase 13: Generic Threshold Evaluation mapping all dimensions
                    for key, val in payload.items():
                        if key in THRESHOLDS:
                            t = THRESHOLDS[key]
                            if val < t["min"] or val > t["max"]:
                                alert_key = f"{sensor_id}_{key}"
                                current_time = time.time()
                                
                                # Check the 1-Hour Cooldown per sensor-attribute pair
                                if current_time - last_alert_time.get(alert_key, 0) > ALERT_COOLDOWN:
                                    direction = "HIGH" if val > t["max"] else "LOW"
                                    
                                    alert = {
                                        "type": "alert",
                                        "sensor_id": sensor_id,
                                        "level": "error",
                                        "message": f"WARNING: {sensor_id} {key.upper()} is {direction} ({val:.2f})!\nSafe range: {t['min']} - {t['max']}."
                                    }
                                    
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
