import time
import json
import random
from datetime import datetime, timezone
import paho.mqtt.client as mqtt
import logging
import sys

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

MQTT_BROKER = "localhost"
MQTT_PORT = 1883
FACILITY_ID = "550e8400-e29b-41d4-a716-446655440000"
ZONE_ID = "zone_1"
PUBLISH_INTERVAL = 3

class FakeBME280:
    def __init__(self):
        self.temperature = 23.5
        self.humidity = 65.0
        self.pressure = 1013.25

    def read(self):
        self.temperature = max(15.0, min(35.0, self.temperature + random.uniform(-0.2, 0.2)))
        self.humidity = max(40.0, min(90.0, self.humidity + random.uniform(-0.5, 0.5)))
        self.pressure = max(980.0, min(1050.0, self.pressure + random.uniform(-0.1, 0.1)))
        return round(self.temperature, 2), round(self.humidity, 2), round(self.pressure, 2)

class FakeAS7341:
    def __init__(self):
        self.lux = 500.0
        self.color_temp = 4000.0

    def read(self):
        self.lux = max(0.0, self.lux + random.uniform(-10, 10))
        self.color_temp = max(2000.0, self.color_temp + random.uniform(-50, 50))
        return round(self.lux, 2), round(self.color_temp, 0)

class FakeSGP30:
    def __init__(self):
        self.eco2 = 400.0 # ppm
        self.tvoc = 0.0 # ppb

    def read(self):
        self.eco2 = max(400.0, min(2000.0, self.eco2 + random.uniform(-5, 15)))
        self.tvoc = max(0.0, min(1000.0, self.tvoc + random.uniform(-2, 5)))
        return round(self.eco2, 0), round(self.tvoc, 0)

class FakeSoilMoisture:
    def __init__(self):
        self.moisture = 45.0 # percent

    def read(self):
        # Soil moisture drops slowly
        self.moisture = max(0.0, min(100.0, self.moisture - random.uniform(0.01, 0.05)))
        return round(self.moisture, 2)

def calculate_vpd(temp, rh):
    svp = 0.6108 * (2.71828 ** ((17.27 * temp) / (temp + 237.3)))
    vpd = svp * (1 - rh / 100)
    return round(vpd, 2)

def on_connect(client, userdata, flags, rc):
    if rc == 0:
        logger.info(f"Connected to MQTT broker at {MQTT_BROKER}:{MQTT_PORT}")
    else:
        logger.error(f"Failed to connect, return code {rc}")

def main():
    logger.info("Starting Multi-Sensor Data Generator")
    
    bme280 = FakeBME280()
    as7341 = FakeAS7341()
    sgp30 = FakeSGP30()
    soil = FakeSoilMoisture()

    client = mqtt.Client(client_id="generator_simulator")
    client.on_connect = on_connect
    
    try:
        client.connect(MQTT_BROKER, MQTT_PORT, 60)
        client.loop_start()
    except Exception as e:
        logger.error(f"Could not connect to MQTT Broker: {e}")
        sys.exit(1)

    try:
        while True:
            # BME280
            temp, hum, pres = bme280.read()
            client.publish("rala/facility_01/zone_1/bme280", json.dumps({
                "sensor_id": "BME280", "timestamp": datetime.now(timezone.utc).isoformat(),
                "data": {"temperature": temp, "humidity": hum, "pressure": pres, "vpd": calculate_vpd(temp, hum)}
            }))

            # AS7341
            lux, cct = as7341.read()
            client.publish("rala/facility_01/zone_1/as7341", json.dumps({
                "sensor_id": "AS7341", "timestamp": datetime.now(timezone.utc).isoformat(),
                "data": {"lux": lux, "color_temperature": cct}
            }))

            # SGP30
            eco2, tvoc = sgp30.read()
            client.publish("rala/facility_01/zone_1/sgp30", json.dumps({
                "sensor_id": "SGP30", "timestamp": datetime.now(timezone.utc).isoformat(),
                "data": {"eco2": eco2, "tvoc": tvoc}
            }))

            # Soil Moisture (via ADS1115)
            moist = soil.read()
            client.publish("rala/facility_01/zone_1/soil", json.dumps({
                "sensor_id": "SoilMoisture", "timestamp": datetime.now(timezone.utc).isoformat(),
                "data": {"moisture": moist}
            }))

            time.sleep(PUBLISH_INTERVAL)
            
    except KeyboardInterrupt:
        logger.info("Shutting down generator...")
        client.loop_stop()
        client.disconnect()
        sys.exit(0)

if __name__ == "__main__":
    main()
