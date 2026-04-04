# Phase 17: UI-Configurable Thresholds

## Overview
Phase 17 completes the transition from hard-coded server-side alert constraints to a fully dynamic, UI-driven architecture. Users can now tweak bounds directly from the frontend dashboard and have them apply instantly.

## Architecture

1. **Redis Hash Storage**
   Thresholds are stored in a key `rala:thresholds:{sensor_id}` as serialized JSON. 
   Redis provides atomic gets and puts, acting as the Single Source of Truth.

2. **FastAPI Endpoints**
   - `GET /api/thresholds/{sensor_id}`: Fetches active thresholds from Redis, defaulting to mathematical bounds identical to Phase 13 if unconfigured.
   - `PUT /api/thresholds/{sensor_id}`: Flushes new slider values to Redis.

3. **Rule Engine Ingestion**
   The `rule_engine.py` daemon directly queries `rala:thresholds:{sensor_id}` from Redis on *every incoming stream evaluation*. Because Redis is exceptionally fast (~1ms local network), this acts as a hot-reload compute mechanism without needing container restarts.

4. **Slide-Out Config Drawer**
   The frontend utilizes a heavy glassmorphic aesthetic (`.slide-drawer`) for an off-canvas config panel, generating UI sliders dynamically based on the current parsed sensor capabilities (e.g. Temperature, Light).
