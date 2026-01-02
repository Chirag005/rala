<template>
  <div class="metrics-grid">
    <!-- VPD Card -->
    <div class="metric-card">
      <div class="metric-card-bg"></div>
      <div class="metric-header">
        <span class="metric-label">VPD (kPa)</span>
        <iconify-icon icon="lucide:droplets" class="metric-icon icon-emerald"></iconify-icon>
      </div>
      <div class="metric-value-row">
        <span class="metric-value">0.85</span>
        <span class="metric-change metric-up">
          <iconify-icon icon="lucide:arrow-up-right" width="12"></iconify-icon> 2%
        </span>
      </div>
      <div class="metric-chart">
        <svg viewBox="0 0 100 20" class="chart-svg chart-emerald" preserveAspectRatio="none">
          <path d="M0 15 Q 10 18, 20 10 T 40 12 T 60 5 T 80 14 T 100 8" vector-effect="non-scaling-stroke"/>
          <path d="M0 15 Q 10 18, 20 10 T 40 12 T 60 5 T 80 14 T 100 8 V 20 H 0 Z" class="chart-fill"/>
        </svg>
      </div>
    </div>

    <!-- PPFD Card -->
    <div class="metric-card">
      <div class="metric-header">
        <span class="metric-label">PPFD (μmol)</span>
        <iconify-icon icon="lucide:sun" class="metric-icon icon-amber"></iconify-icon>
      </div>
      <div class="metric-value-row">
        <span class="metric-value">920</span>
        <span class="metric-target">Target: 950</span>
      </div>
      <div class="progress-bar">
        <div class="progress-fill progress-amber"></div>
      </div>
    </div>

    <!-- Canopy Temp Card -->
    <div class="metric-card">
      <div class="metric-card-bg"></div>
      <div class="metric-header">
        <span class="metric-label">Canopy Temp</span>
        <iconify-icon icon="lucide:thermometer" class="metric-icon icon-rose"></iconify-icon>
      </div>
      <div class="metric-value-row">
        <span class="metric-value">23.4°</span>
        <span class="metric-change metric-alert">
          <iconify-icon icon="lucide:alert-circle" width="12"></iconify-icon> High
        </span>
      </div>
      <div class="metric-chart">
        <svg viewBox="0 0 100 20" class="chart-svg chart-rose" preserveAspectRatio="none">
          <path d="M0 10 L 20 10 L 40 5 L 60 15 L 80 5 L 100 2" vector-effect="non-scaling-stroke"/>
        </svg>
      </div>
    </div>

    <!-- Energy Savings Card -->
    <div class="metric-card">
      <div class="metric-header">
        <span class="metric-label">Energy Savings</span>
        <iconify-icon icon="lucide:zap" class="metric-icon icon-emerald"></iconify-icon>
      </div>
      <div class="energy-value">$4,230</div>
      <div class="energy-subtitle">Projected this month via RL</div>
    </div>
  </div>
</template>

<style scoped>
.metrics-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
  gap: 1rem;
}

@media (max-width: 640px) {
  .metrics-grid {
    grid-template-columns: 1fr;
  }
}

.metric-card {
  position: relative;
  padding: 1.25rem;
  border-radius: 1rem;
  background-color: rgba(24, 24, 27, 0.4);
  border: 1px solid rgba(255, 255, 255, 0.05);
  transition: border-color 300ms ease;
  overflow: hidden;
}

.metric-card:hover {
  border-color: rgba(16, 185, 129, 0.3);
}

.metric-card-bg {
  position: absolute;
  inset: 0;
  background: linear-gradient(to bottom right, rgba(16, 185, 129, 0.05), transparent);
  opacity: 0;
  transition: opacity 300ms;
}

.metric-card:hover .metric-card-bg {
  opacity: 1;
}

.metric-header {
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
  margin-bottom: 0.5rem;
  position: relative;
  z-index: 10;
}

.metric-label {
  font-size: 0.75rem;
  font-weight: 500;
  color: #a1a1aa;
}

.metric-icon {
  font-size: 1.25rem;
}

.icon-emerald { color: #10b981; }
.icon-amber { color: #f59e0b; }
.icon-rose { color: #fb7185; }

.metric-value-row {
  display: flex;
  align-items: flex-end;
  gap: 0.75rem;
  position: relative;
  z-index: 10;
}

.metric-value {
  font-size: 1.875rem;
  font-weight: 600;
  letter-spacing: -0.05em;
}

@media (max-width: 640px) {
  .metric-value {
    font-size: 1.5rem;
  }
}

.metric-change {
  font-size: 0.75rem;
  margin-bottom: 0.25rem;
  display: flex;
  align-items: center;
  gap: 0.125rem;
}

.metric-up { color: #34d399; }
.metric-alert { color: #fb7185; }

.metric-target {
  font-size: 0.75rem;
  color: #71717a;
  margin-bottom: 0.25rem;
}

.metric-chart {
  height: 2.5rem;
  margin-top: 0.5rem;
  margin-left: -0.5rem;
  margin-right: -0.5rem;
  opacity: 0.5;
}

.chart-svg {
  width: 100%;
  height: 100%;
  fill: none;
  stroke-width: 2;
}

.chart-emerald { stroke: #10b981; }
.chart-emerald .chart-fill {
  fill: rgba(16, 185, 129, 0.1);
  stroke: none;
}

.chart-rose { stroke: #f43f5e; }

.progress-bar {
  width: 100%;
  background-color: #27272a;
  height: 0.25rem;
  margin-top: 1rem;
  border-radius: 9999px;
  overflow: hidden;
}

.progress-fill {
  height: 100%;
  border-radius: 9999px;
}

.progress-amber {
  width: 92%;
  background-color: #f59e0b;
  box-shadow: 0 0 10px rgba(245, 158, 11, 0.5);
}

.energy-value {
  font-size: 1.875rem;
  font-weight: 600;
  letter-spacing: -0.05em;
  color: #34d399;
}

@media (max-width: 640px) {
  .energy-value {
    font-size: 1.5rem;
  }
}

.energy-subtitle {
  font-size: 0.625rem;
  color: #71717a;
  margin-top: 0.25rem;
}
</style>
