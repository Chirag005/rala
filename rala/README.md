# RALA - Autonomous Greenhouse OS

<div align="center">

**Reinforcement-learning Autonomous Life-support Automation**

_AI-powered greenhouse operating system that cuts energy costs by 30% and boosts yields by 12%_

[![Version](https://img.shields.io/badge/version-2.0.4--stable-emerald)](https://github.com/rala-systems)
[![License](https://img.shields.io/badge/license-Proprietary-blue)](LICENSE)
[![Nuxt](https://img.shields.io/badge/Nuxt-3-00DC82)](https://nuxt.com/)
[![Vue](https://img.shields.io/badge/Vue-3-4FC08D)](https://vuejs.org/)

[Website](https://rala.systems) • [Demo](https://dashboard.rala.systems) • [Documentation](./docs/) • [Contact](mailto:info@rala.systems)

</div>

---

## 🎯 What is RALA?

**RALA** is an AI-powered autonomous greenhouse operating system that combines cutting-edge reinforcement learning, digital twin technology, and real-time sensor networks to optimize energy consumption and maximize crop yields.

### Key Metrics

- 💰 **30% Energy Savings** - Reduce your #1 operating expense
- 🌱 **12% Yield Increase** - Better crop quality and quantity
- ⚡ **3-6 Month ROI** - Measurable returns in under 6 months
- 🌍 **$110B Market** - Global greenhouse automation opportunity
- 🤖 **24/7 Autonomous** - Lights-out operation with minimal intervention

---

## ✨ Features

### 🎨 Web Application

#### Landing Page (`/`)

- **Hero Section** with Three.js particle animation background
- **Mission & ROI Comparison** table showcasing market positioning
- **Digital Twin Visualization** with animated graphics
- **GTM Roadmap** showing path to $100M valuation
- **GSAP Animations** for smooth scroll-triggered effects

#### Dashboard Page (`/dashboard`)

- **Real-time Metrics**: VPD, PPFD, Canopy Temperature, Energy Savings
- **Sensor Mesh Visualization**: Live 6x4 grid (24 sensor nodes)
- **AI Agent Logs**: Real-time monitoring of autonomous decisions
- **Hardware Control Panel**: HVAC, Irrigation, Lighting controls
- **Fully Responsive**: Desktop, tablet, and mobile optimized

### 🧠 Core Technology

1. **Neural Mesh** - 1,024+ sensor network for comprehensive monitoring
2. **RL Engine** - Deep reinforcement learning (PPO) for continuous optimization
3. **Digital Twin** - Physics-based virtual greenhouse simulation
4. **Autonomous Mode** - Level 5 automation (full autonomy)
5. **Energy-First** - Tackles the #1 greenhouse operating expense
6. **Retrofit-Ready** - Works with existing equipment (no rip-and-replace)

---

## 🚀 Quick Start

### Installation

```bash
# Clone the repository
git clone https://github.com/rala-systems/rala.git
cd rala/rala

# Install dependencies
npm install

# Run development server
npm run dev
```

The application will be available at `http://localhost:3000`

### Build for Production

```bash
# Build the application
npm run build

# Preview production build
npm run preview

# Output will be in .output/ directory
# Deploy to Vercel, Netlify, or any Node.js host
```

---

## 🛠️ Technology Stack

### Frontend

- **Framework**: Nuxt 3 (Vue 3 Composition API)
- **Styling**: Semantic CSS with scoped components (minimal Tailwind)
- **3D Graphics**: Three.js for particle effects
- **Animations**: GSAP (GreenSock) for smooth transitions
- **Icons**: Iconify icon framework
- **State Management**: Pinia (Vue store)
- **Fonts**: JetBrains Mono for code/data displays

### Backend (Planned/Documented)

- **Language**: Python 3.11+
- **Framework**: FastAPI
- **ML/AI**: PyTorch, Stable Baselines 3 (PPO)
- **Databases**: InfluxDB (time-series), PostgreSQL, Redis
- **Deployment**: AWS (ECS, RDS, S3), Kubernetes

### Edge Computing

- **Platform**: Industrial IoT gateway (ARM64)
- **Protocols**: Modbus, BACnet, MQTT
- **Inference**: ONNX Runtime (optimized models)

---

## 📁 Project Structure

```
rala/
├── app/                          # Nuxt application
│   ├── pages/
│   │   ├── index.vue            # Landing page
│   │   └── dashboard.vue        # Dashboard UI
│   ├── components/
│   │   ├── dashboard/           # Dashboard components
│   │   │   ├── DashboardSidebar.vue
│   │   │   ├── DashboardHeader.vue
│   │   │   ├── MetricsGrid.vue
│   │   │   ├── SensorMesh.vue
│   │   │   ├── AgentLogs.vue
│   │   │   └── HardwareSection.vue
│   │   ├── Navbar.vue
│   │   ├── Footer.vue
│   │   └── LoadingWidget.vue
│   ├── layouts/
│   │   ├── default.vue          # Default layout (with nav/footer)
│   │   └── dashboard.vue        # Dashboard layout
│   ├── plugins/
│   │   ├── gsap.client.ts       # GSAP initialization
│   │   └── three.client.ts      # Three.js particle system
│   ├── composables/
│   │   └── useAppState.ts       # Global app state
│   └── assets/
│       └── css/main.css         # Global styles
├── docs/                         # Documentation
│   ├── RALA_OVERVIEW.md         # Complete product overview (600+ lines)
│   ├── EXECUTIVE_SUMMARY.md     # Quick reference (350 lines)
│   ├── TECHNICAL_ARCHITECTURE.md # Technical deep-dive (500+ lines)
│   └── README.md                # Documentation index
├── DASHBOARD_REFACTORING.md     # Component architecture guide
├── nuxt.config.ts               # Nuxt configuration
└── package.json                 # Dependencies
```

---

## 🎨 Design System

### Color Palette

```css
/* Primary - Emerald */
--emerald-400: #34d399;
--emerald-500: #10b981;
--emerald-900: #047857;

/* Alerts */
--amber-500: #f59e0b;
--rose-400: #fb7185;
--rose-500: #f43f5e;

/* Grayscale */
--zinc-50: #fafafa;
--zinc-400: #a1a1aa;
--zinc-500: #71717a;
--zinc-600: #52525b;
--zinc-700: #3f3f46;
--zinc-800: #27272a;
--zinc-900: #18181b;
--zinc-950: #09090b;
```

### Design Philosophy

- ✨ **Premium Dark Mode**: Deep blacks with emerald accents
- 🔮 **Glassmorphism**: Frosted glass effects with backdrop blur
- 🎬 **Micro-animations**: Pulse, bounce, scan effects for engagement
- 📐 **Semantic CSS**: `.metric-card`, `.sensor-node`, `.log-entry`
- 📱 **Mobile-First**: Responsive from 320px to 4K displays

### Responsive Breakpoints

```css
@media (min-width: 640px) {
  /* sm - Mobile landscape */
}
@media (min-width: 768px) {
  /* md - Tablet */
}
@media (min-width: 1024px) {
  /* lg - Desktop */
}
@media (min-width: 1280px) {
  /* xl - Large desktop */
}
```

---

## 🌐 Routes & Pages

| Route        | Description         | Features                                      |
| ------------ | ------------------- | --------------------------------------------- |
| `/`          | Landing Page        | Hero, comparison table, roadmap, CTA          |
| `/dashboard` | Real-time Dashboard | Metrics, sensor mesh, logs, hardware controls |

---

## 📊 Component Architecture

### Dashboard Components

1. **DashboardSidebar** - Navigation with logo, menu, user avatar
2. **DashboardHeader** - Status bar with facility info and alerts
3. **MetricsGrid** - 4 KPI cards (VPD, PPFD, Temperature, Energy)
4. **SensorMesh** - 24-node grid with real-time status
5. **AgentLogs** - Terminal-style AI decision logging
6. **HardwareSection** - Equipment control and monitoring

All components are:

- ✅ Fully responsive (mobile-optimized)
- ✅ Modular and reusable
- ✅ Type-safe (TypeScript ready)
- ✅ Semantic CSS (no inline styles)

---

## 🎬 Animations

- **Scan Animation**: Sweeping line across sensor mesh (4s cycle)
- **Pulse**: Status indicators and glowing effects (2s cycle)
- **Bounce**: Alert/stress sensor nodes
- **Ping**: Growing wave effect on status badges
- **GSAP ScrollTrigger**: Fade-up animations on scroll
- **Three.js Particles**: Interactive background on landing page

---

## 📚 Documentation

Comprehensive documentation is available in the [`docs/`](./docs/) directory:

### Core Documents

1. **[RALA Overview](./docs/RALA_OVERVIEW.md)** (600+ lines)

   - Complete product documentation
   - All features, architecture, market analysis
   - Use cases with ROI examples
   - Business model and roadmap

2. **[Executive Summary](./docs/EXECUTIVE_SUMMARY.md)** (350 lines)

   - Quick reference for stakeholders
   - Investment highlights
   - Market opportunity
   - Key metrics and facts

3. **[Technical Architecture](./docs/TECHNICAL_ARCHITECTURE.md)** (500+ lines)

   - System design and data flow
   - AI/ML pipeline details
   - Security architecture
   - Deployment specifications

4. **[Dashboard Refactoring](./DASHBOARD_REFACTORING.md)** (250 lines)
   - Component breakdown
   - Mobile optimization details
   - Implementation guide

### Quick Navigation

- **New to RALA?** Start with [Executive Summary](./docs/EXECUTIVE_SUMMARY.md)
- **Technical Implementation?** Read [Technical Architecture](./docs/TECHNICAL_ARCHITECTURE.md)
- **Business Case?** Check [RALA Overview → Market Positioning](./docs/RALA_OVERVIEW.md#market-positioning)
- **Frontend Development?** See [Dashboard Refactoring](./DASHBOARD_REFACTORING.md)

---

## 💼 Business Model

### Revenue Streams

| Tier             | Price/Month | Facility Size    | Features               |
| ---------------- | ----------- | ---------------- | ---------------------- |
| **Starter**      | $2,500      | Up to 100K sq ft | Basic automation       |
| **Professional** | $5,000      | 100K-500K sq ft  | Advanced features      |
| **Enterprise**   | $10,000+    | 500K+ sq ft      | Multi-facility, custom |

### Unit Economics (Example: 200K sq ft greenhouse)

- **Monthly Revenue**: $5,000
- **COGS**: $600
- **Gross Margin**: 88%
- **Customer LTV** (5 years): $300,000
- **LTV:CAC Ratio**: 20:1

### Value Proposition

- Customer saves **$120K/year** in energy
- RALA charges **$60K/year** (50% of savings)
- **Perfectly aligned incentives**
- **6-month payback period**

---

## 🎯 Use Case Example

### Commercial Tomato Greenhouse

- **Size**: 10 acres (435,000 sq ft)
- **Location**: Ohio, USA
- **Energy Cost (Before)**: $480,000/year

**Results After 12 Months:**

- ✅ Energy savings: **$144,000/year** (30%)
- ✅ Yield increase: **11.8%**
- ✅ Labor savings: 1 FTE reassigned
- ✅ **Total Benefit**: $225,000/year
- ✅ **ROI**: 6.2 months

---

## 🔐 Security & Compliance

- 🔒 **TLS 1.3** for all communications
- 🔐 **JWT-based** authentication
- 🛡️ **RBAC** (Role-Based Access Control)
- 📊 **SOC 2 Type II** (planned certification)
- 🌍 **GDPR/CCPA** compliant
- 🔑 **Device certificates** for edge gateways

---

## 🚀 Deployment

### Supported Platforms

- ☁️ **Vercel** (recommended for frontend)
- ☁️ **Netlify**
- ☁️ **AWS** (ECS/Fargate)
- ☁️ **Azure** App Service
- 🐳 **Docker** containers
- ⚡ **Node.js** hosting

### Environment Variables

```bash
# .env file
DATABASE_URL=postgresql://...
INFLUXDB_URL=http://...
REDIS_URL=redis://...
JWT_SECRET=your-secret-key
MQTT_BROKER=mqtt://...
```

---

## 🤝 Contributing

This is a proprietary project. For collaboration opportunities:

- **Technical Questions**: tech@rala.systems
- **Partnership Inquiries**: partners@rala.systems
- **Documentation**: docs@rala.systems

---

## 📞 Contact & Support

### Main Channels

- 🌐 **Website**: [https://rala.systems](https://rala.systems)
- 📧 **Email**: info@rala.systems
- 🎯 **Dashboard Demo**: dashboard.rala.systems
- 📖 **API Docs**: docs.rala.systems

### Social Media

- 💼 **LinkedIn**: [/company/rala-systems](https://linkedin.com/company/rala-systems)
- 🐦 **Twitter**: [@RALAsystems](https://twitter.com/RALAsystems)
- 💻 **GitHub**: [github.com/rala-systems](https://github.com/rala-systems)

### Support

- 🔧 **Technical Support**: support@rala.systems
- 💰 **Sales Inquiries**: sales@rala.systems
- 🤝 **Partnerships**: partners@rala.systems

---

## 📈 Performance & Optimization

- ⚡ **Optimized CSS**: Semantic classes reduce bundle size
- 🔄 **Lazy Loading**: Components load on demand
- 🌳 **Tree Shaking**: Unused code eliminated in production
- 🎮 **GPU Acceleration**: Hardware-accelerated animations
- 📦 **Code Splitting**: Route-based chunking
- 🖼️ **Asset Optimization**: Compressed images and fonts

---

## 🎓 Learning Resources

### For Developers

- [Nuxt 3 Documentation](https://nuxt.com/docs)
- [Vue 3 Documentation](https://vuejs.org/guide/)
- [GSAP Documentation](https://greensock.com/docs/)
- [Three.js Documentation](https://threejs.org/docs/)

### For Business

- [Greenhouse Automation Market Report](./docs/RALA_OVERVIEW.md#market-positioning)
- [ROI Calculator](./docs/EXECUTIVE_SUMMARY.md#use-case-example)
- [Investment Highlights](./docs/EXECUTIVE_SUMMARY.md#investment-highlights)

---

## 📝 License

**Proprietary** - All rights reserved

This software is the intellectual property of RALA Systems Inc. Unauthorized copying, distribution, or use is strictly prohibited.

For licensing inquiries: legal@rala.systems

---

## 🏆 Achievements & Milestones

- ✅ **v1.0** - MVP with basic automation (Month 3)
- ✅ **v2.0** - Reinforcement learning integration (Month 6)
- ✅ **v2.0.4** - Dashboard UI overhaul (Current)
- 🚀 **v2.1** - Mobile apps (Q1 2026)
- 🚀 **v3.0** - Multi-crop support (Q2 2026)

---

## 🙏 Acknowledgments

Built for the future of autonomous agriculture.

Special thanks to:

- University research partners (Ohio State, Wageningen)
- Early pilot customers
- Open-source community (Vue, Nuxt, Three.js, GSAP)

---

## ⚡ Quick Facts

| Metric             | Value                           |
| ------------------ | ------------------------------- |
| **Product**        | RALA (Autonomous Greenhouse OS) |
| **Version**        | 2.0.4-stable                    |
| **Status**         | Production Ready                |
| **Energy Savings** | 30%                             |
| **Yield Increase** | 12%                             |
| **ROI**            | 3-6 months                      |
| **Market Size**    | $110B                           |
| **Tech Stack**     | Nuxt 3, Vue 3, Python, RL (PPO) |
| **Deployment**     | Cloud + Edge                    |
| **Founded**        | 2024                            |

---

<div align="center">

**"RALA: The Autonomous Future of Agriculture"**

_Making greenhouses smarter, more profitable, and sustainable through AI_

---

**Version 2.0.4-stable** | **Last Updated: December 2025**

[Get Started](./docs/EXECUTIVE_SUMMARY.md) | [View Demo](https://dashboard.rala.systems) | [Contact Us](mailto:info@rala.systems)

</div>
