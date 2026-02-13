# RAALA Hardware Integration Architecture

## Production System Architecture for Live Sensor Feed

**Version:** 2.1-hardware-phase  
**Status:** Hardware Integration Phase  
**Last Updated:** January 2026

---

## 🎯 Executive Summary

This document defines the **production architecture** for RAALA's hardware integration phase, connecting Raspberry Pi sensors to the existing Nuxt 3 dashboard through a robust MQTT → FastAPI → WebSocket pipeline.

### Critical Architectural Decision

**✅ KEEP:** Nuxt 3 + Vue 3 frontend (Production-ready, premium UI)  
**✅ ADD:** Streamlit for local Pi debugging **ONLY**  
**❌ NEVER:** Replace Nuxt with Streamlit for customer-facing dashboard

**Rationale:** Your Nuxt 3 frontend is production-grade for a $110B market opportunity. Streamlit is a mechanic's diagnostic tool, not a customer-facing product.

---

## 🏗️ Four-Layer System Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│ LAYER 4: PRESENTATION LAYER (Customer-Facing UI)               │
│                                                                 │
│  ┌──────────────────────────────────────────────────────────┐  │
│  │           Nuxt 3 Dashboard (Production)                  │  │
│  │  ┌────────────────────────────────────────────────────┐ │  │
│  │  │ WebSocket Client (wss://api.raala.io/ws)          │ │  │
│  │  │ Components: MetricsGrid, SensorMesh, AgentLogs    │ │  │
│  │  │ Real-time updates < 500ms latency                 │ │  │
│  │  └────────────────────────────────────────────────────┘ │  │
│  └──────────────────────────────────────────────────────────┘  │
└─────────────────────────────────────────────────────────────────┘
                               ▲
                               │ WebSocket (wss://)
                               │
┌─────────────────────────────────────────────────────────────────┐
│ LAYER 3: CLOUD LAYER (The Brain)                               │
│                                                                 │
│  ┌──────────────────────────────────────────────────────────┐  │
│  │              FastAPI Backend                             │  │
│  │  ┌────────────────────────────────────────────────────┐ │  │
│  │  │ MQTT Subscriber    │  WebSocket Server            │ │  │
│  │  │ (Consumes data)    │  (Broadcasts to frontend)    │ │  │
│  │  └────────────────────────────────────────────────────┘ │  │
│  └──────────────────────────────────────────────────────────┘  │
│                                                                 │
│  ┌─────────────┐  ┌──────────────┐  ┌──────────────────────┐  │
│  │   Redis     │  │  InfluxDB    │  │   PostgreSQL         │  │
│  │  (Hot Data) │  │  (Time-Series│  │  (Users/Facilities)  │  │
│  │  Last 1 hour│  │   Historical)│  │                      │  │
│  └─────────────┘  └──────────────┘  └──────────────────────┘  │
└─────────────────────────────────────────────────────────────────┘
                               ▲
                               │ MQTT (QoS 1)
                               │
┌─────────────────────────────────────────────────────────────────┐
│ LAYER 2: TRANSPORT LAYER (The Nervous System)                  │
│                                                                 │
│  ┌──────────────────────────────────────────────────────────┐  │
│  │              MQTT Broker (Mosquitto / HiveMQ)            │  │
│  │  Topic: rala/facility_{id}/zone_{id}/climate            │  │
│  │  Payload: {"temp": 23.5, "humidity": 65, "ts": ...}     │  │
│  │  QoS: 1 (At-least-once delivery)                        │  │
│  │  Retained: Yes (last known value)                       │  │
│  └──────────────────────────────────────────────────────────┘  │
└─────────────────────────────────────────────────────────────────┘
                               ▲
                               │ Publish every 30s
                               │
┌─────────────────────────────────────────────────────────────────┐
│ LAYER 1: EDGE LAYER (The Physical Greenhouse)                  │
│                                                                 │
│  ┌──────────────────────────────────────────────────────────┐  │
│  │         Raspberry Pi 4 Model B (The Edge Gateway)        │  │
│  │                                                          │  │
│  │  ┌────────────────────────────────────────────────────┐ │  │
│  │  │  sensor_driver.py (Main Agent)                    │ │  │
│  │  │  ├─ Poll BME280 every 30s (I2C)                  │ │  │
│  │  │  ├─ Calculate VPD                                 │ │  │
│  │  │  ├─ Publish to MQTT broker                        │ │  │
│  │  │  └─ Buffer to SQLite if offline                   │ │  │
│  │  └────────────────────────────────────────────────────┘ │  │
│  │                                                          │  │
│  │  ┌────────────────────────────────────────────────────┐ │  │
│  │  │  debug_dashboard.py (Streamlit - Dev Tool Only)   │ │  │
│  │  │  └─ Local UI at http://<pi-ip>:8501              │ │  │
│  │  └────────────────────────────────────────────────────┘ │  │
│  └──────────────────────────────────────────────────────────┘  │
│                                                                 │
│  ┌──────────────────────────────────────────────────────────┐  │
│  │              Physical Sensors (I2C Bus)                  │  │
│  │  ┌──────────┐  ┌──────────┐  ┌──────────┐              │  │
│  │  │  BME280  │  │  BME280  │  │  BME280  │  (Multi-zone)│  │
│  │  │ Address: │  │ Address: │  │ Address: │              │  │
│  │  │  0x76    │  │  0x77    │  │ via MUX  │              │  │
│  │  └──────────┘  └──────────┘  └──────────┘              │  │
│  └──────────────────────────────────────────────────────────┘  │
└─────────────────────────────────────────────────────────────────┘
```

---

## 📋 Complete Data Flow (Sensor → Dashboard)

### **End-to-End Pipeline**

```
┌─────────┐   30s    ┌──────────┐   MQTT   ┌──────────┐   Write   ┌──────────┐
│ BME280  │ ──────> │ sensor_  │ ──────> │  MQTT    │ ──────>  │ InfluxDB │
│ (I2C)   │  Poll   │ driver.py│ Publish │  Broker  │  Store   │ (Cold)   │
└─────────┘         └──────────┘         └──────────┘          └──────────┘
                         │                     │
                         │                     │ Subscribe
                         ▼                     ▼
                    ┌──────────┐         ┌──────────┐   Write   ┌──────────┐
                    │  SQLite  │         │ FastAPI  │ ──────>  │  Redis   │
                    │ (Offline │         │ Ingestion│  Cache   │  (Hot)   │
                    │  Buffer) │         │  Worker  │          └──────────┘
                    └──────────┘         └──────────┘               │
                                              │                      │
                                              │ Broadcast            │
                                              ▼                      ▼
                                         ┌──────────┐         ┌──────────┐
                                         │WebSocket │ <────── │ FastAPI  │
                                         │  Server  │  Query  │   API    │
                                         └──────────┘         └──────────┘
                                              │
                                              │ wss://
                                              ▼
                                         ┌──────────┐
                                         │  Nuxt 3  │
                                         │Dashboard │
                                         │(Browser) │
                                         └──────────┘
```

### **Latency Breakdown**

| Stage     | Component           | Latency       | Protocol              |
| --------- | ------------------- | ------------- | --------------------- |
| 1         | BME280 read         | ~5ms          | I2C (400kHz)          |
| 2         | MQTT publish        | 5-50ms        | MQTT/TCP              |
| 3         | Broker routing      | 1-5ms         | Internal              |
| 4         | FastAPI ingestion   | 10-20ms       | Python async          |
| 5         | InfluxDB write      | 5-10ms        | Batch insert          |
| 6         | Redis cache         | 1-2ms         | In-memory             |
| 7         | WebSocket broadcast | 5-10ms        | wss://                |
| 8         | Browser update      | 16ms          | Vue reactivity        |
| **Total** | **End-to-end**      | **~50-120ms** | **< 500ms target** ✅ |

---

## 🔧 Technology Stack (Hardware Integration Phase)

### **LAYER 1: Edge (Raspberry Pi)**

#### **Hardware**

- **Raspberry Pi 4 Model B (4GB)** - Main edge gateway
- **Power:** 5V 3A USB-C supply (or PoE HAT for industrial)
- **Storage:** 32GB microSD Class 10 (OS + buffer)
- **Networking:** Ethernet (primary) + WiFi 5 (backup)

#### **Operating System**

```bash
OS: Raspberry Pi OS (64-bit, Lite)
Kernel: 6.1+ (for latest I2C drivers)
Python: 3.11.x
```

#### **Python Environment**

```bash
# Core sensor libraries
adafruit-circuitpython-bme280==2.6.x    # BME280 driver
paho-mqtt==1.6.x                         # MQTT client
python-dotenv==1.0.x                     # Config management

# Data handling
sqlite3                                  # Built-in (offline buffer)
pytz                                     # Timezone handling

# Optional: Local debugging
streamlit==1.28.x                        # Dev dashboard (local only)
plotly==5.17.x                          # Charts for Streamlit
```

#### **System Services**

```ini
# /etc/systemd/system/raala-sensor.service
[Unit]
Description=RAALA Sensor Driver
After=network-online.target
Wants=network-online.target

[Service]
Type=simple
User=pi
WorkingDirectory=/home/pi/raala-edge
ExecStart=/usr/bin/python3 sensor_driver.py
Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target
```

---

### **LAYER 2: Transport (MQTT)**

#### **MQTT Broker Options**

**Option 1: Self-Hosted Mosquitto (Recommended for MVP)**

```bash
# Install on cloud server (Ubuntu 22.04)
sudo apt install mosquitto mosquitto-clients

# Configure /etc/mosquitto/mosquitto.conf
listener 1883
protocol mqtt

listener 8883
protocol mqtt
cafile /etc/mosquitto/certs/ca.crt
certfile /etc/mosquitto/certs/server.crt
keyfile /etc/mosquitto/certs/server.key
```

**Option 2: HiveMQ Cloud (Managed, Free Tier)**

- URL: `broker.hivemq.com:8883`
- TLS: Required
- Free: Up to 100 connections

**Option 3: AWS IoT Core (Production)**

- Fully managed
- Certificate-based auth
- Integration with AWS services

#### **Topic Structure**

```
rala/
├── facility_<uuid>/
│   ├── zone_<id>/
│   │   ├── climate          # BME280 data
│   │   ├── light            # BH1750 data
│   │   ├── co2              # SCD30 data
│   │   └── soil             # Soil moisture
│   └── actuators/
│       ├── hvac             # Control commands
│       └── irrigation
└── system/
    ├── heartbeat            # Pi health check
    └── logs                 # Error logs
```

#### **Message Format (JSON)**

```json
{
  "facility_id": "550e8400-e29b-41d4-a716-446655440000",
  "zone_id": "zone_1",
  "sensor_id": "bme280_01",
  "timestamp": "2026-01-23T08:35:24.123Z",
  "data": {
    "temperature": 23.5,
    "humidity": 65.2,
    "pressure": 1013.2,
    "vpd": 1.21
  },
  "metadata": {
    "sensor_version": "bme280_v2.6",
    "firmware_version": "raala_edge_v1.0.0"
  }
}
```

---

### **LAYER 3: Cloud (FastAPI Backend)**

#### **Service Architecture**

```python
raala-backend/
├── app/
│   ├── main.py                    # FastAPI app
│   ├── mqtt_subscriber.py         # MQTT → InfluxDB worker
│   ├── websocket_server.py        # WebSocket endpoints
│   ├── api/
│   │   ├── routes/
│   │   │   ├── sensors.py         # Sensor data API
│   │   │   ├── facilities.py      # Facility CRUD
│   │   │   └── auth.py            # JWT auth
│   │   └── models/
│   │       └── sensor_data.py     # Pydantic schemas
│   └── services/
│       ├── influx_service.py      # InfluxDB client
│       ├── redis_service.py       # Redis client
│       └── supabase_service.py    # Auth/users
├── requirements.txt
└── Dockerfile
```

#### **Technology Stack**

```python
# FastAPI
fastapi==0.104.x
uvicorn[standard]==0.24.x          # ASGI server
python-jose[cryptography]==3.3.x   # JWT
pydantic==2.5.x                    # Validation

# MQTT
paho-mqtt==1.6.x                   # MQTT client

# Databases
influxdb-client==1.38.x            # InfluxDB 2.x
redis==5.0.x                       # Redis client
asyncpg==0.29.x                    # PostgreSQL async

# WebSocket
websockets==12.0
python-socketio==5.10.x            # Socket.IO support

# Monitoring
prometheus-client==0.19.x
sentry-sdk==1.38.x
```

#### **MQTT Subscriber Worker**

```python
# mqtt_subscriber.py
import paho.mqtt.client as mqtt
from influxdb_client import InfluxDBClient, Point
from redis import Redis
import json

class MQTTIngestionWorker:
    def __init__(self):
        self.mqtt_client = mqtt.Client()
        self.influx_client = InfluxDBClient(url=INFLUX_URL, token=INFLUX_TOKEN)
        self.redis_client = Redis(host=REDIS_HOST)

    def on_message(self, client, userdata, msg):
        """Process incoming MQTT messages"""
        data = json.loads(msg.payload)

        # Write to InfluxDB (cold storage)
        point = Point("sensor_readings")
            .tag("facility_id", data["facility_id"])
            .tag("zone_id", data["zone_id"])
            .tag("sensor_id", data["sensor_id"])
            .field("temperature", data["data"]["temperature"])
            .field("humidity", data["data"]["humidity"])
            .field("vpd", data["data"]["vpd"])
            .time(data["timestamp"])

        self.influx_client.write_api().write(bucket="raala", record=point)

        # Cache in Redis (hot storage - last 1 hour)
        cache_key = f"sensor:{data['facility_id']}:{data['zone_id']}"
        self.redis_client.setex(cache_key, 3600, json.dumps(data))

        # Broadcast to WebSocket clients
        await self.websocket_broadcast(data)

    def start(self):
        self.mqtt_client.on_message = self.on_message
        self.mqtt_client.connect(MQTT_BROKER, 1883)
        self.mqtt_client.subscribe("rala/#")
        self.mqtt_client.loop_forever()
```

#### **WebSocket Server**

```python
# websocket_server.py
from fastapi import FastAPI, WebSocket
from typing import List

app = FastAPI()
active_connections: List[WebSocket] = []

@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    active_connections.append(websocket)

    try:
        while True:
            # Keep connection alive
            await websocket.receive_text()
    except WebSocketDisconnect:
        active_connections.remove(websocket)

async def broadcast_sensor_update(data: dict):
    """Broadcast to all connected clients"""
    for connection in active_connections:
        await connection.send_json({
            "type": "sensor_update",
            "data": data
        })
```

---

### **LAYER 4: Presentation (Nuxt 3)**

#### **WebSocket Integration**

```typescript
// composables/useSensorData.ts
import { ref, onMounted, onUnmounted } from "vue";

export const useSensorData = () => {
  const metrics = ref({
    temperature: 0,
    humidity: 0,
    vpd: 0,
    co2: 0,
    ppfd: 0,
  });

  let ws: WebSocket | null = null;

  const connect = () => {
    ws = new WebSocket("wss://api.raala.io/ws");

    ws.onmessage = (event) => {
      const message = JSON.parse(event.data);

      if (message.type === "sensor_update") {
        metrics.value.temperature = message.data.data.temperature;
        metrics.value.humidity = message.data.data.humidity;
        metrics.value.vpd = message.data.data.vpd;
      }
    };

    ws.onerror = (error) => {
      console.error("WebSocket error:", error);
      // Reconnect logic
      setTimeout(connect, 5000);
    };
  };

  onMounted(() => connect());
  onUnmounted(() => ws?.close());

  return { metrics };
};
```

#### **Dashboard Component Update**

```vue
<!-- pages/dashboard.vue -->
<script setup>
import { useSensorData } from "~/composables/useSensorData";

const { metrics } = useSensorData();
</script>

<template>
  <div class="dashboard">
    <MetricsGrid :metrics="metrics" />
    <SensorMesh :zones="sensorZones" />
  </div>
</template>
```

---

## 🚀 Implementation Roadmap

### **Phase 1: Local Testing (Week 1)**

**Goal:** Verify BME280 → Streamlit works locally

**Tasks:**

1. ✅ Set up Raspberry Pi 4 with I2C enabled
2. ✅ Connect BME280 to GPIO pins (SDA/SCL)
3. ✅ Install Python dependencies
4. ✅ Write `test_sensor.py` to read I2C data
5. ✅ Create `debug_dashboard.py` (Streamlit) for local viewing
6. ✅ Access at `http://<pi-ip>:8501`

**Code: `debug_dashboard.py` (Streamlit - Dev Tool Only)**

```python
import streamlit as st
import board
from adafruit_bme280 import basic as adafruit_bme280
import time

st.set_page_config(page_title="RAALA Sensor Debug", page_icon="🌱")

i2c = board.I2C()
bme280 = adafruit_bme280.Adafruit_BME280_I2C(i2c)

st.title("🌱 RAALA Sensor Debug Dashboard")
st.caption("Local debugging tool - NOT for production")

col1, col2, col3 = st.columns(3)

# Auto-refresh every 5 seconds
if st.button("Start Live Feed"):
    placeholder = st.empty()

    while True:
        temp = bme280.temperature
        humidity = bme280.relative_humidity
        pressure = bme280.pressure

        # Calculate VPD
        vpd = calculate_vpd(temp, humidity)

        with placeholder.container():
            col1, col2, col3, col4 = st.columns(4)
            col1.metric("Temperature", f"{temp:.1f} °C", f"{temp-22:.1f}")
            col2.metric("Humidity", f"{humidity:.1f} %")
            col3.metric("Pressure", f"{pressure:.1f} hPa")
            col4.metric("VPD", f"{vpd:.2f} kPa")

        time.sleep(5)

def calculate_vpd(temp, rh):
    """Calculate Vapor Pressure Deficit"""
    svp = 0.6108 * (2.71828 ** ((17.27 * temp) / (temp + 237.3)))
    vpd = svp * (1 - rh / 100)
    return vpd
```

---

### **Phase 2: MQTT Pipeline (Week 2)**

**Goal:** Send data to cloud via MQTT

**Tasks:**

1. Set up MQTT broker (Mosquitto or HiveMQ)
2. Write `sensor_driver.py` with MQTT publish
3. Test publish/subscribe locally
4. Add offline buffering (SQLite)
5. Verify data reaches broker

**Code: `sensor_driver.py` (Production Agent)**

```python
import time
import json
import sqlite3
from datetime import datetime, timezone
import paho.mqtt.client as mqtt
import board
from adafruit_bme280 import basic as adafruit_bme280
from dotenv import load_dotenv
import os

load_dotenv()

# Configuration
MQTT_BROKER = os.getenv("MQTT_BROKER", "broker.hivemq.com")
MQTT_PORT = int(os.getenv("MQTT_PORT", 8883))
MQTT_TOPIC = os.getenv("MQTT_TOPIC", "rala/facility_01/zone_1/climate")
FACILITY_ID = os.getenv("FACILITY_ID", "550e8400-e29b-41d4-a716-446655440000")
SAMPLE_INTERVAL = int(os.getenv("SAMPLE_INTERVAL", 30))  # 30 seconds

class RAAlaSensorDriver:
    def __init__(self):
        # Initialize I2C and BME280
        self.i2c = board.I2C()
        self.bme280 = adafruit_bme280.Adafruit_BME280_I2C(self.i2c)

        # Initialize MQTT
        self.mqtt_client = mqtt.Client()
        self.mqtt_client.on_connect = self.on_connect
        self.mqtt_client.on_disconnect = self.on_disconnect
        self.is_connected = False

        # Initialize SQLite buffer
        self.init_buffer_db()

    def init_buffer_db(self):
        """Create SQLite database for offline buffering"""
        self.db = sqlite3.connect('/home/pi/raala_buffer.db')
        cursor = self.db.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS sensor_buffer (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                timestamp TEXT NOT NULL,
                payload TEXT NOT NULL,
                uploaded INTEGER DEFAULT 0
            )
        ''')
        self.db.commit()

    def on_connect(self, client, userdata, flags, rc):
        if rc == 0:
            print("✅ Connected to MQTT broker")
            self.is_connected = True
            self.upload_buffered_data()
        else:
            print(f"❌ Connection failed with code {rc}")

    def on_disconnect(self, client, userdata, rc):
        print("⚠️  Disconnected from MQTT broker")
        self.is_connected = False

    def calculate_vpd(self, temp, rh):
        """Calculate Vapor Pressure Deficit"""
        svp = 0.6108 * (2.71828 ** ((17.27 * temp) / (temp + 237.3)))
        vpd = svp * (1 - rh / 100)
        return round(vpd, 2)

    def read_sensor(self):
        """Read BME280 sensor data"""
        temp = round(self.bme280.temperature, 2)
        humidity = round(self.bme280.relative_humidity, 2)
        pressure = round(self.bme280.pressure, 2)
        vpd = self.calculate_vpd(temp, humidity)

        return {
            "temperature": temp,
            "humidity": humidity,
            "pressure": pressure,
            "vpd": vpd
        }

    def create_payload(self, sensor_data):
        """Create MQTT payload"""
        return {
            "facility_id": FACILITY_ID,
            "zone_id": "zone_1",
            "sensor_id": "bme280_01",
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "data": sensor_data,
            "metadata": {
                "sensor_version": "bme280_v2.6",
                "firmware_version": "raala_edge_v1.0.0"
            }
        }

    def publish_data(self, payload):
        """Publish to MQTT or buffer if offline"""
        payload_json = json.dumps(payload)

        if self.is_connected:
            try:
                result = self.mqtt_client.publish(MQTT_TOPIC, payload_json, qos=1)
                if result.rc == mqtt.MQTT_ERR_SUCCESS:
                    print(f"📤 Published: {payload['data']}")
                    return True
            except Exception as e:
                print(f"❌ Publish error: {e}")

        # Buffer if offline
        self.buffer_data(payload_json)
        return False

    def buffer_data(self, payload_json):
        """Store data in SQLite when offline"""
        cursor = self.db.cursor()
        cursor.execute(
            "INSERT INTO sensor_buffer (timestamp, payload) VALUES (?, ?)",
            (datetime.now(timezone.utc).isoformat(), payload_json)
        )
        self.db.commit()
        print(f"💾 Buffered data (offline)")

    def upload_buffered_data(self):
        """Upload buffered data when reconnected"""
        cursor = self.db.cursor()
        cursor.execute("SELECT id, payload FROM sensor_buffer WHERE uploaded = 0 ORDER BY id")
        rows = cursor.fetchall()

        for row_id, payload_json in rows:
            try:
                self.mqtt_client.publish(MQTT_TOPIC, payload_json, qos=1)
                cursor.execute("UPDATE sensor_buffer SET uploaded = 1 WHERE id = ?", (row_id,))
                self.db.commit()
                print(f"📤 Uploaded buffered data (ID: {row_id})")
            except Exception as e:
                print(f"❌ Failed to upload buffered data: {e}")
                break

    def start(self):
        """Main loop"""
        # Connect to MQTT broker
        try:
            self.mqtt_client.connect(MQTT_BROKER, MQTT_PORT, 60)
            self.mqtt_client.loop_start()
        except Exception as e:
            print(f"⚠️  MQTT connection failed: {e}")

        print(f"🚀 RAALA Sensor Driver started")
        print(f"📡 Publishing to: {MQTT_TOPIC}")
        print(f"⏱️  Sample interval: {SAMPLE_INTERVAL}s\n")

        try:
            while True:
                # Read sensor
                sensor_data = self.read_sensor()

                # Create payload
                payload = self.create_payload(sensor_data)

                # Publish
                self.publish_data(payload)

                # Wait
                time.sleep(SAMPLE_INTERVAL)

        except KeyboardInterrupt:
            print("\n🛑 Shutting down...")
            self.mqtt_client.loop_stop()
            self.mqtt_client.disconnect()
            self.db.close()

if __name__ == "__main__":
    driver = RAAlaSensorDriver()
    driver.start()
```

**Environment File: `.env`**

```bash
MQTT_BROKER=broker.hivemq.com
MQTT_PORT=8883
MQTT_TOPIC=rala/facility_01/zone_1/climate
FACILITY_ID=550e8400-e29b-41d4-a716-446655440000
SAMPLE_INTERVAL=30
```

---

### **Phase 3: Backend Ingestion (Week 3)**

**Goal:** Store data in InfluxDB and Redis

**Tasks:**

1. Set up InfluxDB 2.x instance
2. Set up Redis instance
3. Write FastAPI MQTT subscriber
4. Test data storage
5. Create API endpoints for historical queries

---

### **Phase 4: Dashboard Integration (Week 4)**

**Goal:** Display live data on Nuxt dashboard

**Tasks:**

1. Implement WebSocket server in FastAPI
2. Update Nuxt composable to connect
3. Wire `metrics.value` to real data
4. Test end-to-end latency
5. Add error handling and reconnection logic

---

## 📊 Monitoring & Debugging

### **System Health Dashboard (Streamlit on Pi)**

```python
# system_monitor.py
import streamlit as st
import subprocess

st.title("🔧 RAALA System Monitor")

# Service status
service_status = subprocess.run(
    ["systemctl", "is-active", "raala-sensor"],
    capture_output=True
).stdout.decode().strip()

st.metric("Sensor Service", service_status,
          delta="Running" if service_status == "active" else "Stopped")

# MQTT connectivity
mqtt_test = subprocess.run(
    ["mosquitto_sub", "-h", MQTT_BROKER, "-t", "test", "-C", "1", "-W", "2"],
    capture_output=True
)

st.metric("MQTT Connection",
          "Connected" if mqtt_test.returncode == 0 else "Disconnected")

# Buffered messages
cursor = sqlite3.connect('/home/pi/raala_buffer.db').cursor()
buffered_count = cursor.execute(
    "SELECT COUNT(*) FROM sensor_buffer WHERE uploaded = 0"
).fetchone()[0]

st.metric("Buffered Messages", buffered_count)
```

---

## 🎯 Success Metrics

### **Phase Completion Checklist**

**Phase 1: Local Testing** ✅

- [ ] BME280 reading via I2C
- [ ] Streamlit dashboard shows live data
- [ ] VPD calculation verified

**Phase 2: MQTT Pipeline** 🚧

- [ ] Data publishes to broker every 30s
- [ ] Offline buffering works (disconnect test)
- [ ] Reconnection uploads buffered data

**Phase 3: Cloud Storage** 📋

- [ ] InfluxDB stores time-series data
- [ ] Redis caches last 1 hour
- [ ] FastAPI serves historical queries

**Phase 4: Live Dashboard** 📋

- [ ] Nuxt dashboard shows real-time temp/humidity
- [ ] Latency < 500ms
- [ ] WebSocket reconnects on disconnect
- [ ] Metrics update smoothly without flicker

---

## 🚨 Critical Reminders

1. **Streamlit is NOT the product** - It's a mechanic's wrench for debugging the Pi locally
2. **Keep Nuxt 3** - Your production frontend is already world-class
3. **MQTT is the bridge** - Between hardware and cloud
4. **Buffer everything** - Greenhouses have unreliable internet
5. **Test reconnection** - Simulate network failures early

---

**Next Steps:** Would you like the complete `sensor_driver.py` code to copy directly to your Pi?
