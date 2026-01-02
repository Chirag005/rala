<template>
  <div class="app-container">
    <main class="main-content">
      
      <!-- Hero Section with Particle Canvas -->
      <section class="hero-section">
        <!-- Canvas Background -->
        <canvas ref="particleCanvas" class="particle-canvas"></canvas>
        <div class="hero-gradient"></div>
        
        <div class="hero-content">
          <div class="version-pill fade-up-element">
            <span class="version-ping">
              <span class="ping-wave"></span>
              <span class="ping-dot"></span>
            </span>
            v2.0 Energy Optimization Agent
          </div>
          
          <h1 class="hero-title fade-up-element">
            Autonomous<br>
            <span class="text-highlight">Greenhouse OS</span>
          </h1>
          
          <p class="hero-desc fade-up-element">
            AI Agents + RL + Digital Twins. Cut energy costs by <span class="text-white">30%</span> and boost yields by <span class="text-white">12%</span>. Immediate savings on your #1 operating expense.
          </p>

          <div class="hero-buttons fade-up-element">
            <button class="btn-primary">
              See the Demo
            </button>
            <button class="btn-secondary group">
              <span>Read the Whitepaper</span>
              <iconify-icon icon="lucide:arrow-right" class="arrow-icon"></iconify-icon>
            </button>
          </div>
        </div>
      </section>

      <!-- Mission / ROI Section -->
      <section id="mission" class="mission-section">
        <div class="mission-glow"></div>
        
        <div class="container-wrapper">
          <div class="mission-header fade-up-element">
            <h2 class="section-title">Why Energy Optimization First?</h2>
            <p class="section-desc">
              In a <span class="text-white">$110B market</span>, we're the agent automating physical processes. 
              <br class="hidden-mobile">Measurable ROI in under 30 days.
            </p>
          </div>

          <!-- Comparison Table -->
          <div id="comparison" class="comparison-container fade-up-element">
            <div class="table-wrapper">
              <table class="data-table">
                <thead>
                  <tr class="table-header-row">
                    <th class="th-criteria">Criteria (2025 Lens)</th>
                    <th class="th-basic">Yield Prediction</th>
                    <th class="th-basic">Pest Detection</th>
                    <th class="th-primary">Energy Optimization</th>
                  </tr>
                </thead>
                <tbody>
                  <tr class="table-row">
                    <td class="td-label">Market Size</td>
                    <td class="td-value">$25B</td>
                    <td class="td-value">$12B</td>
                    <td class="td-highlight">$110B</td>
                  </tr>
                  <tr class="table-row">
                    <td class="td-label">ROI Speed</td>
                    <td class="td-value">6-12 Months</td>
                    <td class="td-value">3-9 Months</td>
                    <td class="td-highlight">3-6 Months</td>
                  </tr>
                  <tr class="table-row">
                    <td class="td-label">Investor Buzz</td>
                    <td class="td-value">Common</td>
                    <td class="td-value">Saturated</td>
                    <td class="td-highlight">High (YC RFS #1)</td>
                  </tr>
                  <tr class="table-row">
                    <td class="td-label">Proof of Value</td>
                    <td class="td-value">Hard to measure</td>
                    <td class="td-value">Seasonal</td>
                    <td class="td-highlight">Immediate $ Savings</td>
                  </tr>
                  <tr class="table-row">
                    <td class="td-label">Valuation Multiple</td>
                    <td class="td-value">8-12x ARR</td>
                    <td class="td-value">10-15x ARR</td>
                    <td class="td-highlight">20-40x ARR</td>
                  </tr>
                </tbody>
              </table>
            </div>
          </div>
        </div>
      </section>

      <!-- How It Works (Digital Twin) -->
      <section class="features-section">
        <div class="container-wrapper">
          <div class="features-grid">
            <div class="feature-content fade-up-element">
              <div class="tag-pill">
                <iconify-icon icon="lucide:cpu" class="tag-icon"></iconify-icon>
                Reinforcement Learning
              </div>
              <h2 class="section-title">The Neural Mesh</h2>
              <p class="feature-desc">
                Our proprietary hardware stack integrates seamlessly with legacy PLCs. The Agent builds a Digital Twin of your facility, running thousands of "what-if" scenarios per minute to minimize kWh without compromising crop health.
              </p>
              
              <div class="info-cards">
                <div class="info-card">
                  <div class="card-icon-box">
                    <iconify-icon icon="lucide:activity" width="24"></iconify-icon>
                  </div>
                  <div>
                    <h4 class="card-title">Data Ingestion</h4>
                    <p class="card-text">Ingests humidity, PPFD, CO2, and leaf temp via mesh sensors.</p>
                  </div>
                </div>
                <div class="info-card">
                  <div class="card-icon-box">
                    <iconify-icon icon="lucide:brain-circuit" width="24"></iconify-icon>
                  </div>
                  <div>
                    <h4 class="card-title">Inference Engine</h4>
                    <p class="card-text">Deep RL (PPO) optimizes setpoints for HVAC, lighting, and irrigation.</p>
                  </div>
                </div>
              </div>
            </div>

            <!-- Graphic Visualization -->
            <div class="viz-container fade-up-element group">
              <!-- Background Grid -->
              <div class="viz-grid"></div>
              
              <!-- Animated Elements representing the Twin -->
              <div class="viz-center">
                <div class="viz-ring">
                  <div class="viz-ring-segment"></div>
                </div>
                <div class="viz-core"></div>
                <div class="viz-stats">
                  <div class="stat-value">98.4%</div>
                  <div class="stat-label">Optimization</div>
                </div>
                
                <!-- Floating Stats Cards -->
                <div class="float-card card-top">
                  <div class="float-label">HVAC Load</div>
                  <div class="float-value down">-32% ▼</div>
                </div>
                <div class="float-card card-bottom">
                  <div class="float-label">Yield Pred.</div>
                  <div class="float-value up">+12.4% ▲</div>
                </div>
              </div>
            </div>
          </div>
        </div>
      </section>

      <!-- GTM Roadmap -->
      <section id="roadmap" class="roadmap-section">
        <div class="container-wrapper">
          <div class="roadmap-header fade-up-element">
            <h2 class="section-title">Path to $100M Valuation</h2>
            <p class="section-subtitle">Execution roadmap for the next 18 months.</p>
          </div>

          <div class="roadmap-grid">
            <!-- Connecting Line (Desktop) -->
            <div class="roadmap-line"></div>

            <!-- Phase 1 -->
            <div class="phase-card fade-up-element">
              <div class="phase-dot current"></div>
              <div class="phase-content">
                <div class="phase-date">MONTH 0-3</div>
                <h3 class="phase-title">Prototype & MVP</h3>
                <p class="phase-desc">RL agent + digital twin on 1 greenhouse. Basic sensor integration.</p>
                <div class="phase-badge">Pre-seed $1-2M</div>
              </div>
            </div>

            <!-- Phase 2 -->
            <div class="phase-card fade-up-element delay-100">
              <div class="phase-dot current"></div>
              <div class="phase-content">
                <div class="phase-date">MONTH 4-8</div>
                <h3 class="phase-title">Pilot Testing</h3>
                <p class="phase-desc">10 pilots, 28% avg energy savings. $50k MRR target.</p>
                <div class="phase-badge">Seed $8-15M</div>
              </div>
            </div>

            <!-- Phase 3 -->
            <div class="phase-card fade-up-element delay-200">
               <div class="phase-dot future group-hover:bg-emerald-500"></div>
              <div class="phase-content">
                <div class="phase-date">MONTH 9-14</div>
                <h3 class="phase-title">Expansion</h3>
                <p class="phase-desc">100 greenhouses across EU/US. Full API suite. $500k MRR.</p>
                <div class="phase-badge">Series A $30-50M</div>
              </div>
            </div>

            <!-- Phase 4 -->
            <div class="phase-card fade-up-element delay-300">
               <div class="phase-dot future group-hover:bg-emerald-500"></div>
              <div class="phase-content">
                <div class="phase-date">MONTH 15-18</div>
                <h3 class="phase-title">Platform Scale</h3>
                <p class="phase-desc">Carbon credit integration. Yield prediction upsell. $1.2M MRR.</p>
                <div class="phase-badge">Series B</div>
              </div>
            </div>
          </div>
        </div>
      </section>

      <!-- CTA -->
      <section class="cta-section">
        <div class="cta-gradient"></div>
        <div class="cta-content">
          <h2 class="cta-title">Ready to Optimize?</h2>
          <p class="cta-subtitle">Join 10 Pilots – $500K Builds the Future.</p>
          <div class="cta-buttons">
            <button class="btn-primary shadow-lg">
              Contact for Funding
            </button>
            <button class="btn-tertiary">
              Download Pitch Deck
            </button>
          </div>
          <p class="cta-quote">"We're the Source.ag of North America."</p>
        </div>
      </section>

    </main>
  </div>
</template>

<script setup>
import { ref, reactive, onMounted, onBeforeUnmount } from 'vue'

const particleCanvas = ref(null)
const mouse = reactive({ x: 0.5, y: 0.5 }) // Default center

// Get plugins
const { $gsap, $three } = useNuxtApp()

onMounted(() => {
  // Load Iconify
  if (!document.querySelector('script[src*="iconify"]')) {
    const script = document.createElement('script')
    script.src = 'https://code.iconify.design/iconify-icon/1.0.7/iconify-icon.min.js'
    document.head.appendChild(script)
  }

  // Cursor tracking for immersion
  const updateMouse = (e) => {
    mouse.x = e.clientX / window.innerWidth
    mouse.y = e.clientY / window.innerHeight
  }
  window.addEventListener('mousemove', updateMouse)
  
  // Init Three.js particles
  if ($three && particleCanvas.value) {
    try {
      $three.createParticleField(particleCanvas.value, mouse)
    } catch (error) {
      console.error('Three.js init error:', error)
    }
  }
  
  // GSAP animations for elements
  if ($gsap) {
    // Reveal main container
    const appContent = document.querySelector('.app-container')
    if (appContent) {
      $gsap.to(appContent, {
        opacity: 1,
        scale: 1,
        duration: 1,
        ease: 'power3.out',
        delay: 0.1
      })
    }

    // Fade up elements
    $gsap.utils.toArray('.fade-up-element').forEach((el, index) => {
      $gsap.from(el, {
        scrollTrigger: {
          trigger: el,
          start: 'top 85%',
        },
        y: 50,
        opacity: 0,
        duration: 1,
        ease: 'power3.out',
        delay: index % 3 * 0.1 // Stagger effect
      })
    })
  }
  
  onBeforeUnmount(() => {
    window.removeEventListener('mousemove', updateMouse)
  })
})
</script>

<style scoped>
/* App Container */
.app-container {
  min-height: 100vh;
  display: flex;
  flex-direction: column;
  transition: all 1000ms cubic-bezier(0.22, 1, 0.36, 1);
  opacity: 0; 
  transform: scale(0.95);
}

.main-content {
  flex: 1;
}

/* Reusable Containers */
.container-wrapper {
  max-width: 1280px;
  margin: 0 auto;
  padding: 0 1.5rem;
}

/* Hero Section */
.hero-section {
  position: relative;
  height: 100vh;
  display: flex;
  align-items: center;
  justify-content: center;
  overflow: hidden;
}

.particle-canvas {
  position: absolute;
  inset: 0;
  width: 100%;
  height: 100%;
  opacity: 0.6;
  z-index: 0;
}

.hero-gradient {
  position: absolute;
  inset: 0;
  background: linear-gradient(to top, #000, transparent, transparent ,transparent);
  z-index: 0;
}

.hero-content {
  position: relative;
  z-index: 10;
  text-align: center;
  max-width: 64rem;
  margin: 0 auto;
  padding: 0 1.5rem;
}

.version-pill {
  display: inline-flex;
  align-items: center;
  gap: 0.5rem;
  padding: 0.25rem 0.75rem;
  border-radius: 9999px;
  border: 1px solid rgba(16, 185, 129, 0.2);
  background-color: rgba(16, 185, 129, 0.05);
  color: #34d399;
  font-size: 0.75rem;
  font-family: 'JetBrains Mono', monospace;
  margin-bottom: 2rem;
  backdrop-filter: blur(4px);
}

.version-ping {
  position: relative;
  display: flex;
  height: 0.5rem;
  width: 0.5rem;
}

.ping-wave {
  position: absolute;
  display: inline-flex;
  height: 100%;
  width: 100%;
  border-radius: 9999px;
  background-color: #34d399;
  opacity: 0.75;
  animation: ping 1s cubic-bezier(0, 0, 0.2, 1) infinite;
}

.ping-dot {
  position: relative;
  display: inline-flex;
  border-radius: 9999px;
  height: 0.5rem;
  width: 0.5rem;
  background-color: #10b981;
}

.hero-title {
  font-size: 3.75rem;
  line-height: 1;
  font-weight: 600;
  letter-spacing: -0.05em;
  color: #fff;
  margin-bottom: 1.5rem;
}

@media (min-width: 768px) {
  .hero-title {
    font-size: 6rem;
    line-height: 0.95;
  }
}

.text-highlight {
  color: transparent;
  background-clip: text;
  background-image: linear-gradient(to bottom, #34d399, #047857);
}

.hero-desc {
  font-size: 1.25rem;
  color: #a1a1aa;
  margin-bottom: 2.5rem;
  max-width: 42rem;
  margin-left: auto;
  margin-right: auto;
  line-height: 1.625;
}

.hero-buttons {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  gap: 1rem;
}

@media (min-width: 640px) {
  .hero-buttons {
    flex-direction: row;
  }
}

/* Buttons */
.btn-primary {
  width: 100%;
  padding: 1rem 2rem;
  background-color: #10b981;
  color: #000;
  font-weight: 600;
  border-radius: 9999px;
  transition: all 300ms ease;
  cursor: pointer;
}

@media (min-width: 640px) {
  .btn-primary {
    width: auto;
  }
}

.btn-primary:hover {
  background-color: #34d399;
  box-shadow: 0 0 40px rgba(16, 185, 129, 0.4);
}

.btn-secondary {
  width: 100%;
  padding: 1rem 2rem;
  background-color: rgba(255, 255, 255, 0.05);
  color: #fff;
  font-weight: 500;
  border: 1px solid rgba(255, 255, 255, 0.1);
  border-radius: 9999px;
  backdrop-filter: blur(12px);
  transition: all 300ms ease;
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 0.5rem;
  cursor: pointer;
}

@media (min-width: 640px) {
  .btn-secondary {
    width: auto;
  }
}

.btn-secondary:hover {
  background-color: rgba(255, 255, 255, 0.1);
}

.arrow-icon {
  transition: transform 300ms ease;
}

.group:hover .arrow-icon {
  transform: translateX(0.25rem);
}

.btn-tertiary {
  width: 100%;
  padding: 1rem 2rem;
  background-color: #18181b;
  color: #fff;
  font-weight: 500;
  border: 1px solid #27272a;
  border-radius: 9999px;
  transition: all 300ms ease;
  cursor: pointer;
}

@media (min-width: 640px) {
  .btn-tertiary {
    width: auto;
  }
}

.btn-tertiary:hover {
  background-color: #27272a;
}

/* Mission Section */
.mission-section {
  padding-top: 8rem;
  padding-bottom: 8rem;
  background-color: #09090b;
  border-top: 1px solid rgba(255, 255, 255, 0.05);
  position: relative;
}

.mission-glow {
  position: absolute;
  top: 0;
  left: 50%;
  transform: translateX(-50%);
  width: 800px;
  height: 300px;
  background-color: rgba(16, 185, 129, 0.05);
  filter: blur(100px);
  pointer-events: none;
}

.mission-header {
  text-align: center;
  margin-bottom: 5rem;
}

.section-title {
  font-size: 1.875rem;
  font-weight: 600;
  letter-spacing: -0.025em;
  color: #fff;
  margin-bottom: 1.5rem;
}

@media (min-width: 768px) {
  .section-title {
    font-size: 2.25rem;
  }
}

.section-desc {
  font-size: 1.125rem;
  color: #a1a1aa;
  max-width: 48rem;
  margin-left: auto;
  margin-right: auto;
}

.hidden-mobile {
  display: none;
}

@media (min-width: 768px) {
  .hidden-mobile {
    display: block;
  }
}

.comparison-container {
  background-color: rgba(255, 255, 255, 0.02);
  backdrop-filter: blur(16px);
  border: 1px solid rgba(255, 255, 255, 0.05);
  border-radius: 1rem;
  overflow: hidden;
  box-shadow: 0 25px 50px -12px rgba(0, 0, 0, 0.25);
}

.table-wrapper {
  overflow-x: auto;
}

.data-table {
  width: 100%;
  text-align: left;
  border-collapse: collapse;
  min-width: 800px;
}

.table-header-row {
  border-bottom: 1px solid rgba(255, 255, 255, 0.05);
  background-color: rgba(255, 255, 255, 0.05);
}

.th-criteria {
  padding: 1.5rem;
  font-size: 0.75rem;
  font-family: monospace;
  text-transform: uppercase;
  letter-spacing: 0.1em;
  color: #71717a;
}

.th-basic {
  padding: 1.5rem;
  font-size: 0.875rem;
  font-weight: 600;
  color: #d4d4d8;
}

.th-primary {
  padding: 1.5rem;
  font-size: 0.875rem;
  font-weight: 600;
  color: #34d399;
  background-color: rgba(16, 185, 129, 0.05);
  border-top: 2px solid #10b981;
}

.table-row {
  border-bottom: 1px solid rgba(255, 255, 255, 0.05);
  transition: background-color 300ms;
}

.table-row:hover {
  background-color: rgba(255, 255, 255, 0.05);
}

.td-label {
  padding: 1.5rem;
  font-weight: 500;
  color: #fff;
}

.td-value {
  padding: 1.5rem;
  color: #a1a1aa;
}

.td-highlight {
  padding: 1.5rem;
  color: #34d399;
  font-family: monospace;
  font-weight: 500;
  background-color: rgba(16, 185, 129, 0.05);
}

/* Features Section */
.features-section {
  padding-top: 8rem;
  padding-bottom: 8rem;
  position: relative;
  overflow: hidden;
}

.features-grid {
  display: grid;
  gap: 4rem;
  align-items: center;
}

@media (min-width: 1024px) {
  .features-grid {
    grid-template-columns: repeat(2, 1fr);
  }
}

.tag-pill {
  display: inline-flex;
  align-items: center;
  gap: 0.5rem;
  padding: 0.25rem 0.75rem;
  border-radius: 9999px;
  border: 1px solid #27272a;
  background-color: rgba(24, 24, 27, 0.5);
  color: #a1a1aa;
  font-size: 0.75rem;
  font-family: monospace;
  margin-bottom: 1.5rem;
}

.tag-icon {
  color: #10b981;
}

.feature-desc {
  font-size: 1.125rem;
  color: #a1a1aa;
  margin-bottom: 2rem;
  line-height: 1.625;
}

.info-cards {
  display: flex;
  flex-direction: column;
  gap: 1.5rem;
}

.info-card {
  display: flex;
  gap: 1rem;
}

.card-icon-box {
  width: 3rem;
  height: 3rem;
  border-radius: 0.5rem;
  background-color: #18181b;
  border: 1px solid #27272a;
  display: flex;
  align-items: center;
  justify-content: center;
  flex-shrink: 0;
  color: #10b981;
}

.card-title {
  color: #fff;
  font-weight: 500;
  margin-bottom: 0.25rem;
}

.card-text {
  font-size: 0.875rem;
  color: #71717a;
}

/* Visualization */
.viz-container {
  position: relative;
  aspect-ratio: 1 / 1;
  border-radius: 1rem;
  background-color: #18181b;
  border: 1px solid rgba(255, 255, 255, 0.1);
  overflow: hidden;
}

@media (min-width: 1024px) {
  .viz-container {
    aspect-ratio: 4 / 3;
  }
}

.viz-grid {
  position: absolute;
  inset: 0;
  background-image: 
    linear-gradient(rgba(255, 255, 255, 0.03) 1px, transparent 1px),
    linear-gradient(90deg, rgba(255, 255, 255, 0.03) 1px, transparent 1px);
  background-size: 40px 40px;
  opacity: 0.5;
}

.viz-center {
  position: absolute;
  inset: 0;
  display: flex;
  align-items: center;
  justify-content: center;
}

.viz-ring {
  position: relative;
  width: 12rem;
  height: 12rem;
  border: 1px solid rgba(16, 185, 129, 0.3);
  border-radius: 9999px;
  display: flex;
  align-items: center;
  justify-content: center;
  animation: spin 10s linear infinite;
}

.viz-ring-segment {
  position: absolute;
  inset: 0;
  border-top: 1px solid #10b981;
  border-radius: 9999px;
}

.viz-core {
  position: absolute;
  width: 8rem;
  height: 8rem;
  background-color: rgba(16, 185, 129, 0.1);
  border-radius: 9999px;
  filter: blur(24px);
  animation: pulse 2s cubic-bezier(0.4, 0, 0.6, 1) infinite;
}

.viz-stats {
  position: absolute;
  z-index: 10;
  text-align: center;
}

.stat-value {
  font-size: 1.875rem;
  font-weight: 700;
  color: #fff;
  letter-spacing: -0.05em;
}

.stat-label {
  font-size: 0.625rem;
  color: #34d399;
  font-family: monospace;
  letter-spacing: 0.1em;
  text-transform: uppercase;
  margin-top: 0.25rem;
}

.float-card {
  position: absolute;
  padding: 0.75rem;
  background-color: rgba(0, 0, 0, 0.8);
  backdrop-filter: blur(12px);
  border: 1px solid rgba(255, 255, 255, 0.1);
  border-radius: 0.5rem;
  font-size: 0.75rem;
  font-family: monospace;
  box-shadow: 0 20px 25px -5px rgba(0, 0, 0, 0.1), 0 10px 10px -5px rgba(0, 0, 0, 0.04);
  animation: pulse-glow 4s infinite;
}

.card-top {
  top: 2.5rem;
  right: 2.5rem;
}

.card-bottom {
  bottom: 2.5rem;
  left: 2.5rem;
  animation-delay: 1s;
}

.float-label {
  color: #71717a;
  margin-bottom: 0.25rem;
}

.float-value.down { color: #34d399; }
.float-value.up { color: #34d399; }

/* Roadmap */
.roadmap-section {
  padding-top: 8rem;
  padding-bottom: 8rem;
  background-color: #09090b;
  border-top: 1px solid rgba(255, 255, 255, 0.05);
}

.roadmap-header {
  text-align: center;
  margin-bottom: 5rem;
}

.section-subtitle {
  color: #a1a1aa;
}

.roadmap-grid {
  display: grid;
  gap: 1.5rem;
  position: relative;
}

@media (min-width: 768px) {
  .roadmap-grid {
    grid-template-columns: repeat(4, 1fr);
  }
}

.roadmap-line {
  display: none;
  position: absolute;
  top: 3rem;
  left: 0;
  right: 0;
  height: 1px;
  background: linear-gradient(90deg, transparent, rgba(16, 185, 129, 0.5), transparent);
}

@media (min-width: 768px) {
  .roadmap-line {
    display: block;
  }
}

.phase-card {
  position: relative;
  padding-top: 2rem;
}

.phase-dot {
  position: absolute;
  top: 2.625rem; /* 42px */
  left: 50%;
  transform: translateX(-50%);
  width: 0.75rem;
  height: 0.75rem;
  background-color: #000;
  border-radius: 9999px;
  z-index: 10;
  transition: all 300ms;
}

.phase-dot.current {
  border: 2px solid #10b981;
}

.phase-dot.future {
  border: 2px solid #3f3f46;
}

.phase-content {
  padding: 1.5rem;
  border-radius: 1rem;
  background-color: rgba(24, 24, 27, 0.4);
  border: 1px solid rgba(255, 255, 255, 0.05);
  transition: all 300ms;
  height: 100%;
}

.phase-content:hover {
  border-color: rgba(16, 185, 129, 0.3);
}

.phase-date {
  font-size: 0.75rem;
  font-family: monospace;
  color: #10b981;
  margin-bottom: 0.5rem;
}

.phase-title {
  font-size: 1.125rem;
  font-weight: 600;
  color: #fff;
  margin-bottom: 0.5rem;
}

.phase-desc {
  font-size: 0.875rem;
  color: #71717a;
  margin-bottom: 1rem;
}

.phase-badge {
  display: inline-block;
  padding: 0.25rem 0.5rem;
  background-color: rgba(255, 255, 255, 0.05);
  border-radius: 0.25rem;
  font-size: 0.625rem;
  color: #d4d4d8;
  border: 1px solid rgba(255, 255, 255, 0.1);
}

/* CTA Section */
.cta-section {
  padding-top: 8rem;
  padding-bottom: 8rem;
  position: relative;
  overflow: hidden;
}

.cta-gradient {
  position: absolute;
  inset: 0;
  background: linear-gradient(to bottom, transparent, rgba(6, 78, 59, 0.1), transparent);
}

.cta-content {
  position: relative;
  z-index: 10;
  text-align: center;
  max-width: 1280px;
  margin: 0 auto;
  padding: 0 1.5rem;
}

.cta-title {
  font-size: 2.25rem;
  font-weight: 600;
  letter-spacing: -0.05em;
  color: #fff;
  margin-bottom: 1.5rem;
}

@media (min-width: 768px) {
  .cta-title {
    font-size: 3rem;
  }
}

.cta-subtitle {
  font-size: 1.25rem;
  color: #a1a1aa;
  margin-bottom: 2.5rem;
}

.cta-buttons {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  gap: 1rem;
}

@media (min-width: 640px) {
  .cta-buttons {
    flex-direction: row;
  }
}

.cta-quote {
  margin-top: 2rem;
  font-size: 0.875rem;
  color: #52525b;
}

/* Animations */
@keyframes spin {
  to { transform: rotate(360deg); }
}

@keyframes ping {
  75%, 100% {
    transform: scale(2);
    opacity: 0;
  }
}

@keyframes pulse {
  50% { opacity: 0.5; }
}

@keyframes pulse-glow {
  0%, 100% { box-shadow: 0 0 0 rgba(16, 185, 129, 0); }
  50% { box-shadow: 0 0 20px rgba(16, 185, 129, 0.1); }
}
</style>