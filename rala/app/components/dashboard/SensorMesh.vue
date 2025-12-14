<template>
  <div class="sensor-mesh-panel">
    <div class="panel-header">
      <div class="panel-title-group">
        <iconify-icon icon="lucide:scan-line" class="panel-icon"></iconify-icon>
        <span class="panel-title">Sensor Mesh / Zone A</span>
      </div>
      <div class="panel-controls">
        <button class="control-btn">Heatmap</button>
        <button class="control-btn control-btn-active">Live View</button>
      </div>
    </div>

    <div class="sensor-content">
      <div class="scan-line"></div>
      
      <div class="sensor-grid">
        <!-- Row 1 -->
        <div class="sensor-node sensor-optimal"><div class="node-dot"></div></div>
        <div class="sensor-node sensor-optimal"><div class="node-dot"></div></div>
        <div class="sensor-node sensor-adjusting"><div class="node-dot node-pulse"></div></div>
        <div class="sensor-node sensor-optimal"><div class="node-dot"></div></div>
        <div class="sensor-node sensor-optimal"><div class="node-dot"></div></div>
        <div class="sensor-node sensor-optimal"><div class="node-dot"></div></div>
        
        <!-- Row 2 -->
        <div class="sensor-node sensor-optimal"><div class="node-dot"></div></div>
        <div class="sensor-node sensor-optimal"><div class="node-dot"></div></div>
        <div class="sensor-node sensor-optimal"><div class="node-dot"></div></div>
        <div class="sensor-node sensor-optimal"><div class="node-dot"></div></div>
        <div class="sensor-node sensor-optimal"><div class="node-dot"></div></div>
        <div class="sensor-node sensor-optimal"><div class="node-dot"></div></div>
        
        <!-- Row 3 -->
        <div class="sensor-node sensor-optimal"><div class="node-dot"></div></div>
        <div class="sensor-node sensor-stress"><div class="node-dot node-bounce"></div></div>
        <div class="sensor-node sensor-optimal"><div class="node-dot"></div></div>
        <div class="sensor-node sensor-optimal"><div class="node-dot"></div></div>
        <div class="sensor-node sensor-optimal"><div class="node-dot"></div></div>
        <div class="sensor-node sensor-optimal"><div class="node-dot"></div></div>

        <!-- Row 4 -->
        <div class="sensor-node sensor-optimal"><div class="node-dot"></div></div>
        <div class="sensor-node sensor-optimal"><div class="node-dot"></div></div>
        <div class="sensor-node sensor-optimal"><div class="node-dot"></div></div>
        <div class="sensor-node sensor-optimal"><div class="node-dot"></div></div>
        <div class="sensor-node sensor-optimal"><div class="node-dot"></div></div>
        <div class="sensor-node sensor-optimal"><div class="node-dot"></div></div>
      </div>

      <div class="sensor-legend">
        <div class="legend-item">
          <div class="legend-dot legend-optimal"></div> Optimal
        </div>
        <div class="legend-item">
          <div class="legend-dot legend-adjusting"></div> Adjusting
        </div>
        <div class="legend-item">
          <div class="legend-dot legend-stress"></div> Stress
        </div>
      </div>
    </div>
  </div>
</template>

<style scoped>
.sensor-mesh-panel {
  border-radius: 1rem;
  border: 1px solid rgba(255, 255, 255, 0.05);
  background-color: rgba(24, 24, 27, 0.3);
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

.panel-icon {
  color: #10b981;
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

.panel-controls {
  display: flex;
  gap: 0.5rem;
}

.control-btn {
  font-size: 0.625rem;
  padding: 0.25rem 0.5rem;
  background-color: rgba(255, 255, 255, 0.1);
  border: none;
  border-radius: 0.25rem;
  color: #fff;
  cursor: pointer;
  transition: background-color 300ms;
}

.control-btn:hover {
  background-color: rgba(255, 255, 255, 0.2);
}

.control-btn-active {
  background-color: rgba(16, 185, 129, 0.2);
  color: #34d399;
  border: 1px solid rgba(16, 185, 129, 0.3);
}

.sensor-content {
  flex: 1;
  position: relative;
  padding: 1.5rem;
  display: flex;
  align-items: center;
  justify-content: center;
}

@media (max-width: 640px) {
  .sensor-content {
    padding: 1rem;
  }
}

.scan-line {
  position: absolute;
  top: 0;
  bottom: 0;
  left: 0;
  width: 1px;
  background-color: rgba(16, 185, 129, 0.5);
  box-shadow: 0 0 20px #10b981;
  z-index: 10;
  animation: scan 4s linear infinite;
}

.sensor-grid {
  display: grid;
  grid-template-columns: repeat(6, 1fr);
  grid-template-rows: repeat(4, 1fr);
  gap: 1rem;
  width: 100%;
  height: 100%;
  max-width: 42rem;
}

@media (max-width: 768px) {
  .sensor-grid {
    gap: 0.5rem;
    grid-template-columns: repeat(4, 1fr);
    grid-template-rows: repeat(6, 1fr);
  }
}

.sensor-node {
  border-radius: 0.5rem;
  display: flex;
  align-items: center;
  justify-content: center;
  transition: all 300ms;
  cursor: pointer;
}

.sensor-optimal {
  background-color: rgba(16, 185, 129, 0.1);
  border: 1px solid rgba(16, 185, 129, 0.3);
}

.sensor-optimal:hover {
  background-color: rgba(16, 185, 129, 0.3);
}

.sensor-adjusting {
  background-color: rgba(245, 158, 11, 0.1);
  border: 1px solid rgba(245, 158, 11, 0.3);
}

.sensor-adjusting:hover {
  background-color: rgba(245, 158, 11, 0.3);
}

.sensor-stress {
  background-color: rgba(244, 63, 94, 0.1);
  border: 1px solid rgba(244, 63, 94, 0.3);
}

.sensor-stress:hover {
  background-color: rgba(244, 63, 94, 0.3);
}

.node-dot {
  width: 0.375rem;
  height: 0.375rem;
  border-radius: 50%;
  background-color: #10b981;
  box-shadow: 0 0 5px #10b981;
}

.sensor-adjusting .node-dot {
  background-color: #f59e0b;
}

.node-pulse {
  animation: pulse 2s cubic-bezier(0.4, 0, 0.6, 1) infinite;
}

.sensor-stress .node-dot {
  background-color: #f43f5e;
}

.node-bounce {
  animation: bounce 1s infinite;
}

.sensor-legend {
  position: absolute;
  bottom: 1rem;
  left: 1.5rem;
  padding: 0.75rem;
  border-radius: 0.5rem;
  background-color: rgba(0, 0, 0, 0.6);
  backdrop-filter: blur(8px);
  border: 1px solid rgba(255, 255, 255, 0.05);
  font-size: 0.625rem;
  display: flex;
  flex-direction: column;
  gap: 0.5rem;
}

@media (max-width: 640px) {
  .sensor-legend {
    bottom: 0.5rem;
    left: 0.5rem;
    padding: 0.5rem;
    font-size: 0.5rem;
  }
}

.legend-item {
  display: flex;
  align-items: center;
  gap: 0.5rem;
}

.legend-dot {
  width: 0.5rem;
  height: 0.5rem;
  border-radius: 50%;
}

.legend-optimal { background-color: #10b981; }
.legend-adjusting { background-color: #f59e0b; }
.legend-stress { background-color: #f43f5e; }

@keyframes scan {
  0% { left: 0; opacity: 0; }
  10% { opacity: 1; }
  90% { opacity: 1; }
  100% { left: 100%; opacity: 0; }
}

@keyframes pulse {
  0%, 100% { opacity: 1; }
  50% { opacity: 0.5; }
}

@keyframes bounce {
  0%, 100% {
    transform: translateY(0);
    animation-timing-function: cubic-bezier(0, 0, 0.2, 1);
  }
  50% {
    transform: translateY(-25%);
    animation-timing-function: cubic-bezier(0.8, 0, 1, 1);
  }
}
</style>
