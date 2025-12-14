<template>
  <div class="agent-logs-panel">
    <div class="panel-header">
      <div class="panel-title-group">
        <iconify-icon icon="lucide:terminal-square" class="panel-icon-alt"></iconify-icon>
        <span class="panel-title">Agent Logs</span>
      </div>
      <span class="version-tag">v2.0.4-stable</span>
    </div>
    
    <div class="logs-content">
      <div class="log-entry">
        <span class="log-time">14:02:41</span>
        <div class="log-details">
          <div class="log-title log-success">Optimization Cycle Start</div>
          <div class="log-message">Analyzing 1,024 sensor points. Predictive model indicates yield potential +0.4%.</div>
        </div>
      </div>

      <div class="log-entry">
        <span class="log-time">14:02:55</span>
        <div class="log-details">
          <div class="log-title log-info">Action: HVAC Adjustment</div>
          <div class="log-message">Reducing cooling load by 12% to match external cloud cover data.</div>
        </div>
      </div>

      <div class="log-entry">
        <span class="log-time">14:03:12</span>
        <div class="log-details">
          <div class="log-title log-warning">Alert: Micro-climate Detected</div>
          <div class="log-message">Zone A, Row 3 exhibiting higher humidity (68%).</div>
        </div>
      </div>
      
      <div class="log-entry">
        <span class="log-time">14:03:15</span>
        <div class="log-details">
          <div class="log-title log-success">Action: Spot Ventilation</div>
          <div class="log-message">Activating fans 3 & 4 at 40% capacity.</div>
          <div class="log-command">
            > Executing command...
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<style scoped>
.agent-logs-panel {
  border-radius: 1rem;
  border: 1px solid rgba(255, 255, 255, 0.05);
  background-color: rgba(9, 9, 11, 0.5);
  display: flex;
  flex-direction: column;
  overflow: hidden;
  height: 100%;
}

.panel-header {
  padding: 1rem 1.5rem;
  border-bottom: 1px solid rgba(255, 255, 255, 0.05);
  display: flex;
  justify-content: space-between;
  align-items: center;
  background-color: rgba(24, 24, 27, 0.5);
  flex-wrap: wrap;
  gap: 0.5rem;
}

.panel-title-group {
  display: flex;
  align-items: center;
  gap: 0.5rem;
}

.panel-icon-alt {
  color: #a1a1aa;
}

.panel-title {
  font-size: 0.875rem;
  font-weight: 500;
  color: #e4e4e7;
}

@media (max-width: 640px) {
  .panel-title {
    font-size: 0.75rem;
  }
}

.version-tag {
  font-size: 0.625rem;
  color: #71717a;
  font-family: 'JetBrains Mono', monospace;
}

.logs-content {
  flex: 1;
  padding: 1rem;
  overflow-y: auto;
  font-family: 'JetBrains Mono', monospace;
  font-size: 0.75rem;
  display: flex;
  flex-direction: column;
  gap: 1rem;
}

@media (max-width: 640px) {
  .logs-content {
    font-size: 0.625rem;
    padding: 0.75rem;
    gap: 0.75rem;
  }
}

.log-entry {
  display: flex;
  gap: 0.75rem;
}

@media (max-width: 640px) {
  .log-entry {
    flex-direction: column;
    gap: 0.25rem;
  }
}

.log-time {
  color: #52525b;
  flex-shrink: 0;
}

.log-details {
  flex: 1;
}

.log-title {
  margin-bottom: 0.25rem;
}

.log-success { color: #34d399; }
.log-info { color: #e4e4e7; }
.log-warning { color: #fbbf24; }

.log-message {
  color: #71717a;
  margin-top: 0.25rem;
}

.log-command {
  margin-top: 0.5rem;
  padding: 0.5rem;
  background-color: rgba(16, 185, 129, 0.1);
  border: 1px solid rgba(16, 185, 129, 0.2);
  border-radius: 0.25rem;
  color: #6ee7b7;
}

/* Scrollbar Styling */
.logs-content::-webkit-scrollbar {
  width: 8px;
}

.logs-content::-webkit-scrollbar-track {
  background: transparent;
}

.logs-content::-webkit-scrollbar-thumb {
  background-color: rgba(255, 255, 255, 0.1);
  border-radius: 4px;
}

.logs-content::-webkit-scrollbar-thumb:hover {
  background-color: rgba(255, 255, 255, 0.2);
}
</style>
