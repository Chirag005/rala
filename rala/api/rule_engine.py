import redis
import json
import time

STREAM_KEY = 'rala:sensors:stream_v2'
PUBSUB_CHANNEL = 'rala:sensors:ui_v2'

# Connect to Redis to listen to the fire-hose of raw data
redis_client = redis.Redis(host='localhost', port=6379, decode_responses=True)

# Cooldown: 30s for test verification (restore to 3600 for production)
last_alert_time = {}
ALERT_COOLDOWN = 30  # seconds — change to 3600 for production (1 alert per hour)

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
                                
                                # Check the mathematically calculated 1-Hour Cooldown Limit mapping to specific nodes
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
