# RAALA Sensor Simulator Architecture
### High-Level System Design & Pipeline Flow

The RAALA Simulator is a highly scalable, decoupled microservice architecture designed to mimic a massive real-time IoT agricultural greenhouse. It guarantees zero data-loss through persistent streams, suppresses physical hardware noise using mathematical smoothing, and delivers real-time telemetry to the browser over persistent TCP sockets.

---

## Complete Data Flow Architecture
```mermaid
graph TD
    subgraph "1. Hardware Layer (mock_sensors.py)"
        S1["Sensor 01 (BME280)<br/>Temp, Humidity, VPD, Pressure"]
        S2["Sensor 02 (AS7341)<br/>Lux, Color Temp, PPFD"]
        S3["Sensor 03 (SGP30)<br/>eCO2, TVOC"]
        S4["Sensor 04 (Soil)<br/>Moisture, Soil Temp"]
    end

    subgraph "2. Message Broker (Redis Core)"
        R_Stream[("Redis Stream<br/>(rala:sensors:stream)")]
        R_PubSub(("Redis Pub/Sub<br/>(rala:sensors:ui)"))
    end

    subgraph "3. Data Engine (stream_processor.py)"
        EWMA["Exponentially Weighted<br/>Moving Average (EWMA)"]
        InfluxWriter["Dynamically loops JSON items"]
    end
    
    subgraph "4. Time Series Database"
        InfluxDB[("InfluxDB (Port 8086)<br/>Bucket: RAALA")]
    end

    subgraph "5. Real-Time Gateway (FastAPI)"
        WS_Manager{"WebSocket Manager<br/>(main.py)"}
    end

    subgraph "6. Polymorphic Browser UI (app.js)"
        Polymorph["JSON Keys Extractor<br/>(Auto DOM HTML Injection)"]
        Buffer["5-Sec DOM Metric Buffer<br/>(Visual Text UI Math)"]
        ChartJS["Chart.js Render Engine<br/>(Splices historical arrays)"]
    end

    %% Flow Paths
    S1 & S2 & S3 & S4 -- "JSON payload<br/>(1.0s interval)" --> R_Stream
    
    R_Stream -- "xread blocking loop" --> EWMA
    EWMA -- "Raw data mapping" --> InfluxWriter
    InfluxWriter -- "WritePrecision.NS" --> InfluxDB
    EWMA -- "Mathematically Smoothed JSON" --> R_PubSub
    
    R_PubSub -- "Async Task Listener" --> WS_Manager
    WS_Manager -- "TCP: ws://.../ws/sensors" --> Polymorph
    
    Polymorph -- "Calculates averages" --> Buffer
    Polymorph -- "Appends Data Points" --> ChartJS

    %% Styling
    classDef hardware fill:#1e293b,stroke:#0f172a,stroke-width:2px,color:#fff;
    classDef redis fill:#991b1b,stroke:#7f1d1d,stroke-width:2px,color:#fff;
    classDef engine fill:#075985,stroke:#0c4a6e,stroke-width:2px,color:#fff;
    classDef db fill:#5b21b6,stroke:#4c1d95,stroke-width:2px,color:#fff;
    classDef web fill:#047857,stroke:#065f46,stroke-width:2px,color:#fff;
    classDef frontend fill:#b45309,stroke:#92400e,stroke-width:2px,color:#fff;

    class S1,S2,S3,S4 hardware;
    class R_Stream,R_PubSub redis;
    class EWMA,InfluxWriter engine;
    class InfluxDB db;
    class WS_Manager web;
    class Polymorph,Buffer,ChartJS frontend;
```

---

## 1. The Mock Hardware Layer (`mock_sensors.py`)
**Role:** Simulates the physical hardware chips (I2C/Analog) attached to Raspberry Pi/Arduino microcontrollers in the greenhouse.
- **Polymorphic Generation:** It does not use rigid classes. Instead, it generates distinct JSON dictionaries representing unique hardware signatures (e.g., Adafruit BME280 generates `temperature/humidity/pressure/vpd`, while the AS7341 generates `lux/color_temp/ppfd`).
- **Data Drift Mechanics:** Uses Gaussian noise and controlled random-walk algorithms anchored to a baseline to simulate authentic environmental micro-fluctuations over time.
- **Egress:** Pushes raw payloads into a high-throughput **Redis Stream** (`rala:sensors:stream`) every 1.0 seconds.

## 2. The Message Broker (Redis)
**Role:** The universal nervous system connecting the hardware to the database and the web server.
- **Streams (Persistence):** Acts as a durable buffer. If the database crashes, the hardware data queue backs up in the Redis Stream securely until the DB comes back online.
- **Pub/Sub (Fire-and-Forget):** Once data is cleaned by the stream processor, it is blasted to all active web clients through a lightning-fast memory channel (`rala:sensors:ui`).

## 3. The Data Engine (`stream_processor.py`)
**Role:** The intermediary logic gate connecting raw data to the database and the front-end servers.
- **Schema-Agnostic Processing:** It intercepts the polymorphic JSON. Rather than hard-coding column names, it iterates natively over arbitrary keys.
- **EWMA Mathematical Smoothing:** Applies an Exponentially Weighted Moving Average (`alpha=0.2`) to all numeric values. This flattens out erratic voltage spikes typical of cheap hardware sensors before it reaches the UI.
- **InfluxDB Archiving:** Writes the cleaned time-series data into the persistent InfluxDB bucket.
- **Egress:** Publishes the smoothed JSON object out to the Redis Pub/Sub channel.

## 4. The Real-Time Gateway (FastAPI)
**Role:** A massive concurrency router handling thousands of incoming browser connections.
- **Async WebSockets:** Upgrades standard HTTP connections to persistent two-way TCP lines via `ws://.../ws/sensors`.
- **Redis Listener Thread:** Spawns an asynchronous background task (`asyncio.create_task`) that continuously listens to the Redis Pub/Sub channel. Whenever a smoothed payload arrives, the FastAPI server instantly broadcasts it to every single connected browser.

## 5. The Polymorphic Client (`app.js`)
**Role:** The dynamic browser rendering engine.
- **Zero-Config DOM Injection:** When `app.js` connects via WebSocket, it intercepts the JSON payload. Instead of looking for hard-coded HTML layout grids, it reads the JSON keys, maps them to physical SI units (`°C`, `ppm`, `lx`), and dynamically constructs the HTML metric tracking cards via Javascript Injection.
- **Memory Scaling:** Maintains a 5-second `dataBuffer` to prevent CPU-thrashing DOM updates, meaning the heavy Chart.js graphics render at 1 frame-per-second, but the actual HTML numerical stat blocks only repaint their calculated average once every 5 seconds.
- **Dynamic Chart Slicing:** Manages massive dataset horizons (`maxDataPoints`) natively, allowing the user to toggle between 1-Minute and 24-Hour timelines by truncating internal JavaScript arrays on the fly to prevent browser memory leaks.
