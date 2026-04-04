# RAALA Sensor Simulator: End-to-End Execution Guide

This document is a comprehensive manual for operating the local RAALA IoT sensor simulation environment. It outlines the precise startup commands, architectural behaviors, and background mechanics that route data from the virtual hardware to the graphical web dashboard.

---

## 1. Prerequisites & Database Infrastructure

Before launching any Python code, the foundational data layer must be online.

**Command:**
```powershell
cd e:\projects\rala\rala
docker compose up -d
```

---

## Phase 14: Zero-Touch Auto-Discovery Architecture

RAALA is now a **plug-and-play** IoT platform. Sensors self-register on boot, and the dashboard discovers them automatically. No HTML editing required to add a new sensor.

### How the HELLO Handshake Works

When `mock_sensors.py` starts, it emits one `HELLO` packet per sensor into the Redis stream **before** the data loop begins:

```json
{
  "type": "HELLO",
  "sensor_id": "sensor_01",
  "model": "BME280",
  "display_name": "BME280 — Temperature, Humidity & Pressure",
  "bus": "I2C",
  "capabilities": ["temperature", "humidity", "pressure", "vpd"]
}
```

`stream_processor.py` detects `type == "HELLO"` and stores the metadata in a Redis Hash (`rala:sensors:registry`), skipping all EWMA/InfluxDB processing for these packets.

### REST Inventory Endpoints

Two new endpoints are available on the FastAPI gateway:

| Endpoint | Description |
|---|---|
| `GET http://localhost:8000/api/inventory` | Returns all registered sensors as a JSON array |
| `GET http://localhost:8000/api/sensor-config/{sensor_id}` | Returns metadata for a single sensor |

### Dynamic Sensor URLs

- **Inventory page:** `http://localhost:8080/index.html` — auto-fetches `/api/inventory` and renders tiles dynamically
- **Universal dashboard:** `http://localhost:8080/dashboard.html?id=sensor_01` — replaces all individual sensor HTML pages

---

## Sensor Lifecycle Guide

### Adding a New Sensor

1. Add the sensor to the `sensors` array in `mock_sensors.py` with its metadata and capabilities
2. Add data generation logic in the `if/elif` block
3. Add threshold bounds to `THRESHOLDS` in `app.js` and `rule_engine.py`
4. Restart `mock_sensors.py` — the sensor tile appears on `index.html` automatically

### Removing a Sensor

1. Remove the sensor block from `mock_sensors.py`
2. Delete its Redis registry entry:
```powershell
docker exec -it rala-redis redis-cli HDEL rala:sensors:registry sensor_05
```
3. Restart `mock_sensors.py` — the tile disappears from `index.html` on next refresh

### If Registry is Empty

If `index.html` shows "No sensors registered yet" — the pipeline hasn't started or `mock_sensors.py` hasn't run yet. Start the pipeline and hard-refresh (`Ctrl+F5`).

### Stale Registry Entry

If you forget to `HDEL` an old sensor, its tile will still appear but the dashboard will show "Waiting for data..." indefinitely. This is harmless — just run the `HDEL` cleanup command above.
**Background Mechanics:**
*   This initiates the `docker-compose.yml` stack, booting up **Redis** and **InfluxDB v2**.
*   **Redis** will act as the ultra-fast message broker, handling both the persistent `Streams` (for ingestion from the sensors) and `Pub/Sub` channels (for high-speed routing to the web Gateway).
*   **InfluxDB** will act as the cold storage, securely retaining all historical time-series data for future queries or machine learning.

---

## 2. Launching the Microservices (The Execution Steps)

To run the full pipeline, you must open **four separate terminal windows**. This perfectly mimics a production environment where these services would run on entirely isolated servers or Kubernetes pods. 

### Terminal 1: The FastAPI WebSocket Gateway
```powershell
cd e:\projects\rala\rala\api
.\venv\Scripts\activate
uvicorn main:app --port 8000 --host 0.0.0.0
```
*   **Purpose:** The bridge between the backend stack and the public internet (your browser web app).
*   **What happens in the background:** `uvicorn` boots an ASGI asynchronous web server. Inside `main.py`, a background `asyncio` loop automatically connects to Redis and subscribes to the `rala:sensors:ui` Pub/Sub channel. It exposes the `ws://localhost:8000/ws/sensors` endpoint. When browsers connect, it adds them to a pool, and broadcasts every new Redis message it hears directly to their browser tabs over TCP.

### Terminal 2: The Stream Processor (Data Engine)
```powershell
cd e:\projects\rala\rala\api
.\venv\Scripts\activate
python stream_processor.py
```
*   **Purpose:** Sanitizes raw data and handles dual-routing to the backend databases and frontend UIs.
*   **What happens in the background:** This script firmly attaches itself to the Redis Stream `rala:sensors:stream` using a blocking `XREAD` command (it waits efficiently until new data exists). The moment a payload arrives, it:
    1.  Writes the raw, unedited metric into **InfluxDB** for historical permanence.
    2.  Pipes the metrics through an **EWMA (Exponentially Weighted Moving Average)** mathematical formula to smooth out erratic hardware noise spikes.
    3.  Publishes the polished, smoothed JSON payload to the Redis `rala:sensors:ui` Pub/Sub channel for the FastAPI Gateway.

### Terminal 3: The IoT Hardware Mock Generator
```powershell
cd e:\projects\rala\rala\api
.\venv\Scripts\activate
python mock_sensors.py
```
*   **Purpose:** Physically generates the fake telemetry data, pretending to be your actual Adafruit/I2C chips.
*   **What happens in the background:** An infinite `while True` loop fires every 1.0 seconds. It iterates over 24 distinct hardware IDs (`sensor_01` to `sensor_24`). For each sensor, it synthesizes baseline values (e.g., Temperature: 22°C) and injects randomized **Gaussian noise** to make the telemetry curve look incredibly realistic. It then executes an `XADD` command to aggressively push the JSON package into the Redis stream.

### Terminal 4: The Static Frontend UI
```powershell
cd e:\projects\rala\rala\simulator
python -m http.server 8080
```
*   **Purpose:** Delivers the HTML, CSS, and JS assets to your web browser. 
*   **What happens in the background:** It spins up Python's built-in HTTP server explicitly inside the `/simulator` routing directory.
*   **Action:** You can now navigate to `http://localhost:8080/index.html` in your web browser.

---

## 3. The End-to-End Data Pipeline (What Happens When You Click the UI)

1.  **Browser Boot:** You open `bme280.html`. The native `app.js` runs `new WebSocket('ws://localhost:8000/ws/sensors')`.
2.  **Handshake:** The FastAPI server accepts the connection. The green "Connected" badge lights up on the UI.
3.  **Data Tsunami:** The `mock_sensors.py` pulses, traversing the stream processor to FastAPI, dropping JSON objects right into `app.js`'s `ws.onmessage` event listener every 40 milliseconds (across 24 sensors).
4.  **Hardware Filtering:** `app.js` inspects the page's HTML body `data-sensor="bme280"` attribute, natively knowing it is looking for `sensor_01`. It cleanly deletes/ignores all payloads from the other 23 sensors.
5.  **Data Hydration:** 
    *   The raw JSON string is violently injected into the bottom "Live Data Feed Pipeline" terminal block for visual confirmation of backend integrity.
    *   The `TEMPERATURE` numeric is routed into `Chart.js`, plotting a dark-shaded accent dot on the interactive canvas. If the array exceeds your selected toggle window (e.g., **1M** vs **6H**), standard JavaScript forcefully pops the oldest node out of memory.
    *   Simultaneously, the numbers are captured in a highly temporary 5-second `dataBuffer` array. Once 5 payloads stack up, it calculates the arithmetic average, rewriting the massive glowing text blocks on the DOM exactly once to ensure human eye readability and prevent battery-draining CPU render locks.

---

## 4. Diagnostics & Hard Resetting

Because this architecture isolates processes via Docker and dedicated terminal processes, if the pipeline locks up, it is incredibly easy to diagnose.

*   **Symptoms:** The UI graph is flatlining or says "Waiting for data..." but the FastAPI endpoint is green ("Connected").
*   **Cause:** Either the `mock_sensors.py` script crashed/was closed, or the `stream_processor.py` script has been running for multiple days on a sleeping laptop and its TCP connection to Redis timed out.
*   **The Fix:** 
    1. Go to your terminals. 
    2. Press `Ctrl + C` inside the `uvicorn`, `stream_processor.py`, `rule_engine.py`, and `mock_sensors.py` tabs. 
    3. Simply press UP on your keyboard to relaunch each command. 
    4. Hit `Ctrl+F5` on your web browser. The entire microservice pipeline will reconstruct itself entirely within 2 seconds.

### 5. Advanced: Force-Killing "Ghost" Processes
Occasionally, Windows fails to gracefully terminate Python scripts via `Ctrl+C`, leaving "ghost" processes that continue to secretly occupy RAM, corrupt Redis streams, and maliciously lock TCP Port 8000. 

If your dashboard charts behave erratically (e.g. creating massive "sawtooth" patterns) or FastAPI refuses to boot due to an `[Errno 10048] address already in use` error, you must forcefully purge the pipeline daemons.

**Run the following native PowerShell execution block to blindly hunt and disintegrate the background pipelines:**

```powershell
Write-Host "Hunting Pipeline Daemons..."
Get-WmiObject Win32_Process | Where-Object { 
  $_.CommandLine -match 'mock_sensors.py' -or 
  $_.CommandLine -match 'stream_processor.py' -or 
  $_.CommandLine -match 'rule_engine.py' -or 
  $_.CommandLine -match 'main:app'
} | ForEach-Object { 
  Write-Host "Purging Ghost PID: $($_.ProcessId)"
  Stop-Process -Id $_.ProcessId -Force -ErrorAction SilentlyContinue 
}

Write-Host "Hunting Uvicorn Port 8000 Locks..."
$pid8000 = (netstat -ano | findstr :8000 | Select-String -Pattern "\s+(\d+)$").Matches.Groups[1].Value.Trim()
if ($pid8000) { 
  taskkill /PID $pid8000 /F 
  Write-Host "Assassinated Port 8000 PID: $pid8000"
}
Write-Host "All hardware systems purged. The environment is now pristine."
```
