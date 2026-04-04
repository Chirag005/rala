import json
import asyncio
from fastapi import FastAPI, WebSocket, WebSocketDisconnect, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import redis.asyncio as aioredis
from typing import List, Dict
from influxdb_client import InfluxDBClient
from pydantic import BaseModel
import os
import os

app = FastAPI(title="RAALA Live Sensor API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

PUBSUB_CHANNEL = 'rala:sensors:ui_v2'
REGISTRY_KEY = 'rala:sensors:registry'  # Phase 14: sensor inventory
# Async Redis connection for listening to the pubsub without blocking the main event loop
REDIS_HOST = os.getenv("REDIS_HOST", "localhost")
redis_conn = aioredis.from_url(f"redis://{REDIS_HOST}:6379", decode_responses=True)

# InfluxDB Configuration
INFLUX_URL = os.getenv("INFLUX_URL", "http://localhost:8086")
INFLUX_TOKEN = "raala-super-secret-token"
INFLUX_ORG = "raala"
INFLUX_BUCKET = "raala"

influx_client = InfluxDBClient(url=INFLUX_URL, token=INFLUX_TOKEN, org=INFLUX_ORG)
query_api = influx_client.query_api()

class ConnectionManager:
    def __init__(self):
        self.active_connections: List[WebSocket] = []

    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        self.active_connections.append(websocket)
        print(f"New client connected. Total clients: {len(self.active_connections)}")

    def disconnect(self, websocket: WebSocket):
        if websocket in self.active_connections:
            self.active_connections.remove(websocket)
            print(f"Client disconnected. Total clients: {len(self.active_connections)}")

    async def broadcast(self, message: str):
        broken_conns = []
        for connection in self.active_connections:
            try:
                await connection.send_text(message)
            except Exception:
                broken_conns.append(connection)
        for dead_conn in broken_conns:
            self.disconnect(dead_conn)

manager = ConnectionManager()

@app.on_event("startup")
async def startup_event():
    # Start the background task to listen to Redis Pub/Sub
    asyncio.create_task(redis_listener())

async def redis_listener():
    pubsub = redis_conn.pubsub()
    await pubsub.subscribe(PUBSUB_CHANNEL)
    print(f"Subscribed to Redis channel: {PUBSUB_CHANNEL}")
    
    try:
        async for message in pubsub.listen():
            if message['type'] == 'message':
                data = message['data']
                await manager.broadcast(data)
    except Exception as e:
        print(f"Redis Listener Error: {e}")

@app.websocket("/ws/sensors")
async def websocket_endpoint(websocket: WebSocket):
    await manager.connect(websocket)
    try:
        while True:
            # We must await receive_text to recognize when the client disconnects
            await websocket.receive_text()
    except WebSocketDisconnect:
        manager.disconnect(websocket)

@app.get("/api/history/{sensor_id}")
async def get_history(sensor_id: str, horizon: str = "1M"):
    horizon_map = {
        "1M": ("-1m", "1s"),
        "5M": ("-5m", "5s"),
        "30M": ("-30m", "30s"),
        "1H": ("-1h", "1m"),
        "6H": ("-6h", "6m"),
        "1D": ("-24h", "24m")
    }
    start_param, interval_param = horizon_map.get(horizon.upper(), ("-1m", "1s"))

    query = f'''
    from(bucket: "{INFLUX_BUCKET}")
      |> range(start: {start_param})
      |> filter(fn: (r) => r["_measurement"] == "sensor_readings")
      |> filter(fn: (r) => r["sensor_id"] == "{sensor_id}")
      |> filter(fn: (r) => r["pipeline"] == "v2")
      |> aggregateWindow(every: {interval_param}, fn: mean, createEmpty: false)
      |> yield(name: "mean")
    '''
    try:
        # Offload synchronous network I/O to a background thread to preserve async event loop
        result = await asyncio.to_thread(query_api.query, org=INFLUX_ORG, query=query)
        
        time_map = {}
        for table in result:
            for record in table.records:
                t_str = record.get_time().isoformat()
                field = record.get_field()
                val = record.get_value()
                if t_str not in time_map:
                    time_map[t_str] = {}
                if val is not None:
                    time_map[t_str][field] = round(val, 2)
                    
        sorted_times = sorted(time_map.keys())
        formatted_history = []
        for t in sorted_times:
            formatted_history.append({
                "timestamp": t,
                "data": time_map[t]
            })
            
        print(f"Sent {len(formatted_history)} historical rows for {sensor_id} ({horizon})")
        return formatted_history
    except Exception as e:
        print(f"Flux Query Error: {e}")
        return []

# ─────────────────────────────────────────────
# Phase 14: Auto-Discovery Inventory Endpoints
# ─────────────────────────────────────────────

@app.get("/api/inventory")
async def get_inventory():
    """Returns all sensors registered via the HELLO handshake."""
    registry = await redis_conn.hgetall(REGISTRY_KEY)
    sensors = []
    for sensor_id, metadata_str in registry.items():
        try:
            meta = json.loads(metadata_str)
            # Deserialise the capabilities list (stored as JSON string in Redis)
            if isinstance(meta.get('capabilities'), str):
                meta['capabilities'] = json.loads(meta['capabilities'])
            sensors.append(meta)
        except Exception:
            continue
    # Sort by sensor_id for stable ordering
    sensors.sort(key=lambda s: s.get('sensor_id', ''))
    return sensors

# ─────────────────────────────────────────────
# Phase 17: UI-Configurable Thresholds
# ─────────────────────────────────────────────
class ThresholdModel(BaseModel):
    min: float
    max: float

class ThresholdUpdateModel(BaseModel):
    thresholds: Dict[str, ThresholdModel]

@app.get("/api/thresholds/{sensor_id}")
async def get_thresholds(sensor_id: str):
    data = await redis_conn.get(f"rala:thresholds:{sensor_id}")
    if data:
        return json.loads(data)
    # Phase 13 Hardcoded Defaults Fallback
    defaults = {
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
    return defaults

@app.put("/api/thresholds/{sensor_id}")
async def update_thresholds(sensor_id: str, payload: ThresholdUpdateModel):
    data_dict = {k: {"min": v.min, "max": v.max} for k, v in payload.thresholds.items()}
    await redis_conn.set(f"rala:thresholds:{sensor_id}", json.dumps(data_dict))
    return {"status": "success", "message": f"Thresholds saved for {sensor_id}"}

# ─────────────────────────────────────────────
# Phase 18: Notification Bell Alert History
# ─────────────────────────────────────────────
@app.get("/api/alerts")
async def get_alerts(unacked_only: bool = False):
    query_api = influx_client.query_api()
    # Query last 24 hours of alerts
    query = f'''
    from(bucket: "{INFLUX_BUCKET}")
      |> range(start: -24h)
      |> filter(fn: (r) => r["_measurement"] == "alerts")
      |> filter(fn: (r) => r["_field"] == "message")
    '''
    try:
        result = await asyncio.to_thread(query_api.query, org=INFLUX_ORG, query=query)
        alerts = []
        for table in result:
            for record in table.records:
                alert_id = record.values.get("alert_id", "unknown")
                alerts.append({
                    "id": alert_id,
                    "timestamp": record.get_time().isoformat(),
                    "sensor_id": record.values.get("sensor_id"),
                    "attribute": record.values.get("attribute"),
                    "level": record.values.get("level"),
                    "message": record.get_value()
                })
        
        alerts.sort(key=lambda x: x["timestamp"], reverse=True)
        
        # Check ack state
        acked_ids = await redis_conn.smembers("rala:alerts:acknowledged")
        final_alerts = []
        for a in alerts:
            a["acknowledged"] = a["id"] in acked_ids
            if unacked_only and a["acknowledged"]:
                continue
            final_alerts.append(a)
            
        return final_alerts
    except Exception as e:
        print(f"Flux Alert Query Error: {e}")
        return []

@app.post("/api/alerts/acknowledge/{alert_id}")
async def acknowledge_alert(alert_id: str):
    await redis_conn.sadd("rala:alerts:acknowledged", alert_id)
    return {"status": "success"}
@app.get("/api/sensor-config/{sensor_id}")
async def get_sensor_config(sensor_id: str):
    """Returns metadata for a single sensor by ID."""
    metadata_str = await redis_conn.hget(REGISTRY_KEY, sensor_id)
    if not metadata_str:
        raise HTTPException(status_code=404, detail=f"Sensor '{sensor_id}' not found in registry.")
    meta = json.loads(metadata_str)
    if isinstance(meta.get('capabilities'), str):
        meta['capabilities'] = json.loads(meta['capabilities'])
    return meta
