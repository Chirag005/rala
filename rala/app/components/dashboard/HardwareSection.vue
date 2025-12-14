<template>
  <div class="hardware-section">
    <h3 class="hardware-title">Hardware Interactions</h3>
    <div class="hardware-grid">
      <!-- Ventilation -->
      <div class="hardware-card">
        <div class="hardware-icon">
          <iconify-icon icon="lucide:wind" width="18"></iconify-icon>
        </div>
        <div class="hardware-info">
          <div class="hardware-label">Ventilation</div>
          <div class="hardware-value">40% Capacity</div>
        </div>
        <div class="toggle-switch toggle-on">
          <div class="toggle-knob"></div>
        </div>
      </div>

      <!-- Irrigation -->
      <div class="hardware-card">
        <div class="hardware-icon">
          <iconify-icon icon="lucide:droplet" width="18"></iconify-icon>
        </div>
        <div class="hardware-info">
          <div class="hardware-label">Irrigation</div>
          <div class="hardware-value">Scheduled: 16:00</div>
        </div>
        <div class="hardware-status">IDLE</div>
      </div>

      <!-- Lighting -->
      <div class="hardware-card">
        <div class="hardware-icon">
          <iconify-icon icon="lucide:lightbulb" width="18"></iconify-icon>
        </div>
        <div class="hardware-info">
          <div class="hardware-label">Lighting</div>
          <div class="hardware-value">DLI Control Active</div>
        </div>
        <div class="toggle-switch toggle-on">
          <div class="toggle-knob"></div>
        </div>
      </div>
    </div>
  </div>
</template>

<style scoped>
.hardware-section {
  border-radius: 1rem;
  border: 1px solid rgba(255, 255, 255, 0.05);
  background-color: rgba(24, 24, 27, 0.3);
  padding: 1.5rem;
}

@media (max-width: 640px) {
  .hardware-section {
    padding: 1rem;
  }
}

.hardware-title {
  font-size: 0.875rem;
  font-weight: 500;
  color: #d4d4d8;
  margin-bottom: 1rem;
}

.hardware-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(280px, 1fr));
  gap: 1rem;
}

@media (max-width: 640px) {
  .hardware-grid {
    grid-template-columns: 1fr;
  }
}

.hardware-card {
  padding: 1rem;
  border-radius: 0.75rem;
  background-color: rgba(0, 0, 0, 0.4);
  border: 1px solid rgba(255, 255, 255, 0.05);
  display: flex;
  align-items: center;
  gap: 1rem;
}

.hardware-icon {
  width: 2.5rem;
  height: 2.5rem;
  border-radius: 50%;
  background-color: #27272a;
  display: flex;
  align-items: center;
  justify-content: center;
  color: #a1a1aa;
  flex-shrink: 0;
}

.hardware-info {
  flex: 1;
}

.hardware-label {
  font-size: 0.625rem;
  text-transform: uppercase;
  letter-spacing: 0.1em;
  color: #71717a;
}

.hardware-value {
  font-size: 0.875rem;
  color: #fff;
}

@media (max-width: 640px) {
  .hardware-value {
    font-size: 0.75rem;
  }
}

.toggle-switch {
  width: 2rem;
  height: 1rem;
  border-radius: 9999px;
  position: relative;
  transition: background-color 300ms;
  flex-shrink: 0;
}

.toggle-on {
  background-color: rgba(16, 185, 129, 0.2);
  border: 1px solid rgba(16, 185, 129, 0.5);
}

.toggle-knob {
  position: absolute;
  top: 0.125rem;
  bottom: 0.125rem;
  width: 0.75rem;
  background-color: #10b981;
  border-radius: 50%;
  transition: transform 300ms;
}

.toggle-on .toggle-knob {
  right: 0.125rem;
}

.hardware-status {
  font-size: 0.75rem;
  color: #52525b;
  font-family: 'JetBrains Mono', monospace;
}
</style>
