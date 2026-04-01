# RAALA Live Sensor Pipeline Architecture & Implementation Guide

This document outlines the end-to-end architecture, step-by-step implementation phases, and potential bottleneck scenarios for the RAALA Live Sensor Pipeline. This pipeline captures simulated high-frequency IoT sensor data, processes it, persists it for historical analysis, and streams it live to a realtime dashboard.

---

## 1. System Architecture & Tech Stack

The architecture follows an asynchronous, event-driven microservices pattern designed to decouple rapid data ingestion from frontend presentation.

### The Stack:
*   **Infrastructure:** Docker Compose (Containerization)
*   **Ingestion / Message Broker:** Redis Streams (Handles high-throughput, bursty writes)
*   **Pub/Sub Messaging:** Redis Pub/Sub (Real-time broadcast channels)
*   **Cold Storage / Persistence:** InfluxDB v2 (Optimized time-series database for metrics)
*   **Backend Gateway:** FastAPI / Python (Asynchronous WebSocket serving)
*   **Frontend UI:** Vanilla JS, HTML5, CSS3, `Chart.js`, Native WebSockets

### Data Flow Diagram:
1.  **Data Generation:** `mock_sensors.py` generates noisy JSON payloads for 24 sensors every 1 second.
2.  **Ingestion:** Data is pushed into a Redis Stream (`rala:sensors:stream`).
3.  **Processing:** `stream_processor.py` continuously reads from the stream, applies an Exponentially Weighted Moving Average (EWMA) algorithm to smooth the noise, writes raw data to InfluxDB, and publishes smoothed data to a Redis Pub/Sub channel (`rala:sensors:ui`).
4.  **Gateway:** A FastAPI app (`main.py`) listens to the Pub/Sub channel asynchronously.
5.  **Delivery:** FastAPI broadcasts incoming data over native WebSockets (`ws://...`) to any connected web clients.
6.  **Presentation:** The frontend `app.js` filters the WebSocket stream, aggregates the data into 5-second graphical buffers, and draws live Chart.js visuals.

---

## 2. Implementation Phases (1 to 7)

### Phase 1: Local Infrastructure Setup
*   **Goal:** Establish the foundational databases.
*   **Implementation:** Created a `docker-compose.yml` defining `redis:alpine` and `influxdb:2.0` containers.
*   **Key Detail:** Pre-configured InfluxDB with auto-provisioned initial buckets (`raala`) and static admin tokens to bypass manual UI setup tasks.

### Phase 2: Python Backend Mocking
*   **Goal:** Simulate physical IoT devices.
*   **Implementation:** Created `api/mock_sensors.py`. It loops over 24 unique `sensor_id`s (e.g., `sensor_01` to `sensor_24`), injects randomized Gaussian noise into base metric values (Temperature, Humidity, VPD, PPFD), and executes `XADD` to push the payload to Redis.

### Phase 3: Data Processing & Persistence
*   **Goal:** Decouple ingestion from processing and save historical data.
*   **Implementation:** `stream_processor.py` was built to act as the consumer. 
    *   It uses Redis `XREAD BLOCK 0` to wait for new stream entries efficiently.
    *   It uses the official `influxdb-client` to batch-write time-series points.
    *   It applies mathematical EWMA (`alpha=0.2`) to eliminate extreme sensor spikes before publishing to the UI via `PUBLISH`.

### Phase 4: Dashboard Integration
*   **Goal:** Connect the physical UI to the new pipeline.
*   **Implementation:** Created `api/main.py` utilizing FastAPI's WebSocket capabilities and `asyncio.sleep` non-blocking loops. On the frontend, `app.js` was heavily refactored: removed the legacy Mosquitto MQTT library and established standard JS `new WebSocket()`.

### Phase 5: UI Refinement, Filtering & Averaging
*   **Goal:** Prevent UI thrashing (DOM rewriting 24 times a second).
*   **Implementation:** 
    *   **Filtering:** Mapped physical HTML pages (`data-sensor="bme280"`) to specific payload IDs (`sensor_01`). All non-matching payloads are dropped at the client level.
    *   **5-Second Array Buffer:** Created a JS array that collects 5 seconds of telemetry, computes the arithmetic mean, and strictly updates the large numeric DOM elements only when the buffer is full.

### Phase 6 & 7: Graph Visualization & Attribute Toggles
*   **Goal:** Provide professional, legible time-series plotting.
*   **Implementation:** 
    *   Injected `Chart.js` via CDN.
    *   Refactored the dashboard CSS Grid layout so the `<canvas>` occupies the full width of the main content column.
    *   Added dynamic UI buttons in `app.js` that read payload keys (e.g., `TEMPERATURE`, `VPD`). Clicking a button isolates that specific metric on the chart line, allowing `Chart.js` to automatically recalculate and scale the Y-Axis perfectly to the micro-fluctuations of that specific data point.

---

## 3. Bottleneck Scenarios & Mitigation Strategies

As the system moves toward production or scales up, the following bottlenecks must securely be addressed:

### A. Redis Memory Overflow (OOM)
*   **Scenario:** Redis Streams keep historical data indefinitely by default. Sending 24 messages per second will eventually consume all RAM.
*   **Mitigation:** In `mock_sensors.py`, the `XADD` command must utilize the `MAXLEN` argument (e.g., `MAXLEN ~ 10000`). This ensures Redis acts as a rolling buffer, automatically evicting the oldest logs and keeping memory usage flat and predictable.

### B. UI Render Thrashing (Client-Side CPU Spike)
*   **Scenario:** Processing thousands of WebSocket messages and re-rendering the DOM 60 times a second can cause the browser tab to crash or drain laptop batteries.
*   **Mitigation:** Successfully mitigated in Phase 5. By decoupling the background Chart update (1 Hz) from the heavy DOM text repaint (0.2 Hz / 5sec averages), the browser GPU/CPU maintains optimal efficiency.

### C. FastAPI Synchronous Blocking
*   **Scenario:** Standard Redis libraries (`redis-py`) are synchronous. If placed directly inside a FastAPI WebSocket event loop, one slow Redis read will freeze the server for all connected UI clients.
*   **Mitigation:** `main.py` utilizes `asyncio` and `aioredis` (or running standard Redis in a threaded executor/background task) to ensure the ASGI server remains fully non-blocking. 

### D. Silent Drop-Offs & Stale Connections
*   **Scenario:** Internet hiccups cause the WebSocket to close, leaving the UI showing old data.
*   **Mitigation:** Implemented robust reconnection logic inside `app.js` (`ws.onclose = () => { setTimeout(connect, 2000); }`).

### E. Long-Term InfluxDB Storage Costs
*   **Scenario:** Storing every single 1-second interval forever will lead to massive storage ballooning over years.
*   **Mitigation:** Implement InfluxDB Retention Policies (RPs) and Downsampling Tasks. For example: Keep 1-second raw data for 7 days, 1-minute averaged data for 30 days, and 1-hour averaged data indefinitely.

### F. Aggressive Browser Caching in Development
*   **Scenario:** Python's `http.server` issues `304 Not Modified` on `.js` files, preventing developers from seeing live updates.
*   **Mitigation:** In production, use Vite, Nginx, or Webpack to bundle assets with version hashes (e.g., `app.2f7a9.js`) to permanently solve cache invalidation.
