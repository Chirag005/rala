# Phase 15: Sensor Heartbeat & Offline Detection

## 1. What We Built
We solved the "fake live" issue, where a sensor that died or was unplugged would permanently display its last known value with a green "Live" dot on the RAALA dashboard.

1. **The Stamp (`mock_sensors.py`)**: Every time a sensor publishes telemetry, it also issues a `SETEX rala:heartbeat:{sensor_id} 12 1`. This sets a TTL (Time-to-Live) key that expires independently if not refreshed within 12 seconds.
2. **The Watcher (`rule_engine.py`)**: A daemon thread polls all registered sensors in `rala:sensors:registry` every 5 seconds. If `rala:heartbeat:{id}` is missing, it triggers an `offline` payload down the WebSocket pipeline. If it returns, it triggers an `online` payload.
3. **The UI (`app.js` & `style.css`)**: 
   - Dynamically intercepts these events. 
   - Transitions the dashboard green pulse dot to grey, updates the text to `Offline`, records a `Last seen` timestamp and fires a toast notification.
   - Clears the "Live" state from the `index.html` inventory tiles, marking them "Sensor Offline".

## 2. Why We Built It This Way
- **Redis TTL vs. In-memory timers:** By letting Redis handle the TTL, the "offline" definition spans across independent processes safely. If `mock_sensors.py` crashes, Redis purges the key automatically. 
- **Watcher Thread vs. Async:** `rule_engine.py` is entirely synchronous right now. Using Python's `threading.Thread(target=heartbeat_watcher, daemon=True)` decoupled the 5s sleep loop from the fast-paced `redis_client.xread` stream block perfectly.
- **Frontend Stateless Application:** The backend dictates "offline" and "online". `app.js` no longer guesses if a sensor is dead via custom JavaScript timers.

## 3. Problems Overcome
- **The "Missing Context" Bug on Page Reloads:** During verification, if you reload `index.html` *after* the offline transition occurred, the tile shows "Live" with `--:--:--` for the timestamp. This happens because the backend only broadcasts `offline` on the exact *transition* boundary. Since making endpoints full stateful is redundant at Phase 15, we accept that an active WebSockets feed intercepts transitions perfectly.
