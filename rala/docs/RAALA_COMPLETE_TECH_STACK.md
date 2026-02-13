# RAALA - Complete Technical Overview

## 🌱 What is RAALA?

**RAALA** (Reinforcement-learning Autonomous Life-support Automation) is an **AI-powered autonomous greenhouse operating system** that uses deep reinforcement learning, digital twin technology, and real-time sensor networks to optimize energy consumption and maximize crop yields.

### The Problem

Commercial greenhouses face critical challenges:

- **Energy costs:** 30-40% of total operating expenses
- **Manual control:** Labor-intensive environmental management
- **Inconsistent yields:** Suboptimal growing conditions
- **Market size:** $110B global greenhouse automation opportunity

### The Solution

RAALA provides:

- **30% energy savings** through AI-driven HVAC/lighting optimization
- **12% yield increase** via precise environmental control
- **3-6 month ROI** with measurable, immediate cost reductions
- **24/7 autonomous operation** with minimal human intervention

### Core Technology

1. **Neural Mesh** - 1,024+ sensor network for comprehensive monitoring
2. **RL Engine** - Deep reinforcement learning (PPO algorithm) for continuous optimization
3. **Digital Twin** - Physics-based virtual greenhouse simulation
4. **Autonomous Mode** - Level 5 automation (full autonomy)
5. **Energy-First** - Tackles the #1 greenhouse operating expense
6. **Retrofit-Ready** - Works with existing equipment (no rip-and-replace)

---

## 🏗️ System Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                        RAALA Platform                       │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  ┌──────────────┐    ┌──────────────┐    ┌──────────────┐ │
│  │   Frontend   │◄───│   API Layer  │◄───│   Services   │ │
│  │   (Nuxt 3)   │    │   (FastAPI)  │    │   (Python)   │ │
│  └──────────────┘    └──────────────┘    └──────────────┘ │
│         ▲                    ▲                    ▲         │
│         │                    │                    │         │
│         └────────────────────┴────────────────────┘         │
│                              │                               │
│                              ▼                               │
│  ┌──────────────────────────────────────────────────────┐  │
│  │            Data & ML Infrastructure                  │  │
│  │  ┌──────────┐  ┌──────────┐  ┌──────────────────┐  │  │
│  │  │InfluxDB  │  │PostgreSQL│  │  Training Pipeline│  │  │
│  │  │(Sensors) │  │  (Users) │  │  (RL/ML Models)  │  │  │
│  │  └──────────┘  └──────────┘  └──────────────────┘  │  │
│  └──────────────────────────────────────────────────────┘  │
│                              │                               │
│                              ▼                               │
│  ┌──────────────────────────────────────────────────────┐  │
│  │            Edge Deployment Layer                     │  │
│  │        (MQTT, WebSockets, HTTP/REST)                 │  │
│  └──────────────────────────────────────────────────────┘  │
└─────────────────────────────────────────────────────────────┘
                               │
                               ▼
┌─────────────────────────────────────────────────────────────┐
│                  Greenhouse Edge Gateway                    │
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────────────┐│
│  │   Sensors   │  │Control Logic│  │ Local ML Inference  ││
│  │(I2C/Modbus) │  │(MQTT Client)│  │   (ONNX Runtime)    ││
│  └─────────────┘  └─────────────┘  └─────────────────────┘│
└─────────────────────────────────────────────────────────────┘
                               │
                               ▼
                     ┌──────────────────┐
                     │Physical Equipment│
                     │ HVAC | Lighting  │
                     │   Irrigation     │
                     └──────────────────┘
```

---

## 💻 Complete Tech Stack

### **Frontend Layer**

#### **Framework**

- **Nuxt 3** (v4.2.1) - Vue meta-framework
  - SSR (Server-Side Rendering) for SEO
  - Hybrid rendering (SSR + Client-side)
  - File-based routing
  - Auto-imports for components/composables
  - Nitro engine with route prerendering
- **Vue 3** (v3.5.25) - Progressive JavaScript framework
  - Composition API
  - Reactive state management
  - Single File Components (SFC)
- **Vue Router** (v4.6.3) - Official routing library

#### **Language**

- **TypeScript** - Type-safe development
- **JavaScript ES6+** - Modern syntax
- **ES Modules** - Module system

#### **Styling**

- **Tailwind CSS** (v6.14.0 via @nuxtjs/tailwindcss)
  - Utility-first CSS framework
  - Custom color palette (RAALA Green: #10B981)
  - JIT (Just-In-Time) compilation
- **Semantic CSS** - Custom scoped component styles
  - BEM-like naming conventions
  - Component-scoped styles
- **CSS Variables** - Design token system
- **Custom Fonts:**
  - Inter - Primary UI font
  - JetBrains Mono - Code/data displays

#### **Graphics & Animation**

- **Three.js** (v0.181.2) - 3D WebGL library
  - Particle field background animations
  - Interactive visual effects
  - Custom shader implementations
  - Client-side only rendering
- **GSAP (GreenSock)** (v3.13.0) - Professional animation library
  - ScrollTrigger plugin for scroll-based animations
  - Timeline animations
  - Smooth transitions and effects
- **CSS Animations** - Native CSS keyframes
  - Pulse, bounce, scan, ping effects
  - Hardware-accelerated transforms

#### **Icons & Assets**

- **Iconify** - Unified icon framework
  - Custom element support (`<iconify-icon>`)
  - On-demand icon loading

#### **State Management**

- **Vue Composables** - Composition API pattern
  - `useAppState.ts` - Global app state
  - Auto-imported across components
- **Pinia** - Vue 3 state management (planned)

---

### **Backend Layer (Planned Architecture)**

#### **API Framework**

- **FastAPI** (Python 3.11+) - High-performance async framework
  - Automatic OpenAPI documentation
  - Pydantic validation
  - WebSocket support
  - JWT authentication

#### **Authentication & Security**

- **Supabase** (@nuxtjs/supabase v2.0.3)
  - PostgreSQL database
  - Built-in authentication
  - Row-level security
  - Real-time subscriptions
  - Storage for assets
- **@supabase/supabase-js** (v2.89.0) - JavaScript client
- **JWT (JSON Web Tokens)** - Token-based auth
- **python-jose** - JWT encoding/decoding (Python)
- **passlib[bcrypt]** - Password hashing

#### **Core Services**

```python
# Service architecture
- SensorService - Sensor data ingestion/retrieval
- ControlService - Equipment control commands
- MLService - Model inference/training
- DigitalTwinService - Simulation engine
```

#### **Communication**

- **WebSockets** - Real-time bidirectional data
- **MQTT** - IoT messaging protocol
  - Edge-to-cloud communication
  - Quality of Service (QoS) levels
  - Retained messages
- **Redis** (v5.0.1) - In-memory cache & pub/sub
  - Session management
  - Rate limiting
  - Real-time message broker
- **Celery** (v5.3.4) - Distributed task queue
  - Async background jobs
  - Scheduled tasks

---

### **Database Layer**

#### **Time-Series Database**

- **InfluxDB** - Optimized for sensor data
  - High-write throughput (1000+ writes/sec)
  - Nanosecond timestamp precision
  - Tag-based indexing
  - Continuous queries for downsampling
  - Retention policies:
    - High-res (1-min): 7 days
    - Medium-res (5-min): 90 days
    - Low-res (1-hour): Forever

**Schema:**

```
Measurements:
- sensor_readings (temp, humidity, co2, ppfd, vpd, soil_moisture)
- equipment_state (HVAC, lighting, irrigation)
- ml_predictions (model outputs vs actuals)
```

#### **Relational Database**

- **PostgreSQL** - Primary relational database
  - JSONB for flexible schemas
  - PostGIS for geospatial data
  - Full-text search

**Tables:**

```sql
- users (authentication, profiles)
- facilities (greenhouse metadata)
- equipment (device inventory, protocols)
- sensors (sensor metadata, calibration)
- ml_models (model versions, metrics)
- alerts (notifications, acknowledgments)
- daily_metrics (aggregated performance)
```

#### **Caching Layer**

- **Redis** - Key-value store
  - Config caching (TTL: 1 hour)
  - Pub/Sub for WebSocket broadcasting
  - API rate limiting
  - Session storage

---

### **Machine Learning & AI**

#### **Reinforcement Learning**

- **Python 3.11+** - Core ML language
- **PyTorch** - Deep learning framework
- **Stable Baselines 3** - RL algorithms library
  - PPO (Proximal Policy Optimization)
  - A2C (Advantage Actor-Critic)
  - Custom environment wrappers
- **OpenAI Gym** - Environment interface
  - Custom `GreenhouseSimEnv` environment
  - Observation space: [temp, humidity, co2, vpd, solar, ...]
  - Action space: [hvac_setpoint, light_intensity, co2_flow]

#### **ML Pipeline**

```python
Training:
1. Historical data extraction (InfluxDB)
2. Environment simulation (Digital Twin)
3. PPO training (1M+ timesteps)
4. Validation on held-out data
5. ONNX export for edge deployment

Inference:
1. Real-time state collection
2. ONNX model inference (<100ms)
3. Safety constraint validation
4. Action execution via MQTT
```

#### **Digital Twin Simulator**

- **Physics-based modeling:**
  - Energy balance equations
  - Penman-Monteith evapotranspiration
  - Photosynthesis rate calculations (Tomich model)
  - HVAC thermodynamics
  - Solar radiation modeling
- **Calibration:**
  - Parameter tuning from real facility data
  - System identification techniques
  - Continuous model refinement

#### **Edge ML**

- **ONNX Runtime** - Cross-platform inference
  - Optimized for ARM64 (Raspberry Pi)
  - <100ms latency for real-time control
  - Model versioning and A/B testing

#### **Model Monitoring**

- **MLflow** (planned) - Experiment tracking
- **Prometheus** - Metrics collection
- **Sentry** - Error tracking

---

### **Hardware & Edge Computing**

#### **Edge Gateway**

- **Raspberry Pi 4 Model B (4GB RAM)** - Recommended
  - 64-bit ARM Cortex-A72 quad-core @ 1.5GHz
  - GPIO pins for sensor interfacing
  - I2C, SPI, UART, 1-Wire support
  - Gigabit Ethernet
  - WiFi 5 (802.11ac)
- **Operating System:**
  - Raspberry Pi OS (64-bit, headless)
  - Ubuntu Server 22.04 LTS (alternative)

#### **Sensor Protocols**

- **I2C (Primary)** - Inter-Integrated Circuit
  - BME280, SCD30, BH1750, MLX90614
  - Two-wire communication (SDA/SCL)
  - Multi-device bus (unique addresses)
- **1-Wire** - Temperature sensors
  - DS18B20 waterproof probes
- **Analog (via ADC)** - Soil, pH, TDS sensors
  - ADS1115 16-bit I2C ADC
  - 0-3.3V input range
- **Modbus RTU/TCP** - Industrial equipment
  - HVAC controllers
  - VFD (Variable Frequency Drives)
- **BACnet IP** - Building automation
  - Commercial HVAC systems

#### **Sensor Inventory**

| Parameter      | Sensor Model           | Interface    | Accuracy |
| -------------- | ---------------------- | ------------ | -------- |
| Temperature    | BME280                 | I2C          | ±1.0°C   |
| Humidity       | BME280                 | I2C          | ±3% RH   |
| Pressure       | BME280                 | I2C          | ±1 hPa   |
| CO₂            | SCD30                  | I2C          | ±30 ppm  |
| Light (Lux)    | BH1750                 | I2C          | ±20%     |
| PPFD (planned) | AS7341 / Apogee SQ-500 | I2C / Analog | ±5%      |
| Leaf Temp      | MLX90614               | I2C          | ±0.5°C   |
| Soil Moisture  | Capacitive v1.2        | Analog (ADC) | ±3% VWC  |
| pH             | DFRobot Analog         | Analog (ADC) | ±0.1 pH  |
| TDS/EC         | DFRobot Analog         | Analog (ADC) | ±10%     |

#### **Edge Software Stack**

```bash
Python Libraries:
- adafruit-circuitpython-bme280  # Sensor drivers
- paho-mqtt                       # MQTT client
- influxdb-client                 # InfluxDB writer
- onnxruntime                     # ML inference
- smbus2                          # I2C communication
- RPi.GPIO                        # GPIO control
```

---

### **DevOps & Infrastructure**

#### **Version Control**

- **Git** - Source control
- **GitHub** - Repository hosting

#### **Build Tools**

- **Vite** - Frontend build tool (bundled with Nuxt)
  - Fast HMR (Hot Module Replacement)
  - ES module bundling
  - Tree shaking
- **Nitro** - Server engine (Nuxt)
  - Universal deployment
  - Route rules
  - Prerendering

#### **Package Managers**

- **npm** - Node.js package manager
- **pip** - Python package manager
- **apt** - System packages (Raspberry Pi)

#### **Development Environment**

- **Node.js** - JavaScript runtime
- **Python 3.11+** - ML/backend runtime
- **Nuxt DevTools** - Built-in debugging

#### **Deployment (Planned)**

**Cloud Platform:** AWS

```
- CloudFront CDN (static assets)
- Application Load Balancer
- ECS (Elastic Container Service) - FastAPI containers
- RDS (PostgreSQL)
- ElastiCache (Redis)
- EC2 (InfluxDB)
- S3 (ML models, backups)
- SageMaker (ML training)
```

**Containerization:**

- **Docker** - Application containers
- **Kubernetes (EKS)** - Orchestration
  - Auto-scaling
  - Rolling deployments
  - Health checks

**CI/CD:**

- **GitHub Actions** (planned)
  - Automated testing
  - Build pipelines
  - Deployment automation

**Monitoring:**

- **Prometheus** - Metrics collection
- **Grafana** - Visualization dashboards
- **Sentry** - Error tracking
- **CloudWatch** - AWS monitoring

---

### **Communication Protocols**

#### **Real-Time Data Flow**

```
Sensor → Edge → MQTT Broker → Cloud Ingestion → InfluxDB → WebSocket → Dashboard
          ↓
     Local RL Model
          ↓
     Equipment Control
```

#### **Protocols Used**

- **HTTP/HTTPS** - REST API (TLS 1.3)
- **WebSocket** - Real-time bidirectional (wss://)
- **MQTT** - IoT messaging
  - Topic structure: `facility/{id}/sensors/{type}`
  - QoS 1 (at-least-once delivery)
  - Retained messages for latest values
- **I2C** - Sensor communication (400 kHz)
- **Modbus RTU** - Serial equipment (9600 baud)
- **BACnet/IP** - Building automation (UDP port 47808)

---

### **Security & Compliance**

#### **Authentication & Authorization**

- **JWT tokens** - Stateless authentication
  - Access token (1 hour TTL)
  - Refresh token (30 days TTL)
- **RBAC** - Role-Based Access Control
  - Admin: Full access
  - Operator: Control equipment
  - Viewer: Read-only

#### **Encryption**

- **TLS 1.3** - All HTTP/WebSocket traffic
- **MQTT over TLS** - Edge communication
- **Database encryption at rest**
- **S3 server-side encryption** - Model storage

#### **Security Measures**

- **Certificate pinning** - Mobile apps
- **Device certificates** - mTLS for edge gateways
- **Firewall rules** - Outbound MQTT/HTTPS only
- **Auto-updates** - Security patches
- **Rate limiting** - API abuse prevention

#### **Compliance (Planned)**

- **SOC 2 Type II** - Security certification
- **GDPR** - European data protection
- **CCPA** - California privacy law

---

## 📁 Project Structure

```
e:/projects/rala/rala/
├── app/                           # Nuxt application
│   ├── pages/                     # File-based routes
│   │   ├── index.vue             # Landing page
│   │   ├── login.vue             # Authentication
│   │   ├── dashboard.vue         # Real-time dashboard
│   │   ├── loading-test.vue      # Loading widget test
│   │   └── auth/                 # Auth pages
│   ├── components/                # Vue components
│   │   ├── Navbar.vue            # Navigation bar
│   │   ├── Footer.vue            # Site footer
│   │   ├── LoadingWidget.vue     # Original loader
│   │   ├── LoadingWidgetNew.vue  # Premium loader (lusion-inspired)
│   │   └── dashboard/            # Dashboard components
│   │       ├── DashboardSidebar.vue
│   │       ├── DashboardHeader.vue
│   │       ├── MetricsGrid.vue
│   │       ├── SensorMesh.vue
│   │       ├── AgentLogs.vue
│   │       └── HardwareSection.vue
│   ├── layouts/                   # App layouts
│   │   ├── default.vue           # Default (with nav/footer)
│   │   └── dashboard.vue         # Full-screen dashboard
│   ├── composables/               # Composable functions
│   │   └── useAppState.ts        # Global state management
│   ├── plugins/                   # Nuxt plugins
│   │   ├── gsap.client.ts        # GSAP initialization
│   │   └── three.client.ts       # Three.js particle system
│   ├── assets/                    # Static assets
│   │   └── css/main.css          # Global styles (Tailwind imports)
│   └── app.vue                    # Root component
├── public/                        # Public static files
│   └── raala-logo.png            # RAALA logo
├── docs/                          # Documentation
│   ├── RALA_OVERVIEW.md          # Complete product overview (600+ lines)
│   ├── EXECUTIVE_SUMMARY.md      # Quick reference (350 lines)
│   ├── TECHNICAL_ARCHITECTURE.md # Technical deep-dive (800+ lines)
│   └── README.md                 # Documentation index
├── .nuxt/                         # Nuxt build cache
├── node_modules/                  # NPM dependencies
├── nuxt.config.ts                 # Nuxt configuration
├── tailwind.config.js             # Tailwind config
├── tsconfig.json                  # TypeScript config
├── package.json                   # Dependencies manifest
├── package-lock.json              # Locked versions
├── .gitignore                     # Git ignore rules
└── .env                           # Environment variables (gitignored)
```

---

## 🎨 Design System

### **Color Palette**

```css
/* Primary - Emerald (RAALA Brand) */
--emerald-400: #34d399;
--emerald-500: #10b981; /* Primary brand color */
--emerald-900: #047857;

/* Alerts */
--amber-500: #f59e0b;
--rose-400: #fb7185;
--rose-500: #f43f5e;

/* Grayscale (Dark Theme) */
--zinc-50: #fafafa;
--zinc-400: #a1a1aa;
--zinc-500: #71717a;
--zinc-600: #52525b;
--zinc-700: #3f3f46;
--zinc-800: #27272a;
--zinc-900: #18181b;
--zinc-950: #09090b; /* Background */
```

### **Typography**

- **Headings:** Inter (600 weight, tight tracking)
- **Body:** Inter (400/500 weight)
- **Code/Data:** JetBrains Mono (monospace)

### **Design Philosophy**

- ✨ Premium dark mode (deep blacks)
- 🔮 Glassmorphism (frosted glass effects)
- 🎬 Micro-animations (pulse, bounce, scan)
- 📐 Semantic CSS (`.metric-card`, `.sensor-node`)
- 📱 Mobile-first responsive design

### **Responsive Breakpoints**

```css
sm: 640px   /* Mobile landscape */
md: 768px   /* Tablet */
lg: 1024px  /* Desktop */
xl: 1280px  /* Large desktop */
```

---

## 🚀 Performance Optimizations

### **Frontend**

- **Code splitting** - Route-based chunking
- **Lazy loading** - Components on demand
- **Tree shaking** - Unused code elimination
- **SSG for homepage** - Static generation
- **Image optimization** - WebP format
- **Font subsetting** - Only used characters

### **Backend**

- **Connection pooling** - Database connections
- **Redis caching** - Frequently accessed data
- **Query optimization** - Database indexes
- **Batch operations** - Reduce round trips

### **Edge**

- **Local ML inference** - <100ms latency
- **Data batching** - Reduce MQTT overhead
- **Compression** - Reduce bandwidth

---

## 📊 Key Metrics & KPIs

### **Technical Metrics**

- **Sensor sampling rate:** 30 seconds
- **Dashboard update latency:** <500ms
- **ML inference time:** <100ms
- **Data retention:** 7 days (1-min), 90 days (5-min), forever (1-hour)
- **API response time:** <200ms (p95)
- **Uptime target:** 99.9%

### **Business Metrics**

- **Energy savings:** 30%
- **Yield increase:** 12%
- **ROI:** 3-6 months
- **Target market:** $110B
- **Pricing:** $2,500-$10,000+/month (tiered)

---

## 🔄 Data Flow Example

### **Temperature Sensor Reading → Dashboard Display**

1. **Sensor reads temperature** (BME280 via I2C)

   ```python
   temp = bme280.temperature  # 23.5°C
   ```

2. **Edge gateway processes**

   ```python
   data = {
       "facility_id": "abc123",
       "sensor_id": "zone1_temp",
       "timestamp": "2026-01-23T08:35:24Z",
       "temperature": 23.5,
       "humidity": 65.2,
       "vpd": 1.2
   }
   ```

3. **Publish to MQTT**

   ```
   Topic: facility/abc123/sensors/zone1
   Payload: {JSON above}
   QoS: 1
   ```

4. **Cloud ingestion service subscribes**

   ```python
   # Batch write to InfluxDB every 5s
   influx_client.write_points([data])
   ```

5. **WebSocket broadcasts to connected clients**

   ```javascript
   ws.send(
     JSON.stringify({
       type: "sensor_update",
       data: data,
     }),
   );
   ```

6. **Dashboard receives & updates**

   ```vue
   <script setup>
   const { data } = useWebSocket("wss://api.raala.io/ws");

   watch(data, (newData) => {
     if (newData.type === "sensor_update") {
       metrics.value.temperature = newData.data.temperature;
     }
   });
   </script>
   ```

7. **Vue component re-renders**
   ```vue
   <template>
     <div class="metric-card">
       <span class="metric-value">{{ metrics.temperature }}°C</span>
     </div>
   </template>
   ```

**Total latency:** ~500ms (sensor → screen)

---

## 🎯 Current Development Status

### **✅ Completed (Production Ready)**

- Frontend web application (Nuxt 3 + Vue 3)
- Dashboard UI with real-time metrics display
- Authentication system (Supabase)
- Premium loading animations
- Responsive design (mobile/tablet/desktop)
- Three.js particle effects
- GSAP scroll animations

### **🚧 In Progress**

- Hardware sensor integration (Raspberry Pi)
- MQTT broker setup
- InfluxDB time-series database
- WebSocket real-time updates
- Live sensor data streaming

### **📋 Planned (Next Phases)**

- ML model training pipeline
- Digital twin simulator
- Edge ML inference (ONNX)
- Multi-facility support
- Mobile apps (iOS/Android)
- Advanced analytics dashboard
- Carbon credit integration

---

## 🛠️ Development Setup

### **Prerequisites**

```bash
- Node.js 18+
- npm 9+
- Python 3.11+ (for backend)
- Raspberry Pi 4 (for edge)
```

### **Installation**

```bash
# Clone repository
git clone https://github.com/Chirag005/rala.git
cd rala/rala

# Install dependencies
npm install

# Configure environment
cp .env.example .env
# Edit .env with Supabase credentials

# Run development server
npm run dev
# Opens at http://localhost:3000
```

### **Available Scripts**

```bash
npm run dev      # Development server (HMR)
npm run build    # Production build
npm run preview  # Preview production build
npm run generate # Static site generation
```

---

## 🌟 Unique Selling Points

1. **Energy-First Approach** - Target #1 operating expense (30% savings)
2. **Immediate ROI** - Measurable savings in 3-6 months
3. **Retrofit-Ready** - No equipment replacement needed
4. **Autonomous AI** - Level 5 automation with RL
5. **Digital Twin** - Physics-based simulation for safe optimization
6. **Scalable Architecture** - From 1 to 1000+ greenhouses
7. **Real-Time Monitoring** - 24/7 visibility with <500ms latency
8. **Premium UX** - Beautiful, intuitive dashboard

---

## 📈 Roadmap to $100M Valuation

| Phase         | Timeline    | Goal                      | Funding          |
| ------------- | ----------- | ------------------------- | ---------------- |
| **MVP**       | Month 0-3   | RL agent + 1 facility     | Pre-seed $1-2M   |
| **Pilot**     | Month 4-8   | 10 pilots, $50k MRR       | Seed $8-15M      |
| **Expansion** | Month 9-14  | 100 facilities, $500k MRR | Series A $30-50M |
| **Platform**  | Month 15-18 | Carbon credits, $1.2M MRR | Series B         |

---

## 🤝 Mentorship & Collaboration

**Academic Mentor:**

- **Prof. Yu Jiang** - Cornell University, CALS Department
- Expertise: Agricultural systems, precision agriculture
- Role: Technical guidance on greenhouse operations, sensor calibration, agronomic validation

---

## 📞 Contact & Resources

- **Repository:** https://github.com/Chirag005/rala
- **Documentation:** [docs/](file:///e:/projects/rala/rala/docs/)
- **Email:** info@rala.systems (planned)
- **Website:** rala.systems (planned)

---

**Version:** 2.0.4-stable  
**Last Updated:** January 2026  
**Project Status:** Active Development - Hardware Integration Phase
