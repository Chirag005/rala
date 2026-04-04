# RAALA Sensor Simulator: Phase 1–14 Engineering Log

> **What this document is:** A thorough account of every engineering decision made across 14 development phases. For each phase: what we built, *why* we built it that way, and *what specific problems we ran into and solved*.

---

## Table of Contents
1. [Phase 1 — Local Infrastructure Setup](#phase-1)
2. [Phase 2 — Python Hardware Mocking](#phase-2)
3. [Phase 3 — Data Processing & InfluxDB Persistence](#phase-3)
4. [Phase 4 — FastAPI WebSocket Gateway](#phase-4)
5. [Phase 5 — Polymorphic UI & Anti-Thrash Buffering](#phase-5)
6. [Phase 6 — Chart.js Real-Time Graph](#phase-6)
7. [Phase 7 — Multi-Attribute Metric Toggles](#phase-7)
8. [Phase 8 — Historical Data Timeline Loader](#phase-8)
9. [Phase 9 — WebSocket Auto-Reconnect & Recovery](#phase-9)
10. [Phase 10 — Full Polymorphic Multi-Sensor Expansion](#phase-10)
11. [Phase 11 — Inventory Page & Sensor HTML Pages](#phase-11)
12. [Phase 12 — Toast Notification Engine (CDN → Self-Contained)](#phase-12)
13. [Phase 13 — Threshold-Aware Monitoring & Alert UI](#phase-13)
14. [Phase 14 — Zero-Touch Auto-Discovery Pipeline](#phase-14)

---

## System Architecture Overview

Before the phases: the entire pipeline follows one invariant design principle — **every layer is decoupled and asynchronous**. No layer blocks the next.

```
mock_sensors.py  →  Redis Stream  →  stream_processor.py  →  InfluxDB
                                            ↓
                                     Redis Pub/Sub
                                            ↓
                                       main.py (FastAPI)
                                            ↓
                                    WebSocket (ws://)
                                            ↓
                                    app.js (Browser)
```

The rule engine (`rule_engine.py`) runs as a parallel consumer on the same Redis stream, firing alert payloads back into the Pub/Sub channel for the browser to receive alongside live telemetry.

---

<a name="phase-1"></a>
## Phase 1 — Local Infrastructure Setup

### What We Built
A `docker-compose.yml` defining two containerised services:
- **Redis** (`redis:alpine`) — lightweight, fast, in-memory broker
- **InfluxDB v2** (`influxdb:2.0`) — time-series database with a pre-configured bucket, org, and static admin token

### Why This Approach
Containerising both services means a single `docker compose up -d` command replicates the exact same environment on any machine. InfluxDB was auto-provisioned with environment variables (`DOCKER_INFLUXDB_INIT_*`) so no manual web-UI setup was needed — critical for repeatable onboarding.

### Problems Overcome
- **InfluxDB required a one-time manual setup by default.** Solved by using the `DOCKER_INFLUXDB_INIT_MODE=setup` environment variables to script the initial organization, bucket, and admin token directly in `docker-compose.yml`.
- **Port conflicts on Windows.** Redis binds to `6379` and InfluxDB to `8086`. We verified no system-level Redis or InfluxDB conflicted with the Docker-mapped ports.

---

<a name="phase-2"></a>
## Phase 2 — Python Hardware Mocking

### What We Built
`api/mock_sensors.py` — a Python script simulating physical IoT hardware chips. Initially stubbed 24 `sensor_id`s, later refined to 4 distinct hardware signatures:

| ID | Hardware | Attributes |
|---|---|---|
| sensor_01 | BME280 (I2C) | temperature, humidity, pressure, VPD |
| sensor_02 | AS7341 (I2C) | ambient_light, color_temp, ppfd |
| sensor_03 | SGP30 (I2C) | eco2, tvoc |
| sensor_04 | Soil Moisture (ADC) | moisture, soil_temp |

### Why This Approach
Rather than using rigid OOP classes per sensor, the script uses a **data-driven config array** + `if/elif` dispatch block. This keeps the generation logic flat and easy to extend — adding a new sensor means adding one dict to the array and one `elif` block, nothing else.

**Gaussian random-walk** (not pure random) generates realistic micro-fluctuations. Pure random would make the chart look like noise. The walk anchors to a baseline and drifts in a correlated way over time, exactly as real hardware would behave during environmental change.

### Problems Overcome
- **Pure random values looked fake.** A temperature jumping from 24°C to 17°C to 31°C in three seconds breaks the illusion of hardware. Solved with controlled random-walk: `new_val = old_val + random.uniform(-delta, +delta)`, clamped with `max(min_bound, min(max_bound, new_val))`.
- **VPD cannot be independently randomised.** VPD (Vapour Pressure Deficit) is a derived formula from temperature and relative humidity: `VPD = SVP × (1 − RH/100)`. It's calculated in real-time from the walking temperature and humidity values so it always stays physically consistent.

---

<a name="phase-3"></a>
## Phase 3 — Data Processing & InfluxDB Persistence

### What We Built
`api/stream_processor.py` — the data engine that sits between the Redis stream and everything downstream. It:
1. Reads from the Redis stream using blocking `XREAD`
2. Applies **EWMA** (Exponentially Weighted Moving Average) to smooth each metric
3. Writes raw readings to InfluxDB
4. Publishes smoothed JSON to the Redis Pub/Sub channel for the UI

### Why This Approach
**EWMA over Simple Moving Average:** EWMA gives more weight to recent readings (`alpha = 0.2`) and is `O(1)` per update — no sliding window array needed. For a 1Hz sensor stream, this keeps memory flat regardless of uptime.

**Schema-agnostic InfluxDB writes:** Instead of hardcoding field names, the processor iterates `for key, val in payload.items()` and maps every numeric value as a field under the sensor's measurement tag. This means adding a new sensor attribute requires zero changes to `stream_processor.py`.

### Problems Overcome
- **XREAD vs XREADGROUP:** We chose simple `XREAD` (no consumer groups) since there's only one stream processor replica. XREADGROUP would be needed only if we scaled to multiple workers consuming the same stream in parallel.
- **InfluxDB client blocking the async loop:** The standard `influxdb-client` is synchronous. To prevent it from blocking the Redis listener, the processor runs as a standalone process (not inside FastAPI's event loop) so blocking calls are safe.
- **Duplicate EWMA key pollution:** The raw payload contains `sensor_id` and `timestamp` keys alongside metric values. We `pop()` both before the EWMA loop so the smoothing state only tracks real numeric dimensions.

---

<a name="phase-4"></a>
## Phase 4 — FastAPI WebSocket Gateway

### What We Built
`api/main.py` — a FastAPI application that:
- Exposes `ws://localhost:8000/ws/sensors`
- Manages a pool of connected WebSocket clients via a `ConnectionManager` class
- Subscribes to the Redis Pub/Sub channel in an `asyncio` background task
- Broadcasts every incoming Redis message instantly to all connected browsers

### Why This Approach
FastAPI was chosen over a raw WebSocket library because it gives HTTP REST and WebSocket routing in one ASGI process, making it trivial to add REST endpoints later (which we did in Phase 14).

**asyncio + aioredis** rather than sync Redis: putting a synchronous `redis.pubsub.listen()` inside FastAPI's async event loop would completely block it — no new WebSocket connections could be accepted while waiting for Redis. `aioredis` uses `await` so the event loop stays free.

### Problems Overcome
- **`redis-py` blocking inside FastAPI:** Using the synchronous Redis client directly inside `async def redis_listener()` froze the entire server for all connected browsers during each Redis read. Fixed by switching to `redis.asyncio` (the async client bundled with modern `redis-py`).
- **WebSocket broadcasts to dead connections:** If a client disconnects without a clean close frame (e.g., browser tab crash), `websocket.send_text()` raises an exception. Fixed with a try/except loop that collects broken connections and removes them from the pool after each broadcast.
- **CORS rejection from browser:** Browsers refuse WebSocket connections across origins without `Access-Control-Allow-Origin`. Added `CORSMiddleware` to allow all origins in development.

---

<a name="phase-5"></a>
## Phase 5 — Polymorphic UI & Anti-Thrash Buffering

### What We Built
Rewrote the JavaScript in `app.js` to be fully polymorphic:
- **Sensor filtering:** `document.body.getAttribute('data-sensor')` identifies which hardware page is loaded, mapped to the corresponding `sensor_id`
- **Dynamic DOM injection:** Instead of hardcoded HTML metric cards, `app.js` reads the JSON keys from the first payload and generates the HTML metric boxes at runtime
- **5-second buffer:** Collects 5 readings, averages them, then repaints the large numeric DOM blocks

### Why This Approach
Without filtering, every browser tab receives payloads from all 4 sensors (the WebSocket broadcasts everything). Client-side filtering is intentional — it keeps the server dumb and the client smart, avoiding per-connection subscriptions on the server.

The **5-second averaging buffer** prevents CPU thrashing. Without it, 1 update/second per sensor × DOM repaint = 60 repaints/minute on the main thread, causing visible jank and battery drain on mobile.

### Problems Overcome
- **Chart.js Y-axis rescaling panic:** When all 4 sensor metrics (temperature in tens, pressure in thousands) rendered on the same chart, the Y-axis scale became meaningless. Solved in Phase 7 by isolating one attribute per chart line.
- **`data-sensor` attribute mismatch:** Legacy pages used model-code slugs (`bme280`) while Phase 14 uses raw IDs (`sensor_01`). Solved by building a bidirectional lookup map in `app.js` with a fallback: `typeToSensorMap[sensorType] || sensorType`.

---

<a name="phase-6"></a>
## Phase 6 — Chart.js Real-Time Graph

### What We Built
Integrated Chart.js into each sensor dashboard:
- A `<canvas>` element fills the data-feed column
- `initChart(keys)` builds one dataset per sensor attribute, all hidden except the first
- Every WebSocket message appends a new data point and calls `chart.update('none')` (skips animation for real-time performance)
- A sliding window (`maxDataPoints`) pops the oldest label/data when the array exceeds the selected time horizon

### Why This Approach
`chart.update('none')` is critical — the default animation mode triggers easing recalculations for every data point on every update, which at 1Hz causes observable CPU spikes. The `'none'` flag bypasses animation entirely for live data while still supporting animated transitions when switching time horizons.

### Problems Overcome
- **Chart canvas not found at init time:** `initChart()` was being called before the `<canvas>` element was rendered. Fixed by calling it lazily on the first message (only after the DOM injection from Phase 5 has created the grid).
- **Memory growth on long sessions:** Without a `shift()` on the labels array, the chart would hold every data point forever. For a 24-hour view at 1Hz, that's 86,400 data points — enough to freeze the tab. Fixed with `maxDataPoints` trimming.
- **Date/time axis formatting:** Chart.js's time axis requires the `chartjs-adapter-date-fns` plugin for proper date parsing. Without it, all x-axis labels rendered as `NaN`. Added the adapter CDN link to all HTML pages.

---

<a name="phase-7"></a>
## Phase 7 — Multi-Attribute Metric Toggles

### What We Built
Dynamic toggle buttons above the chart generated from JSON payload keys:
- Clicking `TEMPERATURE` hides all other datasets and forces Y-axis to rescale to temperature's range
- The active button gets a highlighted border
- Time-horizon buttons (1M, 5M, 30M, 1H, 6H, 1D) switch between historical load and live-only modes

### Why This Approach
Because different sensor attributes have completely different numerical ranges (temperature: 19–25°C vs pressure: 1000–1020 hPa vs ppfd: 400–800 μmol), plotting them on one shared Y-axis destroys readability. Isolating to one attribute at a time lets Chart.js auto-scale perfectly.

### Problems Overcome
- **Toggles generated before first data arrived:** The toggle buttons were initially rendered at page load, but we had no key names yet. Fixed by deferring toggle creation to the first WebSocket message that contains actual data keys.
- **Preferred UI ordering broken by JSON key order:** InfluxDB returns historical data keys in alphabetical order (`ambient_light`, `color_temp`, `ppfd`) but we wanted a logical human order (matching physical measurement groups). Solved with a `PREFERRED_UI_ORDER` array and a custom sort function that stably reorders keys before rendering.

---

<a name="phase-8"></a>
## Phase 8 — Historical Data Timeline Loader

### What We Built
A `GET /api/history/{sensor_id}` endpoint in `main.py` that queries InfluxDB using Flux query language and returns time-bucketed historical data. The frontend calls this on page load (and on time-horizon button clicks) to pre-populate the chart before live data arrives.

### Why This Approach
Without historical pre-load, every page refresh shows an empty chart that starts from the current second. The user would always see only the most recent 60 data points (1 minute). Loading history gives immediate context — you can see the trend of the last 6 hours the moment the page loads.

**Flux query with `aggregateWindow`:** InfluxDB's Flux language aggregates raw seconds-resolution data into sensible buckets (e.g., 1-minute averages for the 6H view) so we're not sending 21,600 raw rows to the browser for a 6-hour graph.

### Problems Overcome
- **InfluxDB Flux query syntax is non-trivial:** Flux uses a chained pipe-forward syntax (`|> filter() |> aggregateWindow()`) that is very different from SQL. Early queries returned empty results because of incorrect `measurement` field names and missing `_field` filters.
- **Historical rows arriving in wrong order:** InfluxDB doesn't guarantee time-ascending order without `|> sort(columns: ["_time"])`. Randomly-ordered rows caused the chart to zig-zag incorrectly.
- **Merging historical + live data:** When the historical load completed and live WebSocket messages started arriving, there was a timestamp gap (the few seconds of load time). Fixed by tracking the last historical timestamp and only appending live points with newer timestamps.

---

<a name="phase-9"></a>
## Phase 9 — WebSocket Auto-Reconnect & Recovery

### What We Built
Robust connection lifecycle management in `app.js`:
- `ws.onclose` triggers `setTimeout(connect, 2000)` for automatic reconnection
- `ws.onerror` closes the socket to trigger `onclose`
- The connection status badge (`Connected` / `Reconnecting...`) updates on every state change
- The `pulseDot` animation only plays while the connection is active

### Why This Approach
Real-world networks drop. A developer leaving the laptop for 15 minutes may return to a stale tab showing frozen data from before the sleep. Auto-reconnect ensures the UI self-heals without a manual page reload.

### Problems Overcome
- **Reconnect storm:** Without an exponential backoff, a network outage causes the browser to hammer the server with thousands of reconnect attempts per second. The 2-second fixed delay was a pragmatic choice for a local dev environment (a production build would use exponential backoff with jitter).
- **Ghost TimeoutIntervals surviving reconnect:** The `activeTimeout` variable that marks the sensor as "Offline" after 4 seconds of silence was not being cleared on reconnect, causing the sensor to immediately flash offline on reconnect. Fixed by clearing `activeTimeout` inside `ws.onopen`.

---

<a name="phase-10"></a>
## Phase 10 — Full Polymorphic Multi-Sensor Expansion

### What We Built
Refactored `mock_sensors.py` from 24 generic sensors to 4 distinct hardware signatures with realistic physical properties. Added a units map in `app.js` (`°C`, `%`, `hPa`, `kPa`, `lx`, `K`, `μmol`, `ppm`, `ppb`) so metric cards display correct SI labels without hardcoding.

### Why This Approach
24 identical sensors with different IDs is not realistic and makes it impossible to test heterogeneous hardware. Each real chip (BME280, AS7341, SGP30, Soil ADC) has a completely different register map and output schema. Simulating this correctly validates that the pipeline is truly schema-agnostic.

### Problems Overcome
- **EWMA state pollution between sensors:** The `ewma_state` dictionary in `stream_processor.py` was initially keyed only by `metric_name`. When two sensors both reported `temperature`, their EWMA state was shared and corrupted. Fixed by keying as `f"{sensor_id}_{key}"` (composite key).
- **InfluxDB tag cardinality:** Using `sensor_id` as an InfluxDB tag (high-cardinality string index) was initially rejected by performance advisors in favour of a numeric tag. However, for 4 sensors the cardinality is negligible, and string IDs make Flux queries human-readable.

---

<a name="phase-11"></a>
## Phase 11 — Inventory Page & Sensor HTML Pages

### What We Built
- `simulator/index.html` — an inventory grid listing all hardware with clickable tiles linking to individual sensor pages
- `simulator/bme280.html`, `as7341.html`, `sgp30.html`, `soil.html` — per-sensor dashboard pages using a shared `app.js` and `style.css`
- Each page uses `data-sensor="bme280"` on the `<body>` to signal to `app.js` which sensor to subscribe to

### Why This Approach
Separate HTML files per sensor mirror real-world product dashboards (one page per device). A shared `app.js` with a `data-sensor` discrimination attribute means all 4 pages run identical logic — no page-specific code duplication.

### Problems Overcome
- **Hardcoded sensor count:** Every time a sensor was added, a new HTML file had to be created AND a new tile added to `index.html`. This manual process was the main motivation for Phase 14 (auto-discovery).
- **`app.js` loading on `index.html` without a sensor target:** `app.js` would call `loadHistoricalData()` on the index page where there's no chart canvas, causing null reference errors. Fixed with an early `if (sensorType === 'index') return;` guard at the top of the data-loading path.

---

<a name="phase-12"></a>
## Phase 12 — Toast Notification Engine (CDN → Self-Contained)

### What We Built
A completely self-contained CSS + JS toast notification system embedded directly in `app.js`. Features:
- Sliding entry animation from the top-right
- 6-second animated progress bar countdown
- Full-height right-side dismiss zone (52px) with hover and pressed visual states
- Two-line message format: warning text + safe range on a new line
- Alert de-duplication: toasts stack without overlapping via incremental `top` offset

### Why This Approach (and the CDN Failure Story)
The original plan was to use `vue3-toastify` via CDN. This is where a significant challenge emerged.

`vue3-toastify` is a **Vue 3 plugin** — it is not designed to run standalone in a vanilla HTML page without a Vue application instance. The CDN build of `vue3-toastify@0.2.9` exposed a UMD module, but calling `Vue3Toastify.toast(...)` without a mounted Vue app produced silent runtime errors — no error in the console, no toast rendered.

Multiple approaches were attempted:
1. **Direct CDN UMD call** — failed silently (no Vue app to inject into)
2. **Creating a stub Vue app** — `Vue.createApp({}).use(Vue3Toastify).mount('#app')` — triggered CORS errors downloading icon assets from `unpkg.com`
3. **Switching to `toastify-js`** (a different library with no Vue dependency) — the CSS CDN was reachable but the JS module had no browser-compatible UMD export
4. **Downloading and bundling** — impractical without a build system

**Decision:** Abandon all CDN dependencies entirely and write a zero-dependency toast engine from scratch inside `app.js`. This is the most reliable approach in a build-tool-free environment and gives us full control over styling and behaviour.

### Problems Overcome
- **CDN CORS on `unpkg.com`:** The library loaded stylesheets that fetched icon fonts from a second origin. Browser blocked these as CORS violations.
- **`position: absolute` dismiss zone not full-height:** When the toast message wrapped to multiple lines, the dismiss zone (a `div` on the right) didn't stretch to match. Fixed by making the toast body `display: flex; align-items: stretch` and the dismiss zone `position: absolute; top: 0; right: 0; height: 100%; width: 52px`.
- **`\n` not rendering as line breaks in the DOM:** The alert message from `rule_engine.py` uses `\n` as a separator for the two-line format. In raw `textContent`, `\n` renders as a space. Fixed with `white-space: pre-line` CSS and `.replace(/\n/g, '<br>')` before injecting as `innerHTML`.

---

<a name="phase-13"></a>
## Phase 13 — Threshold-Aware Monitoring & Alert UI

### What We Built
A mathematically rigorous threshold monitoring system spanning backend and frontend:

**Backend (`rule_engine.py`):**
- Runs as a standalone process consuming the Redis stream
- Defines `THRESHOLDS` dict for all 11 sensor attributes with `{min, max}` bounds
- Evaluates every incoming payload with a schema-agnostic loop: `for key, val in payload.items(): if key in THRESHOLDS`
- Fires a structured alert JSON to the Redis Pub/Sub channel when a breach is detected
- Enforces a per-(sensor, attribute) cooldown (`ALERT_COOLDOWN`) to prevent alert spam

**Frontend (`app.js`):**
- Alert payloads are intercepted in `handleMessage()` before normal sensor processing
- `showToast()` is called unconditionally — alerts appear on any open page, not just the breaching sensor's dashboard
- Chart lines turn red when the latest value exceeds the threshold; green when safe
- Individual data point dots are colored independently: each dot reflects only its own value, not a global state

### Why This Approach
**Schema-agnostic threshold evaluation** is the key design principle. The rule engine doesn't know which sensor is which — it just checks if a metric key is in its dictionary. Adding a new sensor attribute only requires adding one line to `THRESHOLDS` in two files (`rule_engine.py` and `app.js`).

**Rule engine as a separate process** (not inside FastAPI) ensures that a slow or crashing rule evaluation never affects the WebSocket gateway's ability to serve live data.

### Problems Overcome
- **`vue3-toastify` CDN failure (see Phase 12):** The toast notification system required a full rebuild from scratch.
- **1-hour cooldown too long for testing:** An initial test session can't wait 60 minutes to see if all 4 sensors fire alerts. Solved by making `ALERT_COOLDOWN` a named constant with a comment marking the test value (30s) vs production value (3600s).
- **Sensors 03 and 04 never triggered alerts:** The SGP30 eco2 baseline was set to 400 (exactly equal to the threshold minimum). `val < 400` is `False` when `val == 400`, so no alert fired. The soil sensor's moisture and soil_temp baselines were safely mid-range. Fixed by adjusting baselines to realistically "stressed" values that naturally drift in and out of the safe zone.
- **HELLO packets reaching rule engine:** The rule engine iterated all payload keys. HELLO packets contain `type`, `sensor_id`, `model`, `display_name`, `bus`, `capabilities` — none of which are in `THRESHOLDS`, so no harm was done. However, to be explicit and efficient, an early `continue` guard was added: `if payload.get('type') == 'HELLO': continue`.

---

<a name="phase-14"></a>
## Phase 14 — Zero-Touch Auto-Discovery Pipeline

### What We Built
A complete architectural shift from hardcoded HTML to a plug-and-play registration system. Four layers:

**Layer 1 — Hardware Boot Handshake (`mock_sensors.py`):**
Before the data loop begins, each sensor emits one `HELLO` packet to the Redis stream:
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

**Layer 2 — Registry & API (`stream_processor.py` + `main.py`):**
- `stream_processor.py` intercepts HELLO packets (detected by `payload.get('type') == 'HELLO'`), writes them to a Redis Hash (`rala:sensors:registry`), and skips EWMA/InfluxDB entirely for these packets
- Two new REST endpoints in `main.py`:
  - `GET /api/inventory` → returns all sensors from the Redis hash
  - `GET /api/sensor-config/{sensor_id}` → returns one sensor's metadata

**Layer 3 — Dynamic Frontend:**
- `index.html` calls `fetch('/api/inventory')` at page load and renders tiles dynamically via JavaScript DOM creation
- `dashboard.html` (new, universal) reads `?id=sensor_01` from the URL, fetches `/api/sensor-config/sensor_01`, sets the page title/subtitle/model label from the registry, then loads `app.js`
- `app.js` extended with a module-level `expectedSensorId` that handles both legacy slug routing (`bme280` → `sensor_01`) and direct ID routing (`sensor_01` → `sensor_01`)

### Why This Approach
**The core problem with Phase 11:** Every new sensor required:
1. Writing a new Python data generator block
2. Creating a new HTML file
3. Adding a new tile to `index.html`
4. Restarting the frontend server

Steps 2–4 were pure maintenance overhead with no engineering value. The HELLO protocol eliminates them. A new sensor is added by modifying only `mock_sensors.py` — the rest of the system discovers it on next restart.

**Redis Hash for the registry** (vs. a database table): The registry is small (≤ tens of sensors), read-frequently, and needs to survive restarts (Redis is persistent via AOF). `HSET` and `HGETALL` on a Redis hash are O(1) and O(N) respectively — perfect for the inventory endpoint.

### Problems Overcome
- **Critical: local variable shadowing module-level `expectedSensorId`:** In `handleMessage()` inside `app.js`, a local variable was declared:
  ```javascript
  const expectedSensorId = typeToSensorMap[sensorType]; // local shadow!
  ```
  When `dashboard.html` sets `data-sensor="sensor_01"`, `typeToSensorMap['sensor_01']` returns `undefined` (the map keys are `'bme280'`, not `'sensor_01'`). So `undefined !== 'sensor_01'` was always `true`, causing every single WebSocket message to be silently dropped. The chart appeared to update (from historical pre-load), the metrics showed values, but the live feed log was empty and the status stuck on `Waiting`. Fixed by removing the local shadow and using the module-level `expectedSensorId` which has the `|| sensorType` fallback.

- **Script load order race condition in `index.html`:** The inline `buildInventory()` async function called `registerIndexBox(id)` to wire dynamic tile IDs into `app.js`'s `indexBoxes` lookup object. But `app.js` was loaded *after* the inline script via a `<script src="app.js">` tag at the bottom of `<body>`. Since `buildInventory()` is async, its `fetch()` resolves after the synchronous `<script>` execution order completes — but `registerIndexBox` might still be undefined at that point if the load order is wrong. Fixed by moving `<script src="app.js">` *before* the inline script so the function is guaranteed to exist when the fetch resolves.

- **`onload` timing on async inventory fetch:** An intermediate attempt used `<script src="app.js" onload="...">` to call `registerIndexBox`. This `onload` fires synchronously after the script parses, before `buildInventory()`'s `fetch()` resolves. So `_raalaSensorIds` was still empty when `onload` ran. The final fix (script order swap) made this entire mechanism unnecessary.

- **HELLO packet `capabilities` serialisation:** Redis Hash values must be strings. `capabilities` is a Python list (`["temperature", "humidity"]`). If stored directly, Redis silently coerces it to its `repr()` string (`"['temperature', 'humidity']"`) which breaks JSON parsing on the frontend. Fixed by `json.dumps(capabilities)` on write and `json.loads(capabilities)` on read in both the FastAPI endpoint and the `buildInventory()` frontend fetch.

- **Git committed the entire `venv/` directory:** When pushing the Phase 13/14 work, the absence of a Python section in `.gitignore` caused `api/venv/` (4,268 files, ~15MB) to be staged and committed. GitHub's remote hung up mid-push (`send-pack: unexpected disconnect`). Fixed by: running `git rm -r --cached api/venv`, adding `venv/`, `__pycache__/`, `*.pyc` to `.gitignore`, amending the commit, and force-pushing with `--force-with-lease`.

---

## Summary Table

| Phase | Primary File(s) Changed | Core Problem Solved |
|---|---|---|
| 1 | `docker-compose.yml` | Reproducible database infrastructure with zero manual setup |
| 2 | `mock_sensors.py` | Realistic hardware simulation with correlated random-walk drift |
| 3 | `stream_processor.py` | Noise smoothing (EWMA) + decoupled buffered persistence |
| 4 | `main.py` | Non-blocking async WebSocket broadcast without freezing the server |
| 5 | `app.js` | Per-sensor client-side filtering + 5s buffer to prevent DOM thrashing |
| 6 | `app.js`, HTML templates | Real-time Chart.js graph with sliding memory window |
| 7 | `app.js` | Per-attribute Y-axis isolation for mixed-range sensor metrics |
| 8 | `main.py`, `app.js` | Historical timeline pre-load from InfluxDB on page open |
| 9 | `app.js` | Auto-reconnect with clean state reset on connection drop |
| 10 | `mock_sensors.py`, `stream_processor.py` | True polymorphic multi-sensor expansion with EWMA composite keying |
| 11 | `index.html`, per-sensor `.html` | Inventory UI + per-sensor dashboard pages sharing one `app.js` |
| 12 | `app.js` | Zero-dependency self-contained toast engine replacing broken CDN libraries |
| 13 | `rule_engine.py`, `app.js` | Threshold breach detection, per-attribute alert cooldown, red/green chart coloring |
| 14 | All files + `dashboard.html` | HELLO handshake, Redis registry, REST inventory API, dynamic UI with zero hardcoded sensor HTML |
