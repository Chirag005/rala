# RAALA Polymorphic Sensor Architecture

This document dictates the design pattern used to make the RAALA simulation pipeline infinitely scalable using **Zero-Config Polymorphism**.

## The Problem
Historically, adding a single new sensor to an IoT dashboard required massive code duplication:
1. Hard-coding the new attributes (e.g. `ph_level`) into the Python message broker.
2. Rewriting the Stream Processing engine to avoid crashing when it saw a new key.
3. Writing explicit `<div id="val-ph-level">` HTML blocks into the frontend templates.

## The Solution: JSON-Driven DOM Generation

RAALA reverses this paradigm. Neither the backend pipelines nor the frontend HTML templates know or care about what a physical sensor does. 

### 1. The Hardware Signature Generator (`mock_sensors.py`)
Each distinct `sensor_id` is assigned a distinct dictionary schema. For instance:
- `sensor_bme280`: outputs `{"temperature": 24, "humidity": 60, "pressure": 1013, "vpd": 0.5}`
- `sensor_as7341`: outputs `{"ambient_light": 1500, "color_temp": 5000, "ppfd": 600}`

### 2. The Agnostic Stream Processor (`stream_processor.py`)
Because it no longer hard-codes processing strings (like `"temperature"`), the script simply loops through `payload.items()`. It blindly executes the Exponentially Weighted Moving Average (EWMA) to mathematically suppress hardware noise, and writes natively to InfluxDB using the raw JSON keys as column headers.

### 3. Native UI Rendering (`app.js`)
The `bme280.html` and other pages contain absolutely no metric blocks. They contain only an empty wrapper:
```html
<div class="metrics-grid" id="dynamicMetricsGrid"></div>
```
When `app.js` detects the first stream payload, it extracts the JSON keys (e.g., `["ambient_light", "ppfd"]`). It formats them visually to `"AMBIENT LIGHT"` and injects native `<div class="metric">` blocks dynamically into the DOM tree. 

### How to Add Future Sensors
If you install an Arduino running a completely unrecognizable Soil Acid Sensor:
1. Ensure the chip spits out a JSON string to Redis `rala:sensors:stream`: `{"ph_level": 5.5, "acidity": 1.2}`
2. Open the webpage. 
3. *That's it.*

The RAALA pipeline will autonomously intercept the JSON keys, mathematically smooth the variations, write the new columns into the database, draw two new tabs on your graph, and dynamically inject two new visual statistic boxes onto the sidebar. Zero code modifications required.
