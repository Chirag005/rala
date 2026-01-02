# RALA - Technical Architecture Documentation

## Table of Contents

1. [System Overview](#system-overview)
2. [Architecture Layers](#architecture-layers)
3. [Component Details](#component-details)
4. [Data Flow](#data-flow)
5. [AI/ML Pipeline](#aiml-pipeline)
6. [Security Architecture](#security-architecture)
7. [Deployment Architecture](#deployment-architecture)
8. [API Specifications](#api-specifications)
9. [Database Schema](#database-schema)
10. [Monitoring & Observability](#monitoring--observability)

---

## System Overview

### High-Level Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                          RALA Platform                          │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  ┌──────────────┐    ┌──────────────┐    ┌──────────────┐    │
│  │   Frontend   │◄───│   API Layer  │◄───│   Services   │    │
│  │   (Nuxt 3)   │    │   (FastAPI)  │    │   (Python)   │    │
│  └──────────────┘    └──────────────┘    └──────────────┘    │
│         ▲                    ▲                    ▲            │
│         │                    │                    │            │
│         └────────────────────┴────────────────────┘            │
│                              │                                  │
│                              ▼                                  │
│  ┌────────────────────────────────────────────────────────┐   │
│  │              Data & ML Infrastructure                  │   │
│  │  ┌──────────┐  ┌──────────┐  ┌───────────────────┐  │   │
│  │  │InfluxDB  │  │PostgreSQL│  │  Training Pipeline│  │   │
│  │  │(Sensors) │  │  (Users) │  │  (RL/ML Models)   │  │   │
│  │  └──────────┘  └──────────┘  └───────────────────┘  │   │
│  └────────────────────────────────────────────────────────┘   │
│                              │                                  │
│                              ▼                                  │
│  ┌────────────────────────────────────────────────────────┐   │
│  │              Edge Deployment Layer                     │   │
│  │        (MQTT, WebSockets, HTTP/REST)                   │   │
│  └────────────────────────────────────────────────────────┘   │
└─────────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────────┐
│                    Greenhouse Edge Gateway                     │
│  ┌─────────────┐  ┌─────────────┐  ┌──────────────────────┐  │
│  │   Sensors   │  │Control Logic│  │  Local ML Inference  │  │
│  │(Modbus/BACnet)│ │(MQTT Client)│  │   (ONNX Runtime)     │  │
│  └─────────────┘  └─────────────┘  └──────────────────────┘  │
└─────────────────────────────────────────────────────────────────┘
                              │
                              ▼
                    ┌──────────────────┐
                    │Physical Equipment│
                    │ HVAC | Lighting  │
                    │   Irrigation     │
                    └──────────────────┘
```

---

## Architecture Layers

### 1. **Presentation Layer** (Client-Side)

#### Web Application

- **Framework**: Nuxt 3 (Vue 3 Composition API)
- **State Management**: Pinia (Vue store)
- **Routing**: File-based (Nuxt auto-routing)
- **Styling**: Semantic CSS with scoped components
- **Real-Time**: WebSocket connection for live updates

#### Mobile Applications

- **iOS**: SwiftUI + Combine
- **Android**: Jetpack Compose + Kotlin Flow
- **Shared Logic**: REST API clients

---

### 2. **API Layer** (Gateway)

#### FastAPI Service

**Responsibilities**

- Authentication & authorization
- Request validation
- Rate limiting
- API versioning
- WebSocket gateway

**Endpoints Structure**

```
/api/v1/
├── /auth/          # Authentication
├── /facilities/    # Facility management
├── /sensors/       # Sensor data
├── /controls/      # Equipment control
├── /analytics/     # Performance metrics
├── /ml/            # Model management
└── /ws/            # WebSocket connections
```

**Technology Stack**

```python
# Core
FastAPI==0.104.0
Pydantic==2.5.0  # Request/response validation
SQLAlchemy==2.0.0  # ORM

# Auth
python-jose[cryptography]==3.3.0  # JWT tokens
passlib[bcrypt]==1.7.4  # Password hashing

# Communication
websockets==12.0
redis==5.0.1  # Pub/sub for real-time
celery==5.3.4  # Async tasks

# Monitoring
prometheus-client==0.19.0
sentry-sdk==1.38.0
```

---

### 3. **Service Layer** (Business Logic)

#### Core Services

**1. SensorService**

```python
class SensorService:
    """Handles all sensor data operations"""

    async def ingest_data(self, sensor_id, data):
        # Validate data
        # Store in InfluxDB
        # Trigger anomaly detection
        # Publish to WebSocket subscribers
        pass

    async def get_historical(self, sensor_id, start, end):
        # Query InfluxDB
        # Apply aggregations
        # Return time-series data
        pass
```

**2. ControlService**

```python
class ControlService:
    """Equipment control and automation"""

    async def execute_action(self, facility_id, action):
        # Validate permissions
        # Send command to edge gateway (MQTT)
        # Log action
        # Update digital twin
        pass

    async def get_schedule(self, facility_id):
        # Return upcoming automated actions
        pass
```

**3. MLService**

```python
class MLService:
    """ML model management and inference"""

    async def get_recommendation(self, facility_id):
        # Fetch current state from digital twin
        # Run RL model inference
        # Return optimized setpoints
        pass

    async def train_model(self, facility_id):
        # Fetch historical data
        # Trigger training pipeline
        # Deploy updated model
        pass
```

**4. DigitalTwinService**

```python
class DigitalTwinService:
    """Manages virtual greenhouse replicas"""

    async def simulate(self, facility_id, scenario):
        # Run thermodynamic simulation
        # Predict outcomes
        # Return results
        pass

    async def calibrate(self, facility_id):
        # Compare predictions vs. actuals
        # Adjust model parameters
        pass
```

---

### 4. **Data Layer**

#### InfluxDB (Time-Series Database)

**Schema Design**

```
Measurement: sensor_readings
├── Tags (Indexed)
│   ├── facility_id
│   ├── zone_id
│   ├── sensor_type
│   └── sensor_id
├── Fields
│   ├── temperature (float)
│   ├── humidity (float)
│   ├── co2 (int)
│   ├── ppfd (float)
│   ├── vpd (float)
│   └── soil_moisture (float)
└── Timestamp (nanosecond precision)

Measurement: equipment_state
├── Tags
│   ├── facility_id
│   ├── equipment_id
│   └── equipment_type
├── Fields
│   ├── state (string: on/off/auto)
│   ├── setpoint (float)
│   ├── actual (float)
│   └── power_consumption (float)
└── Timestamp

Measurement: ml_predictions
├── Tags
│   ├── facility_id
│   ├── model_version
│   └── prediction_type
├── Fields
│   ├── predicted_value (float)
│   ├── confidence (float)
│   └── actual_value (float, filled later)
└── Timestamp
```

**Retention Policies**

```sql
-- High-resolution (1 minute): 7 days
CREATE RETENTION POLICY "high_res" ON "rala" DURATION 7d REPLICATION 1 DEFAULT

-- Medium-resolution (5 minutes): 90 days
CREATE RETENTION POLICY "medium_res" ON "rala" DURATION 90d REPLICATION 1

-- Low-resolution (1 hour): Forever
CREATE RETENTION POLICY "long_term" ON "rala" DURATION INF REPLICATION 1
```

**Continuous Queries** (Downsampling)

```sql
-- Downsample to 5-minute averages
CREATE CONTINUOUS QUERY "cq_5min_avg" ON "rala"
BEGIN
  SELECT mean(*) INTO "medium_res".:MEASUREMENT FROM "high_res"./.*/
  GROUP BY time(5m), *
END

-- Downsample to 1-hour averages
CREATE CONTINUOUS QUERY "cq_1hour_avg" ON "rala"
BEGIN
  SELECT mean(*) INTO "long_term".:MEASUREMENT FROM "medium_res"./.*/
  GROUP BY time(1h), *
END
```

#### PostgreSQL (Relational Database)

**Schema**

```sql
-- Users & Authentication
CREATE TABLE users (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    email VARCHAR(255) UNIQUE NOT NULL,
    password_hash VARCHAR(255) NOT NULL,
    created_at TIMESTAMPTZ DEFAULT NOW(),
    last_login TIMESTAMPTZ
);

-- Facilities
CREATE TABLE facilities (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    name VARCHAR(255) NOT NULL,
    location GEOMETRY(POINT, 4326),  -- PostGIS for geospatial
    size_sqft INTEGER,
    crop_type VARCHAR(100),
    owner_id UUID REFERENCES users(id),
    created_at TIMESTAMPTZ DEFAULT NOW()
);

-- Equipment Inventory
CREATE TABLE equipment (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    facility_id UUID REFERENCES facilities(id),
    equipment_type VARCHAR(50),  -- hvac, lighting, irrigation
    model VARCHAR(100),
    install_date DATE,
    protocol VARCHAR(20),  -- modbus-rtu, bacnet-ip, etc.
    address TEXT,  -- Connection details (JSON)
    specs JSONB  -- Equipment specifications
);

-- Sensors
CREATE TABLE sensors (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    facility_id UUID REFERENCES facilities(id),
    zone_id VARCHAR(50),
    sensor_type VARCHAR(50),
    location GEOMETRY(POINT, 4326),  -- Position within facility
    calibration_date DATE,
    specs JSONB
);

-- ML Models
CREATE TABLE ml_models (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    facility_id UUID REFERENCES facilities(id),
    model_type VARCHAR(50),  -- rl_ppo, yield_pred, etc.
    version VARCHAR(20),
    accuracy_metrics JSONB,
    deployed_at TIMESTAMPTZ,
    model_path TEXT  -- S3 bucket path
);

-- Alerts
CREATE TABLE alerts (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    facility_id UUID REFERENCES facilities(id),
    alert_type VARCHAR(50),
    severity VARCHAR(20),  -- info, warning, critical
    message TEXT,
    acknowledged BOOLEAN DEFAULT FALSE,
    created_at TIMESTAMPTZ DEFAULT NOW()
);

-- Performance Metrics (Aggregated)
CREATE TABLE daily_metrics (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    facility_id UUID REFERENCES facilities(id),
    date DATE NOT NULL,
    energy_kwh FLOAT,
    energy_cost FLOAT,
    energy_saved_kwh FLOAT,
    yield_kg FLOAT,
    vpd_avg FLOAT,
    temp_avg FLOAT,
    UNIQUE(facility_id, date)
);
```

#### Redis (Caching & Pub/Sub)

**Usage**

```python
# Cache frequently accessed data
redis.setex('facility:123:config', 3600, json.dumps(config))

# Pub/Sub for real-time updates
redis.publish('facility:123:sensors', json.dumps(sensor_data))

# Rate limiting
redis.incr('api:user:456:requests', expire=60)

# Session management
redis.setex('session:token123', 86400, user_id)
```

---

## AI/ML Pipeline

### Reinforcement Learning Architecture

#### 1. **Training Pipeline** (Cloud)

```python
# Training workflow
class RLTrainingPipeline:
    def __init__(self, facility_id):
        self.facility_id = facility_id
        self.env = GreenhouseSimEnv(facility_id)  # Digital twin
        self.model = PPO("MlpPolicy", self.env, verbose=1)

    def train(self, total_timesteps=1000000):
        # Load historical data
        historical_data = self.load_data()

        # Train in simulation
        self.model.learn(total_timesteps=total_timesteps)

        # Validate performance
        metrics = self.validate()

        # Export to ONNX for edge deployment
        self.export_onnx()

        return metrics

    def validate(self):
        # Test on held-out data
        # Ensure safety constraints
        # Compare vs. baseline
        pass
```

**Environment Definition**

```python
class GreenhouseSimEnv(gym.Env):
    """Custom OpenAI Gym environment for greenhouse"""

    def __init__(self, facility_config):
        # State space: [temp, humidity, co2, vpd, solar, ...]
        self.observation_space = spaces.Box(
            low=np.array([0, 0, 200, 0, 0]),
            high=np.array([40, 100, 2000, 3, 1200]),
            dtype=np.float32
        )

        # Action space: [hvac_setpoint, light_intensity, co2_flow]
        self.action_space = spaces.Box(
            low=np.array([15, 0, 0]),
            high=np.array([30, 100, 10]),
            dtype=np.float32
        )

        self.digital_twin = DigitalTwin(facility_config)

    def step(self, action):
        # Apply action to digital twin
        next_state = self.digital_twin.simulate(action)

        # Calculate reward
        energy_cost = self.digital_twin.get_energy_cost()
        crop_health = self.digital_twin.get_crop_score()

        # Multi-objective reward
        reward = -energy_cost + 0.5 * crop_health

        # Check if done (end of grow cycle)
        done = self.digital_twin.is_cycle_complete()

        return next_state, reward, done, {}

    def reset(self):
        return self.digital_twin.reset()
```

#### 2. **Inference Pipeline** (Edge)

```python
class EdgeInference:
    def __init__(self, model_path):
        # Load ONNX model
        self.session = onnxruntime.InferenceSession(model_path)

    def predict(self, current_state):
        # Normalize inputs
        state_normalized = self.normalize(current_state)

        # Run inference
        input_name = self.session.get_inputs()[0].name
        output = self.session.run(None, {input_name: state_normalized})

        # Denormalize actions
        actions = self.denormalize(output[0])

        # Apply safety constraints
        actions_safe = self.apply_constraints(actions)

        return actions_safe

    def apply_constraints(self, actions):
        # Ensure actions are within safe operating ranges
        # E.g., don't exceed equipment capacity
        # Don't create dangerous conditions
        pass
```

### Digital Twin Simulator

```python
class DigitalTwin:
    """Physics-based greenhouse simulation"""

    def __init__(self, facility_config):
        self.config = facility_config
        self.state = self.initial_state()

    def simulate(self, action, timestep=60):
        """
        Simulate greenhouse for given timestep (seconds)

        Args:
            action: [hvac_setpoint, light_intensity, co2_flow]
            timestep: Simulation timestep in seconds

        Returns:
            next_state: Updated environmental state
        """
        # Unpack action
        T_setpoint, I_light, CO2_flow = action

        # Weather data (from API or forecast)
        T_outdoor, RH_outdoor, I_solar = self.get_weather()

        # Energy balance
        Q_solar = self.calc_solar_gain(I_solar)
        Q_lights = self.calc_light_heat(I_light)
        Q_hvac = self.calc_hvac_load(T_setpoint, T_outdoor)
        Q_crop = self.calc_crop_transpiration()

        # Temperature dynamics
        dT_dt = (Q_solar + Q_lights - Q_hvac - Q_crop) / self.thermal_mass
        T_new = self.state['temperature'] + dT_dt * timestep

        # Humidity dynamics
        # (Penman-Monteith ET + ventilation mixing)
        dRH_dt = self.calc_humidity_change(T_new, RH_outdoor)
        RH_new = self.state['humidity'] + dRH_dt * timestep

        # CO2 dynamics
        # (Photosynthesis uptake + injection + ventilation)
        dCO2_dt = CO2_flow - self.calc_photosynthesis_rate() + self.calc_respiration()
        CO2_new = self.state['co2'] + dCO2_dt * timestep

        # Update state
        self.state = {
            'temperature': T_new,
            'humidity': RH_new,
            'co2': CO2_new,
            'vpd': self.calc_vpd(T_new, RH_new)
        }

        return self.state

    def calc_photosynthesis_rate(self):
        """Tomich-style photosynthesis model"""
        # Based on current light, CO2, temperature
        pass

    def get_energy_cost(self):
        """Calculate energy consumption in current state"""
        # kWh from HVAC, lights
        # Apply electricity rates (time-of-use)
        pass
```

---

## Data Flow

### Real-Time Sensor Data Flow

```
[ Sensor ] → [ Edge Gateway ] → [ MQTT Broker ] → [ Cloud Ingestion Service ]
                    ↓                                         ↓
            [ Local RL Model ]                        [ InfluxDB ]
                    ↓                                         ↓
            [ Equipment Control ]                [ WebSocket Broadcast ]
                    ↓                                         ↓
            [ Physical Equipment ]                    [ Dashboard ]
```

**Step-by-Step**

1. **Sensor Reading** (every 30 seconds)

   - Modbus/BACnet query
   - Data validation
   - Timestamp assignment

2. **Edge Processing**

   - Anomaly detection (local)
   - RL model inference (if in autonomous mode)
   - Safety check

3. **MQTT Publish**

   - Topic: `facility/{id}/sensors/{type}`
   - QoS level 1 (at least once delivery)
   - Retain flag for latest value

4. **Cloud Ingestion**

   - Subscribe to MQTT topics
   - Batch insert to InfluxDB (every 5 seconds)
   - Trigger alerts if thresholds exceeded

5. **Dashboard Update**
   - WebSocket push to connected clients
   - React component re-render
   - Chart update

### Control Command Flow

```
[ Dashboard User Action ] → [ API POST /controls/execute ]
                ↓
        [ Authentication & Authorization ]
                ↓
        [ Validation & Safety Check ]
                ↓
        [ MQTT Publish to Edge ]
                ↓
        [ Edge Gateway Receives ]
                ↓
        [ Execute via Modbus/BACnet ]
                ↓
        [ Verify Execution ]
                ↓
        [ Confirm to Cloud/User ]
```

---

## Security Architecture

### Authentication & Authorization

**JWT-Based Auth**

```python
# Login flow
@router.post("/auth/login")
async def login(credentials: LoginCredentials):
    user = await authenticate_user(credentials.email, credentials.password)
    if not user:
        raise HTTPException(401, "Invalid credentials")

    # Generate JWT
    access_token = create_access_token(
        data={"sub": str(user.id)},
        expires_delta=timedelta(hours=1)
    )
    refresh_token = create_refresh_token(
        data={"sub": str(user.id)},
        expires_delta=timedelta(days=30)
    )

    return {
        "access_token": access_token,
        "refresh_token": refresh_token,
        "token_type": "bearer"
    }

# Protected endpoint
@router.get("/facilities/", dependencies=[Depends(get_current_user)])
async def get_facilities(user: User = Depends(get_current_user)):
    return await facility_service.get_by_user(user.id)
```

**Role-Based Access Control (RBAC)**

```python
class UserRole(Enum):
    ADMIN = "admin"        # Full access
    OPERATOR = "operator"  # Control equipment
    VIEWER = "viewer"      # Read-only

@router.post("/controls/execute")
async def execute_control(
    action: ControlAction,
    user: User = Depends(require_role(UserRole.OPERATOR))
):
    # Only operators+ can control equipment
    pass
```

### Data Encryption

**In Transit**

- TLS 1.3 for all HTTP/WebSocket connections
- MQTT over TLS for edge communication
- Certificate pinning on mobile apps

**At Rest**

- Database encryption (PostgreSQL built-in)
- InfluxDB encryption at rest
- S3 server-side encryption for ML models

### Edge Security

**Gateway Hardening**

- Minimal OS (Ubuntu Server, no desktop)
- Firewall rules (only outbound MQTT/HTTP)
- Auto-updates for security patches
- No SSH by default (console access only)

**Device Authentication**

- Unique device certificates
- Mutual TLS (mTLS) for MQTT
- Revocation list for compromised devices

---

## Deployment Architecture

### Cloud Infrastructure (AWS)

```
┌─────────────────────── VPC ────────────────────────┐
│                                                     │
│  ┌──────────── Public Subnet ──────────────┐      │
│  │                                           │      │
│  │  [ CloudFront CDN ]                       │      │
│  │        ↓                                  │      │
│  │  [ Application Load Balancer ]           │      │
│  │                                           │      │
│  └───────────────────────────────────────────┘      │
│                    ↓                                │
│  ┌──────────── Private Subnet ─────────────┐       │
│  │                                           │      │
│  │  ┌──────────┐  ┌──────────┐             │      │
│  │  │ ECS Task │  │ ECS Task │             │      │
│  │  │ (FastAPI)│  │ (FastAPI)│ Auto-scaling│      │
│  │  └──────────┘  └──────────┘             │      │
│  │                                           │      │
│  │  ┌──────────┐  ┌──────────┐             │      │
│  │  │  RDS      │  │ ElastiCache            │      │
│  │  │(Postgres) │  │  (Redis)  │             │      │
│  │  └──────────┘  └──────────┘             │      │
│  │                                           │      │
│  └───────────────────────────────────────────┘      │
│                                                     │
│  ┌──────────── Data Tier ───────────────────┐      │
│  │                                           │      │
│  │  [ InfluxDB ]  [ S3 ]  [ SageMaker ]      │      │
│  │                                           │      │
│  └───────────────────────────────────────────┘      │
└─────────────────────────────────────────────────────┘
```

**Kubernetes Deployment (EKS)**

```yaml
# api-deployment.yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: rala-api
spec:
  replicas: 3
  selector:
    matchLabels:
      app: rala-api
  template:
    metadata:
      labels:
        app: rala-api
    spec:
      containers:
        - name: api
          image: rala/api:2.0.4
          ports:
            - containerPort: 8000
          env:
            - name: DATABASE_URL
              valueFrom:
                secretKeyRef:
                  name: rala-secrets
                  key: database-url
          resources:
            requests:
              memory: "256Mi"
              cpu: "250m"
            limits:
              memory: "512Mi"
              cpu: "500m"
          livenessProbe:
            httpGet:
              path: /health
              port: 8000
            initialDelaySeconds: 30
            periodSeconds: 10
```

---

## Monitoring & Observability

### Metrics Collection

**Prometheus Metrics**

```python
from prometheus_client import Counter, Histogram, Gauge

# API metrics
api_requests = Counter('rala_api_requests_total', 'Total API requests', ['method', 'endpoint','status'])
api_latency = Histogram('rala_api_latency_seconds', 'API latency')

# Business metrics
facilities_active = Gauge('rala_facilities_active', 'Number of active facilities')
energy_saved = Counter('rala_energy_saved_kwh_total', 'Total energy saved')
```

### Logging

**Structured Logging**

```python
import structlog

logger = structlog.get_logger()

logger.info(
    "control_executed",
    facility_id=facility.id,
    action=action.type,
    user_id=user.id,
    duration_ms=duration
)
```

### Alerting

**PagerDuty Integration**

- Critical: Edge gateway offline >5 minutes
- High: API latency >2 seconds
- Medium: Sensor data gap >10 minutes
- Low: Model accuracy degradation

---

_This is a living document. Last updated: December 2025_  
_For questions: tech@rala.systems_
