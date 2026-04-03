import time
import json
import random
from datetime import datetime, timezone
import redis

# Redis connection
redis_client = redis.Redis(host='localhost', port=6379, db=0, decode_responses=True)
STREAM_KEY = 'rala:sensors:stream_v2'

# Initialize 4 Specific Polymorphic Sensors
sensors = [
    {
        "id": "sensor_01", "type": "BME280",
        "model": "BME280",
        "display_name": "BME280 — Temperature, Humidity & Pressure",
        "bus": "I2C",
        "capabilities": ["temperature", "humidity", "pressure", "vpd"]
    },
    {
        "id": "sensor_02", "type": "AS7341",
        "model": "AS7341",
        "display_name": "AS7341 — 10-Channel Light & Color Sensor",
        "bus": "I2C",
        "capabilities": ["ambient_light", "color_temp", "ppfd"]
    },
    {
        "id": "sensor_03", "type": "SGP30",
        "model": "SGP30",
        "display_name": "SGP30 — Air Quality (eCO2 & TVOC)",
        "bus": "I2C",
        "capabilities": ["eco2", "tvoc"]
    },
    {
        "id": "sensor_04", "type": "SOIL",
        "model": "Soil Moisture",
        "display_name": "Soil Moisture Sensor (via ADS1115 ADC)",
        "bus": "Analog (I2C ADC)",
        "capabilities": ["moisture", "soil_temp"]
    }
]

# Baseline anchors for walking drift
# Note: baselines are set to realistic "stressed" values so all sensors drift
# in and out of their safe zones, generating alerts across all 4 hardware types.
base_values = {
    "sensor_01": {"temperature": 24.0, "humidity": 60.0, "pressure": 1013.0, "vpd": 0.5},
    # sensor_02: lux below min (2000) to simulate low-light alert
    "sensor_02": {"ambient_light": 1000.0, "color_temp": 5000.0, "ppfd": 600.0},
    # sensor_03: eco2 above max (800) and tvoc above max (100) to simulate air quality alert
    "sensor_03": {"eco2": 850.0, "tvoc": 120.0},
    # sensor_04: moisture below min (30) and soil_temp above max (22) to simulate dry/warm soil alert
    "sensor_04": {"moisture": 25.0, "soil_temp": 23.5}
}

print(f"Starting POLYMORPHIC mock data generation for 4 distinct hardware signatures...")
print(f"Publishing to Redis Stream: {STREAM_KEY}")

# --- Phase 14: HELLO Handshake ---
# Emit one HELLO packet per sensor into the stream at boot.
# stream_processor.py intercepts these and writes them to the Redis registry.
for s in sensors:
    hello_packet = {
        "type": "HELLO",
        "sensor_id": s["id"],
        "model": s["model"],
        "display_name": s["display_name"],
        "bus": s["bus"],
        "capabilities": json.dumps(s["capabilities"])  # Redis streams store strings
    }
    redis_client.xadd(STREAM_KEY, {"data": json.dumps(hello_packet)})
    print(f"HELLO sent: {s['id']} ({s['display_name']})")


try:
    while True:
        timestamp = datetime.now(timezone.utc).isoformat()
        
        for s in sensors:
            s_id = s["id"]
            s_type = s["type"]
            base = base_values[s_id]
            
            payload = {"sensor_id": s_id, "timestamp": timestamp}
            
            if s_type == "BME280":
                temp = max(18.0, min(35.0, base["temperature"] + random.uniform(-0.1, 0.1)))
                rh = max(40.0, min(80.0, base["humidity"] + random.uniform(-0.2, 0.2)))
                pr = max(980.0, min(1050.0, base["pressure"] + random.uniform(-0.5, 0.5)))
                svp = 0.6108 * (2.71828 ** ((17.27 * temp) / (temp + 237.3)))
                vpd = svp * (1 - rh / 100)
                
                base.update({"temperature": temp, "humidity": rh, "pressure": pr})
                payload["temperature"] = round(temp, 2)
                payload["humidity"] = round(rh, 2)
                payload["pressure"] = round(pr, 2)
                payload["vpd"] = round(vpd, 2)
                
            elif s_type == "AS7341":
                lux = max(100.0, min(5000.0, base["ambient_light"] + random.uniform(-10.0, 10.0)))
                ct = max(2000.0, min(10000.0, base["color_temp"] + random.uniform(-50.0, 50.0)))
                ppfd = max(0.0, min(2000.0, base["ppfd"] + random.uniform(-5.0, 5.0)))
                
                base.update({"ambient_light": lux, "color_temp": ct, "ppfd": ppfd})
                payload["ambient_light"] = round(lux, 2)
                payload["color_temp"] = round(ct, 2)
                payload["ppfd"] = round(ppfd, 2)
                
            elif s_type == "SGP30":
                eco2 = max(400.0, min(2000.0, base["eco2"] + random.uniform(-2.0, 2.0)))
                tvoc = max(0.0, min(500.0, base["tvoc"] + random.uniform(-1.0, 1.0)))
                
                base.update({"eco2": eco2, "tvoc": tvoc})
                payload["eco2"] = round(eco2, 2)
                payload["tvoc"] = round(tvoc, 2)
                
            elif s_type == "SOIL":
                moist = max(0.0, min(100.0, base["moisture"] + random.uniform(-0.1, 0.1)))
                stemp = max(15.0, min(30.0, base["soil_temp"] + random.uniform(-0.05, 0.05)))
                
                base.update({"moisture": moist, "soil_temp": stemp})
                payload["moisture"] = round(moist, 2)
                payload["soil_temp"] = round(stemp, 2)

            # Redis injection + Phase 15 Heartbeat TTL key
            redis_client.xadd(STREAM_KEY, {"data": json.dumps(payload)})
            redis_client.setex(f"rala:heartbeat:{s_id}", 12, "1")  # 12s TTL — expires if silent
            
        print(f"[{timestamp}] Published distinct payloads for 4 sensors")
        time.sleep(1)

except KeyboardInterrupt:
    print("\nShutting down mock sensor generator...")
except Exception as e:
    print(f"Error occurred: {e}")
