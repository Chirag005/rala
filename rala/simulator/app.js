// Multi-sensor App JS
const WS_URL = "ws://localhost:8000/ws/sensors";
const badge = document.getElementById("connectionBadge");
const badgeText = document.getElementById("connectionText");

// ============================================================
// SELF-CONTAINED TOAST ENGINE (no external CDN dependency)
// ============================================================
(function() {
    const STYLE = `
        #raala-toast-container {
            position: fixed; top: 20px; right: 20px; z-index: 99999;
            display: flex; flex-direction: column; gap: 10px;
            pointer-events: none;
        }
        .raala-toast {
            min-width: 320px; max-width: 480px;
            border-radius: 10px; overflow: hidden;
            font-family: 'Inter', sans-serif; font-size: 13px; font-weight: 500;
            color: #fff; line-height: 1.5;
            backdrop-filter: blur(12px);
            box-shadow: 0 8px 32px rgba(0,0,0,0.45);
            pointer-events: all;
            animation: raala-slide-in 0.3s ease;
            transition: opacity 0.4s ease, transform 0.4s ease;
        }
        .raala-toast { position: relative; }
        .raala-toast-body {
            display: flex; align-items: center;
            padding: 13px 68px 13px 16px; gap: 10px;
        }
        .raala-toast-msg { flex: 1; white-space: pre-line; }
        .raala-toast-icon { font-size: 15px; flex-shrink: 0; }
        /* Dismiss zone: absolutely covers the full right strip */
        .raala-toast-dismiss-zone {
            position: absolute; top: 0; right: 0; bottom: 0; width: 56px;
            display: flex; align-items: center; justify-content: center;
            cursor: pointer;
            border-left: 1px solid rgba(255,255,255,0.08);
            transition: background 0.2s;
            z-index: 1;
        }
        .raala-toast-dismiss-zone:hover { background: rgba(255,255,255,0.1); }
        .raala-toast-dismiss-zone:hover .raala-toast-close {
            background: rgba(255,255,255,0.18); color: #fff;
        }
        .raala-toast-dismiss-zone:active .raala-toast-close {
            transform: scale(0.85); background: rgba(255,255,255,0.28);
        }
        .raala-toast-close {
            width: 24px; height: 24px;
            display: flex; align-items: center; justify-content: center;
            border-radius: 50%; border: none; background: transparent;
            color: rgba(255,255,255,0.55); font-size: 16px; line-height: 1;
            pointer-events: none; /* clicks handled by dismiss-zone */
            transition: background 0.2s, color 0.2s, transform 0.1s;
        }
        .raala-toast-progress {
            height: 3px; width: 100%;
            background: rgba(255,255,255,0.12);
            position: relative;
        }
        .raala-toast-progress-bar {
            height: 100%; width: 100%;
            transform-origin: left;
            animation: raala-shrink linear forwards;
        }
        .raala-toast.error  { background: rgba(239,68,68,0.18);  border: 1px solid rgba(239,68,68,0.55); }
        .raala-toast.warning{ background: rgba(251,146,60,0.18); border: 1px solid rgba(251,146,60,0.55); }
        .raala-toast.info   { background: rgba(56,189,248,0.18); border: 1px solid rgba(56,189,248,0.55); }
        .raala-toast.success{ background: rgba(52,211,153,0.18); border: 1px solid rgba(52,211,153,0.55); }
        .raala-toast.error   .raala-toast-progress-bar { background: rgba(239,68,68,0.8); }
        .raala-toast.warning .raala-toast-progress-bar { background: rgba(251,146,60,0.8); }
        .raala-toast.info    .raala-toast-progress-bar { background: rgba(56,189,248,0.8); }
        .raala-toast.success .raala-toast-progress-bar { background: rgba(52,211,153,0.8); }
        @keyframes raala-slide-in {
            from { opacity: 0; transform: translateX(60px); }
            to   { opacity: 1; transform: translateX(0); }
        }
        @keyframes raala-shrink {
            from { transform: scaleX(1); }
            to   { transform: scaleX(0); }
        }
    `;
    const styleEl = document.createElement('style');
    styleEl.textContent = STYLE;
    document.head.appendChild(styleEl);

    const container = document.createElement('div');
    container.id = 'raala-toast-container';
    document.body.appendChild(container);

    const ICONS = { error: '🔴', warning: '🟠', info: '🔵', success: '🟢' };

    window.showToast = function(message, type = 'info', duration = 6000) {
        const toast = document.createElement('div');
        toast.className = `raala-toast ${type}`;

        // Body: icon + message + close button
        const body = document.createElement('div');
        body.className = 'raala-toast-body';
        body.innerHTML = `
            <span class="raala-toast-icon">${ICONS[type] || '🔔'}</span>
            <span class="raala-toast-msg" style="align-self:center">${message.replace(/\n/g, '<br>')}</span>
        `;

        // Build the dismiss zone (full-height right strip)
        const dismissZone = document.createElement('div');
        dismissZone.className = 'raala-toast-dismiss-zone';

        const closeBtn = document.createElement('button');
        closeBtn.className = 'raala-toast-close';
        closeBtn.innerHTML = '&times;';
        closeBtn.title = 'Dismiss';
        dismissZone.appendChild(closeBtn);
        body.appendChild(dismissZone);

        // Progress bar
        const progress = document.createElement('div');
        progress.className = 'raala-toast-progress';
        const bar = document.createElement('div');
        bar.className = 'raala-toast-progress-bar';
        bar.style.animationDuration = `${duration}ms`;
        progress.appendChild(bar);

        toast.appendChild(body);
        toast.appendChild(progress);
        container.appendChild(toast);

        // Dismiss helper
        const dismiss = () => {
            toast.style.opacity = '0';
            toast.style.transform = 'translateX(60px)';
            setTimeout(() => toast.remove(), 400);
        };

        closeBtn.addEventListener('click', dismiss);
        const timer = setTimeout(dismiss, duration);

        // The entire dismiss zone (not just the button) fires dismiss + clears timer
        dismissZone.addEventListener('click', () => { clearTimeout(timer); dismiss(); });
    };
})();


// Global aesthetic UI ordering to prevent InfluxDB Alphabetical scrambling
const PREFERRED_UI_ORDER = ['temperature', 'humidity', 'pressure', 'vpd', 'ambient_light', 'color_temp', 'ppfd', 'eco2', 'tvoc', 'moisture', 'soil_temp'];

// Phase 13: Mathematical Crop Definitions
const THRESHOLDS = {
    temperature: { min: 19, max: 22 },
    humidity: { min: 40, max: 60 },
    pressure: { min: 1000, max: 1020 },
    vpd: { min: 0.8, max: 1.2 },
    ambient_light: { min: 2000, max: 4000 },
    color_temp: { min: 4000, max: 6000 },
    ppfd: { min: 400, max: 800 },
    eco2: { min: 400, max: 800 },
    tvoc: { min: 0, max: 100 },
    moisture: { min: 30, max: 60 },
    soil_temp: { min: 15, max: 22 }
};

function sortDataKeys(keys) {
    return keys.sort((a, b) => {
        let indexA = PREFERRED_UI_ORDER.indexOf(a);
        let indexB = PREFERRED_UI_ORDER.indexOf(b);
        if (indexA === -1) indexA = 999;
        if (indexB === -1) indexB = 999;
        return indexA - indexB;
    });
}

// Phase 13: Mathematical Chart Canvas Manipulation
function updateChartColors(chart) {
    chart.data.datasets.forEach((ds) => {
        const key = ds.label.toLowerCase().replace(' ', '_');
        const t = THRESHOLDS[key];
        
        if (t && ds.data.length > 0) {
            // Evaluates specifically the LATEST chronological record mapped onto the grid
            const latestVal = ds.data[ds.data.length - 1];
            const hasRisk = (latestVal < t.min || latestVal > t.max);
            
            if (hasRisk) {
                // Synthesize faint red fill graph background and solid red border line
                ds.backgroundColor = 'rgba(239, 68, 68, 0.15)'; 
                ds.borderColor = 'rgba(239, 68, 68, 1)'; 
            } else {
                // Synthesize the classic green optimal zone colors
                ds.backgroundColor = 'rgba(16, 185, 129, 0.1)'; 
                ds.borderColor = 'rgba(16, 185, 129, 1)'; 
            }
            
            // Map the individual scatter dots point-by-point to reflect their own isolated mathematical truth inside the array
            const pointColors = ds.data.map(val => (val < t.min || val > t.max) ? 'rgba(239, 68, 68, 1)' : 'rgba(16, 185, 129, 1)');
            ds.pointBackgroundColor = pointColors;
            ds.pointBorderColor = pointColors;
        }
    });
}

// Determine which sensor page we are on based on the data-sensor attribute of the body
// Supports two modes:
//   Legacy:    data-sensor="bme280"    (individual HTML pages)
//   Phase 14:  data-sensor="sensor_01" (universal dashboard.html)
const sensorType = document.body.getAttribute('data-sensor');

const typeToSensorMap = {
    'bme280': 'sensor_01',
    'as7341': 'sensor_02',
    'sgp30': 'sensor_03',
    'soil': 'sensor_04'
};

// Reverse map to resolve raw sensor_id inputs from dashboard.html
const sensorIdToType = Object.fromEntries(Object.entries(typeToSensorMap).map(([k,v]) => [v, k]));

// Normalise: if data-sensor is already a raw sensor_id (e.g. 'sensor_01'), resolve both directions
const expectedSensorId = typeToSensorMap[sensorType] || sensorType;  // 'bme280'→'sensor_01' OR 'sensor_01'→'sensor_01'

console.log(`Attempting to connect to ${WS_URL}...`);
let ws;

function connect() {
    ws = new WebSocket(WS_URL);

    ws.onopen = () => {
        console.log("Connected to FastAPI WebSocket");
        if(badge) {
            badge.classList.add("connected");
            badgeText.innerText = "Connected";
        }
        if (sensorType !== 'index') {
            appendLog("SYSTEM", `Subscribed to WebSocket stream`);
        }
    };

    ws.onclose = () => {
        if(badge) {
            badge.classList.remove("connected");
            badgeText.innerText = "Reconnecting...";
        }
        setTimeout(connect, 2000);
    };

    ws.onerror = (err) => {
        console.error("WebSocket encountered error: ", err.message, "Closing socket");
        ws.close();
    };

    ws.onmessage = (event) => {
        handleMessage(event.data);
    };
}

const horizons = { "1M": 60, "5M": 300, "30M": 1800, "1H": 3600, "6H": 21600, "1D": 86400 };

async function loadHistoricalData(horizon, initialLoad = false) {
    if (sensorType === 'index' || sensorType === 'loading') {
        if (initialLoad) connect();
        return;
    }
    // Use the module-level expectedSensorId (handles both legacy and Phase 14 routing)
    if (!expectedSensorId || expectedSensorId === 'loading') {
        if (initialLoad) connect();
        return;
    }
    
    try {
        if (badgeText && initialLoad) badgeText.innerText = "Loading Horizon...";
        const res = await fetch(`http://localhost:8000/api/history/${expectedSensorId}?horizon=${horizon}`);
        const historyData = await res.json();
        
        if (historyData && historyData.length > 0) {
            const dataKeys = sortDataKeys(Object.keys(historyData[0].data));
            
            // Build Dynamic HTML Metric Boxes (only on initial load)
            if (initialLoad) {
                const grid = document.getElementById('dynamicMetricsGrid');
                if (grid && grid.children.length === 0) {
                    const unitsMap = {
                        'temperature': '°C', 'soil_temp': '°C', 'humidity': '%', 'moisture': '%',
                        'pressure': 'hPa', 'vpd': 'kPa', 'ambient_light': 'lx', 'color_temp': 'K',
                        'ppfd': 'μmol', 'eco2': 'ppm', 'tvoc': 'ppb'
                    };
                    
                    dataKeys.forEach(key => {
                        const unit = unitsMap[key] || '';
                        const label = key.toUpperCase().replace('_', ' ');
                        const box = document.createElement('div');
                        box.className = 'metric';
                        box.innerHTML = `
                            <span class="label">${label}</span>
                            <div class="value-container">
                                <span class="value" id="val-${key}">--</span>
                                <span class="unit">${unit}</span>
                            </div>
                        `;
                        grid.appendChild(box);
                    });
                }
                
                if (!chartInstance && document.getElementById('sensorChart')) {
                    initChart(dataKeys);
                }
            }
            
            // Populate Historical Data
            if (chartInstance) {
                chartInstance.data.labels = [];
                chartInstance.data.datasets.forEach(ds => ds.data = []);
                
                historyData.forEach(point => {
                    chartInstance.data.labels.push(point.timestamp);
                    dataKeys.forEach((key, index) => {
                        if (chartInstance.data.datasets[index]) {
                            chartInstance.data.datasets[index].data.push(point.data[key]);
                        }
                    });
                });
                
                maxDataPoints = horizons[horizon] || 60;
                updateChartColors(chartInstance);
                chartInstance.update();
                console.log(`Loaded ${historyData.length} decimated historical points for ${horizon} horizon.`);
                
                if (initialLoad) {
                    const latest = historyData[historyData.length - 1].data;
                    for (const [key, value] of Object.entries(latest)) {
                        const el = document.getElementById(`val-${key}`);
                        if (el) {
                            el.innerText = typeof value === 'number' && value % 1 !== 0 ? value.toFixed(2) : value;
                            const t = THRESHOLDS[key];
                            if (t && (value < t.min || value > t.max)) el.style.color = '#ef4444';
                            else el.style.color = '#e2e8f0';
                        }
                    }
                }
            }
        }
    } catch(err) {
        console.error("Historical Load Failed:", err);
    }
    
    if (initialLoad) connect();
}

// Start sequence
loadHistoricalData("1M", true);

// UI Elements for individual pages
const feedContent = document.getElementById("feedContent");
const sensorBox = document.getElementById("iotSensor");
const liveIndicator = document.querySelector(".live-indicator");
const sensorStatus = document.getElementById("sensorStatus");
const lastUpdatedText = document.getElementById("lastUpdated");
let activeTimeout = null;

// Inventory boxes on index page — dynamically resolved after fetch populates the grid
const indexBoxes = {};
function registerIndexBox(sensorId) {
    const el = document.getElementById(`box-${sensorId}`);
    if (el) indexBoxes[sensorId] = el;
}
const indexTimeouts = {};

let chartInstance = null;
let dataBuffer = [];
const BUFFER_SIZE = 5;

let maxDataPoints = 60; // Default to 1M (60 second horizon)

// Initialize Chart.js
function initChart(keys) {
    const ctx = document.getElementById('sensorChart');
    if (!ctx) return;
    
    // Create UI Toggles
    const toggleContainer = document.getElementById('chartAttributeToggles');
    if (toggleContainer) {
        toggleContainer.innerHTML = ''; // clear wait message
        keys.forEach((key, i) => {
            const btn = document.createElement('button');
            btn.className = `metric-toggle ${i === 0 ? 'active' : ''}`;
            btn.innerText = key.toUpperCase();
            btn.onclick = () => {
                document.querySelectorAll('.metric-toggle').forEach(b => b.classList.remove('active'));
                btn.classList.add('active');
                
                chartInstance.data.datasets.forEach((ds, dsIndex) => {
                    ds.hidden = (dsIndex !== i);
                });
                
                // Deploy mathematical styling passes logically mapping the arrays
                updateChartColors(chartInstance);
                chartInstance.update();
            };
            toggleContainer.appendChild(btn);
        });
    }

    // Create datasets dynamically based on payload keys
    const datasets = keys.map((key, i) => ({
        label: key.toUpperCase(),
        data: [],
        borderColor: `hsl(${i * 65 + 180}, 70%, 50%)`,
        backgroundColor: `hsla(${i * 65 + 180}, 70%, 50%, 0.1)`,
        borderWidth: 2,
        tension: 0.3,
        fill: true,
        pointRadius: 3, // Accent dots
        pointBackgroundColor: `hsl(${i * 65 + 180}, 70%, 30%)`, // Darker dot center
        pointBorderColor: `hsl(${i * 65 + 180}, 70%, 30%)`,     // Darker dot border
        hidden: i !== 0 // ONLY render the first dataset by default!
    }));

    // Attach click listeners to Time Toggles dynamically
    document.querySelectorAll('.time-toggle').forEach(btn => {
        btn.onclick = () => {
            // Update UI State
            document.querySelectorAll('.time-toggle').forEach(b => b.classList.remove('active'));
            btn.classList.add('active');
            
            // Trigger historical backend wipe & replace instead of static JS array truncation
            loadHistoricalData(btn.innerText, false);
        };
    });

    chartInstance = new Chart(ctx, {
        type: 'line',
        data: { labels: [], datasets: datasets },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            animation: false,
            plugins: { legend: { display: false } }, // Hide built-in legend since we have our custom toggle bar
            scales: {
                x: { 
                    type: 'time', 
                    time: { tooltipFormat: 'PPpp' },
                    ticks: { color: 'rgba(255,255,255,0.5)', maxTicksLimit: 8 }, 
                    grid: { color: 'rgba(255,255,255,0.1)' } 
                },
                y: { ticks: { color: 'rgba(255,255,255,0.5)' }, grid: { color: 'rgba(255,255,255,0.1)' } }
            }
        }
    });
}

function handleMessage(message) {
    try {
        const payload = JSON.parse(message.toString());
        const tObj = payload.timestamp ? new Date(payload.timestamp) : new Date();
        
        // --- Intercept Global Alert Payloads ---
        if (payload.type === 'alert') {
            const toastMessage = payload.message;
            const toastLevel = payload.level || 'info';
            
            // Phase 18: Notification Bell Unread Counter
            try {
                if (typeof window.unreadAlerts !== 'undefined') {
                    window.unreadAlerts++;
                    const badge = document.getElementById('alertBadgeCount');
                    if (badge) {
                        badge.innerText = window.unreadAlerts;
                        badge.classList.add('active');
                    }
                }
            } catch(e) {}
            
            // Use the self-contained RAALA toast engine
            if (window.showToast) {
                window.showToast(toastMessage, toastLevel);
            } else {
                console.warn("RAALA Toast engine not initialised.");
            }

            // Append natively to the JSON Event Feed
            if (feedContent) {
                const targetSensor = payload.sensor_id;
                if (sensorType === 'index' || expectedSensorId === targetSensor) {
                    const spanColor = toastLevel === 'error' || toastLevel === 'warning' ? '#f43f5e' : '#34d399';
                    appendLog(formatTime(tObj), `<span style="color:${spanColor}; font-weight:bold">[${toastLevel.toUpperCase()}]</span> ${payload.message}`, true);
                }
            }
            return;
        }
        
        // --- Phase 15: Offline / Online Events (server-driven heartbeat) ---
        if (payload.type === 'offline' || payload.type === 'online') {
            const sid = payload.sensor_id;
            const isOffline = payload.type === 'offline';
            const lastSeenTime = formatTime(new Date());

            // Dashboard page: update sensor box state
            if (sensorBox && expectedSensorId === sid) {
                if (isOffline) {
                    sensorBox.classList.remove('active');
                    sensorBox.classList.add('offline');
                    liveIndicator.classList.remove('active');
                    liveIndicator.classList.add('offline-indicator');
                    if (sensorStatus) {
                        sensorStatus.innerText = 'Offline';
                        sensorStatus.style.color = 'var(--zinc-500)';
                    }
                    if (lastUpdatedText) lastUpdatedText.innerText = `Last seen: ${lastSeenTime}`;
                    if (window.showToast) showToast(`${sid} has gone offline`, 'warning');
                    if (feedContent) appendLog('SYSTEM', `<span style="color:#f59e0b;font-weight:bold">[OFFLINE]</span> ${sid} heartbeat expired`, true);
                } else {
                    sensorBox.classList.remove('offline');
                    sensorBox.classList.add('active');
                    liveIndicator.classList.remove('offline-indicator');
                    liveIndicator.classList.add('active');
                    if (sensorStatus) {
                        sensorStatus.innerText = 'Transmitting';
                        sensorStatus.style.color = 'var(--emerald-400)';
                    }
                    if (feedContent) appendLog('SYSTEM', `<span style="color:#34d399;font-weight:bold">[ONLINE]</span> ${sid} reconnected`, true);
                }
            }

            // Index page: update inventory tile state
            if (sensorType === 'index' && indexBoxes[sid]) {
                const box = indexBoxes[sid];
                const statObj = box.querySelector('.status-text');
                const lastUpd = box.querySelector('.last-updated');
                if (isOffline) {
                    box.classList.remove('live');
                    box.classList.add('offline');
                    if (statObj) statObj.innerText = 'Sensor Offline';
                    if (lastUpd) lastUpd.innerText = `Last: ${lastSeenTime}`;
                } else {
                    box.classList.remove('offline');
                    if (statObj) statObj.innerText = 'Live';
                    if (lastUpd) lastUpd.innerText = lastSeenTime;
                }
            }
            return;
        }

        // --- Index Page Logic ---
        if (sensorType === 'index') {
            const id = payload.sensor_id;
            if (indexBoxes[id]) {
                const box = indexBoxes[id];
                // Clear any offline state when live data resumes
                box.classList.remove('offline');
                box.classList.add('live');
                const statObj = box.querySelector('.status-text');
                const lastUpd = box.querySelector('.last-updated');
                if (statObj) statObj.innerText = 'Live Data Stream Active';
                if (lastUpd) lastUpd.innerText = tObj.toLocaleTimeString();
            }
            return;
        }

        // --- Hardware UI Box (Individual Pages) ---
        // expectedSensorId is set at module level and handles both:
        //   legacy:   sensorType='bme280'   → typeToSensorMap['bme280'] = 'sensor_01'
        //   Phase 14: sensorType='sensor_01' → fallback to 'sensor_01'
        if (payload.sensor_id !== expectedSensorId) return; // The crucial filter!

        if (sensorBox) {
            sensorBox.classList.add("active");
            liveIndicator.classList.add("active");
            sensorStatus.innerText = "Transmitting";
            sensorStatus.style.color = "var(--emerald-400)";
            lastUpdatedText.innerText = tObj.toLocaleTimeString();

            // 1) Initialize Chart and Dynamic UI if not done
            const dataKeys = sortDataKeys(Object.keys(payload.data));
            
            // Build Dynamic HTML Metric Boxes magically!
            const grid = document.getElementById('dynamicMetricsGrid');
            if (grid && grid.children.length === 0) {
                const unitsMap = {
                    'temperature': '°C', 'soil_temp': '°C', 'humidity': '%', 'moisture': '%',
                    'pressure': 'hPa', 'vpd': 'kPa', 'ambient_light': 'lx', 'color_temp': 'K',
                    'ppfd': 'μmol', 'eco2': 'ppm', 'tvoc': 'ppb'
                };
                
                dataKeys.forEach(key => {
                    const unit = unitsMap[key] || '';
                    const label = key.toUpperCase().replace('_', ' ');
                    const box = document.createElement('div');
                    box.className = 'metric';
                    box.innerHTML = `
                        <span class="label">${label}</span>
                        <div class="value-container">
                            <span class="value" id="val-${key}">--</span>
                            <span class="unit">${unit}</span>
                        </div>
                    `;
                    grid.appendChild(box);
                });
            }

            if (!chartInstance && document.getElementById('sensorChart')) {
                initChart(dataKeys);
            }

            // 2) Update Chart with raw 1-second data
            if (chartInstance) {
                chartInstance.data.labels.push(payload.timestamp);
                dataKeys.forEach((key, index) => {
                    if (chartInstance.data.datasets[index]) {
                        chartInstance.data.datasets[index].data.push(payload.data[key]);
                    }
                });

                // Extend line chart by 1 tick constraint by maxDataPoints horizon
                if (chartInstance.data.labels.length > maxDataPoints) {
                    chartInstance.data.labels.shift();
                    chartInstance.data.datasets.forEach(ds => ds.data.shift());
                }
                
                // Deploy real-time structural re-renders
                updateChartColors(chartInstance);
                chartInstance.update('none');
            }

            // 3) Push to the 5-second chunk buffer
            dataBuffer.push(payload.data);

            // 4) If buffer is full, calculate the average and update the large UI text
            if (dataBuffer.length >= BUFFER_SIZE) {
                const averagedData = {};
                
                dataKeys.forEach(key => {
                    const sum = dataBuffer.reduce((acc, curr) => acc + curr[key], 0);
                    averagedData[key] = sum / BUFFER_SIZE;
                });

                // Update UI text with 5-second average
                for (const [key, value] of Object.entries(averagedData)) {
                    const el = document.getElementById(`val-${key}`);
                    if (el) el.innerText = typeof value === 'number' && value % 1 !== 0 ? value.toFixed(2) : value;
                }

                // Clear buffer for the next 5 seconds
                dataBuffer = [];
            }

            if (activeTimeout) clearTimeout(activeTimeout);
            activeTimeout = setTimeout(() => {
                sensorBox.classList.remove("active");
                liveIndicator.classList.remove("active");
                sensorStatus.innerText = "Waiting...";
                sensorStatus.style.color = "var(--zinc-500)";
            }, 4000);
        }

        // --- Terminal Feed ---
        if (feedContent) {
            const formattedPayload = syntaxHighlight(JSON.stringify(payload, null, 2));
            appendLog(formatTime(tObj), formattedPayload, true);
        }
        
    } catch (e) {
        if(feedContent) appendLog(formatTime(new Date()), `Decode Error: ${e.message}`);
    }
}

function appendLog(timeStr, contentHTML, isHtml = false) {
    if (!feedContent) return;
    const entry = document.createElement("div");
    entry.className = "log-entry";
    
    const timeEl = document.createElement("div");
    timeEl.className = "log-time";
    timeEl.innerText = timeStr;

    const dataEl = document.createElement("div");
    dataEl.className = "log-data";
    
    if (isHtml) dataEl.innerHTML = contentHTML;
    else dataEl.innerText = contentHTML;

    entry.appendChild(timeEl);
    entry.appendChild(dataEl);
    feedContent.appendChild(entry);

    if (feedContent.children.length > 50) feedContent.removeChild(feedContent.firstChild);
    feedContent.scrollTop = feedContent.scrollHeight;
}

function formatTime(date) {
    return date.toISOString().split('T')[1].slice(0, 12);
}

function syntaxHighlight(json) {
    json = json.replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;');
    return json.replace(/("(\\u[a-zA-Z0-9]{4}|\\[^u]|[^\\"])*"(\s*:)?|\b(true|false|null)\b|-?\d+(?:\.\d*)?(?:[eE][+\-]?\d+)?)/g, function (match) {
        let cls = 'number';
        if (/^"/.test(match)) {
            if (/:$/.test(match)) cls = 'key';
            else cls = 'string';
        } else if (/true|false/.test(match)) cls = 'boolean';
        else if (/null/.test(match)) cls = 'null';
        return '<span class="' + cls + '">' + match + '</span>';
    });
}

// ──────────────────────────────────────────────
// Phase 17 & 18: Notification Bell & Slide Drawer UX
// ──────────────────────────────────────────────

function initDrawers() {
    const drawerOverlay = document.getElementById('drawerOverlay');
    const slideDrawer = document.getElementById('slideDrawer');
    const drawerTitle = document.getElementById('drawerTitle');
    const drawerContent = document.getElementById('drawerContent');
    const drawerClose = document.getElementById('drawerClose');
    const btnAlerts = document.getElementById('btnAlerts');
    const btnSettings = document.getElementById('btnSettings');
    
    window.unreadAlerts = 0;

    function closeDrawer() {
        if(drawerOverlay) drawerOverlay.classList.remove('open');
        if(slideDrawer) slideDrawer.classList.remove('open');
    }

    if (drawerClose) drawerClose.addEventListener('click', closeDrawer);
    if (drawerOverlay) drawerOverlay.addEventListener('click', closeDrawer);

    // Phase 18: Alerts Drawer
    if (btnAlerts && drawerTitle) {
        btnAlerts.addEventListener('click', async () => {
            drawerTitle.innerText = "Alert History";
            drawerOverlay.classList.add('open');
            slideDrawer.classList.add('open');
            drawerContent.innerHTML = '<span style="color:var(--zinc-500)">Loading Timeline...</span>';
            
            try {
                // Clear unread count when viewing
                window.unreadAlerts = 0;
                const badge = document.getElementById('alertBadgeCount');
                if (badge) badge.classList.remove('active');
                
                const res = await fetch('http://localhost:8000/api/alerts');
                const alerts = await res.json();
                
                if (!alerts || alerts.length === 0) {
                    drawerContent.innerHTML = '<span style="color:var(--zinc-500)">No alerts logged in the past 24 hours.</span>';
                    return;
                }
                
                let html = '<ul class="alert-list">';
                alerts.forEach(a => {
                    const ackClass = a.acknowledged ? "acknowledged" : "";
                    const ackBtnHTML = a.acknowledged ? 
                        `<button class="ack-btn" disabled>Acknowledged</button>` : 
                        `<button class="ack-btn" onclick="window.ackAlert('${a.id}')">Acknowledge</button>`;
                        
                    const isGlobal = (typeof expectedSensorId === 'undefined' || expectedSensorId === 'index');
                    const prefix = (isGlobal || a.sensor_id !== expectedSensorId) ? `<strong>${a.sensor_id}</strong> - ` : '';
                    
                    html += `
                        <li class="alert-item ${ackClass}" id="alert-dom-${a.id}">
                            <div class="alert-header">
                                <span style="opacity:0.7">${new Date(a.timestamp).toLocaleString(undefined, {hour:'2-digit', minute:'2-digit'})}</span>
                                <span style="color:var(--rose-500);font-weight:bold">${a.level.toUpperCase()}</span>
                            </div>
                            <div class="alert-msg">${prefix}${a.message}</div>
                            ${ackBtnHTML}
                        </li>
                    `;
                });
                html += '</ul>';
                drawerContent.innerHTML = html;
            } catch (e) {
                drawerContent.innerHTML = '<span style="color:var(--rose-500)">Error fetching alert log.</span>';
                console.error(e);
            }
        });
    }

    // Acknowledge Function (global window scope for inline onclicks)
    window.ackAlert = async function(id) {
        try {
            await fetch(`http://localhost:8000/api/alerts/acknowledge/${id}`, {method: 'POST'});
            const li = document.getElementById(`alert-dom-${id}`);
            if(li) {
                li.classList.add('acknowledged');
                const btn = li.querySelector('.ack-btn');
                if(btn) {
                    btn.innerText = "Acknowledged";
                    btn.disabled = true;
                }
            }
        } catch(e) {
            console.error("Failed to acknowledge", e);
        }
    };

    // Phase 17: Settings Drawer (Configurable Thresholds)
    if (btnSettings && drawerTitle) {
        btnSettings.addEventListener('click', async () => {
            if (typeof expectedSensorId === 'undefined' || expectedSensorId === 'loading' || expectedSensorId === 'index') return;
            
            drawerTitle.innerText = "Active Thresholds Mode";
            drawerOverlay.classList.add('open');
            slideDrawer.classList.add('open');
            drawerContent.innerHTML = '<span style="color:var(--zinc-500)">Loading Server Constraints...</span>';
            
            try {
                const res = await fetch(`http://localhost:8000/api/thresholds/${expectedSensorId}`);
                const thresholds = await res.json();
                
                // Map sensor metrics to visual slider bounds for UI rendering
                function getBoundsForAttribute(attr) {
                    switch (attr) {
                        case 'temperature': return {min: -20, max: 80};
                        case 'humidity': return {min: 0, max: 100};
                        case 'pressure': return {min: 900, max: 1200};
                        case 'vpd': return {min: 0, max: 5};
                        case 'lux': return {min: 0, max: 65000};
                        case 'uv_index': return {min: 0, max: 15};
                        case 'tvoc': return {min: 0, max: 60000};
                        case 'eco2': return {min: 400, max: 60000};
                        case 'moisture': return {min: 200, max: 1000}; 
                        default: return {min: 0, max: 2000};
                    }
                }

                // Pluck existing metrics dynamically from the UI
                const liveLabels = Array.from(document.querySelectorAll('.metric .label'));
                
                if (liveLabels.length === 0) {
                     drawerContent.innerHTML = '<span style="color:var(--zinc-500)">Waiting for live telemetry to parse active capabilities...</span>';
                     return;
                }
                
                let html = '<div style="display:flex;flex-direction:column;gap:1.5rem;">';
                const activeKeys = [];
                liveLabels.forEach(el => {
                     const key = el.innerText.toLowerCase().replace(' ', '_');
                     activeKeys.push(key);
                     const t = thresholds[key] || {min: 0, max: 100};
                     html += `
                        <div class="slider-group">
                            <label style="display:flex; justify-content:space-between">
                               <span>${key.toUpperCase()} safe range</span>
                            </label>
                            <div class="slider-container">
                                <div id="noui-${key}"></div>
                                <div class="slider-value-tags">
                                    <span id="slider-min-val-${key}">0</span>
                                    <span id="slider-max-val-${key}">0</span>
                                </div>
                            </div>
                        </div>
                     `;
                });
                html += `</div><button class="save-btn" id="btnSaveSettings">Push Hot Reload to Server</button>`;
                
                drawerContent.innerHTML = html;
                
                // Initialize noUiSlider instances
                const activeSliders = {};
                activeKeys.forEach(k => {
                    const el = document.getElementById(`noui-${k}`);
                    const t = thresholds[k] || {min: 0, max: 100};
                    const bounds = getBoundsForAttribute(k);
                    
                    noUiSlider.create(el, {
                        start: [t.min, t.max],
                        connect: true,
                        range: {
                            'min': bounds.min,
                            'max': bounds.max
                        },
                        step: 0.1
                    });
                    
                    activeSliders[k] = el.noUiSlider;
                    
                    el.noUiSlider.on('update', function (values, handle) {
                        if (handle === 0) {
                            document.getElementById(`slider-min-val-${k}`).innerText = `Min: ${parseFloat(values[0]).toFixed(2)}`;
                        } else {
                            document.getElementById(`slider-max-val-${k}`).innerText = `Max: ${parseFloat(values[1]).toFixed(2)}`;
                        }
                    });
                });
                
                // Bind Save Logic
                const btnSave = document.getElementById('btnSaveSettings');
                if (btnSave) {
                    btnSave.addEventListener('click', async () => {
                        const payload = { thresholds: {} };
                        activeKeys.forEach(k => {
                             const vals = activeSliders[k].get();
                             payload.thresholds[k] = {
                                 min: parseFloat(vals[0]),
                                 max: parseFloat(vals[1])
                             };
                        });
                        try {
                            btnSave.innerText = "Deploying...";
                            btnSave.style.opacity = 0.5;
                            await fetch(`http://localhost:8000/api/thresholds/${expectedSensorId}`, {
                                method: 'PUT',
                                headers: {'Content-Type': 'application/json'},
                                body: JSON.stringify(payload)
                            });
                            closeDrawer();
                            if(window.showToast) window.showToast("New Edge compute limits successfully deployed without restart! ✅", "success");
                        } catch(e) {
                            console.error(e);
                            if(window.showToast) window.showToast("Failed to save backend constraints", "error");
                        } finally {
                            btnSave.innerText = "Push Hot Reload to Server";
                            btnSave.style.opacity = 1;
                        }
                    });
                }
                
            } catch(e) {
                 drawerContent.innerHTML = '<span style="color:var(--rose-500)">Network disconnect. Cannot reach backend registry.</span>';
                 console.error(e);
            }
        });
    }
}

if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', initDrawers);
} else {
    initDrawers();
}
