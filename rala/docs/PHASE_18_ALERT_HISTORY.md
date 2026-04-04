# Phase 18: Notification Bell & Alert History Drawer

## Overview
Phase 18 implements a persistent backend storage mapping for all triggered alerts, allowing historical audit trailing inside a clean, glassmorphic UI overlay on the frontend.

## Architecture

1. **InfluxDB Persistent Log**
   - The `rule_engine.py` generates native UUIDs for every anomaly. 
   - Anomalies are pushed to the WebSocket stream, but explicitly mapped as a `Point("alerts")` in InfluxDB, tracking `{alert_id, sensor_id, attribute, value, message}`.

2. **Redis Acknowledgment State**
   - A Redis SET `rala:alerts:acknowledged` tracks the UUID of any reviewed alert.

3. **API Cross-Stitching**
   - `GET /api/alerts`: Executes an InfluxDB `Flux` query scanning the `alerts` measurement across a rolling 24h window. The Python API automatically intersects the response with `SMEMBERS rala:alerts:acknowledged` to decorate the JSON with an `acknowledged: true/false` field before serving to the client.
   - `POST /api/alerts/acknowledge/{id}`: Commits the UUID mapping into the Redis SET.

4. **Frontend Implementation**
   - A persistent Notification Bell `.badge` listens to WebSocket fire-hose `type === "alert"` events.
   - It acts purely natively, incrementing instantly decoupled from backend polling.
   - Opening the Notification Drawer flushes the unread badge and requests the 24h timeline.
   - Clicking "Acknowledge" fires the POST, rendering inline strikethrough logic (Phase 13 aesthetic context).
