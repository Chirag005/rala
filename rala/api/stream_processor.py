import time
import json
import redis
import os
from influxdb_client import InfluxDBClient, Point, WritePrecision
from influxdb_client.client.write_api import SYNCHRONOUS
from datetime import datetime, timezone

# Configurations
REDIS_HOST = os.getenv("REDIS_HOST", "localhost")
REDIS_PORT = 6379
STREAM_KEY = 'rala:sensors:stream_v2'
PUBSUB_CHANNEL = 'rala:sensors:ui_v2'
REGISTRY_KEY = 'rala:sensors:registry'  # Phase 14: Redis Hash for sensor inventory

INFLUX_URL = os.getenv("INFLUX_URL", "http://localhost:8086")
INFLUX_TOKEN = "raala-super-secret-token"
INFLUX_ORG = "raala"
INFLUX_BUCKET = "raala"

# Connections
redis_client = redis.Redis(host=REDIS_HOST, port=REDIS_PORT, db=0, decode_responses=True)
influx_client = InfluxDBClient(url=INFLUX_URL, token=INFLUX_TOKEN, org=INFLUX_ORG)
write_api = influx_client.write_api(write_options=SYNCHRONOUS)

# EWMA State
ewma_alpha = 0.2
ewma_state = {}

def calculate_ewma(sensor_id, new_data):
    if sensor_id not in ewma_state:
        ewma_state[sensor_id] = new_data
        return new_data
    
    smoothed = {}
    for key, value in new_data.items():
        if isinstance(value, (int, float)):
            prev = ewma_state[sensor_id].get(key, value)
            smoothed[key] = round(ewma_alpha * value + (1 - ewma_alpha) * prev, 2)
        else:
            smoothed[key] = value
            
    ewma_state[sensor_id] = smoothed
    return smoothed

print("RAALA Stream Processor Booting...")

last_id = '$'  # Start reading only new messages

while True:
    try:
        # Block for up to 1 second waiting for stream data
        messages = redis_client.xread({STREAM_KEY: last_id}, count=100, block=1000)
        
        if messages:
            for stream, msg_list in messages:
                for msg_id, msg_data in msg_list:
                    last_id = msg_id
                    
                    raw_payload = json.loads(msg_data['data'])
                    
                    # --- Phase 14: HELLO Handshake Intercept ---
                    # HELLO packets are registry announcements, not sensor readings.
                    # Store them in the Redis Hash and skip all EWMA/InfluxDB processing.
                    if raw_payload.get('type') == 'HELLO':
                        sensor_id = raw_payload.get('sensor_id')
                        redis_client.hset(REGISTRY_KEY, sensor_id, json.dumps(raw_payload))
                        print(f"Registered sensor: {sensor_id} ({raw_payload.get('model')})")
                        continue
                    
                    sensor_id = raw_payload.pop('sensor_id')
                    timestamp_str = raw_payload.pop('timestamp')
                    
                    # 1. Write raw data to InfluxDB dynamically based on ANY keys found
                    point = Point("sensor_readings") \
                        .tag("facility_id", "facility_01") \
                        .tag("zone_id", "zone_1") \
                        .tag("pipeline", "v2") \
                        .tag("sensor_id", sensor_id)
                    
                    for key, val in raw_payload.items():
                        if isinstance(val, (int, float)):
                            point = point.field(key, float(val))
                            
                    point = point.time(timestamp_str, WritePrecision.NS)
                    write_api.write(bucket=INFLUX_BUCKET, record=point)
                    
                    # 2. Calculate EWMA natively on all attributes
                    smoothed_values = calculate_ewma(sensor_id, raw_payload)
                    
                    # 3. Publish smoothed payload to Pub/Sub
                    smoothed_payload = {
                        "type": "sensor_update",
                        "sensor_id": sensor_id,
                        "timestamp": timestamp_str,
                        "data": smoothed_values
                    }
                    
                    redis_client.publish(PUBSUB_CHANNEL, json.dumps(smoothed_payload))
                    
                    
    except Exception as e:
        print(f"Error processing stream: {e}")
        time.sleep(1)
