<template>
  <header class="dashboard-header">
    <div class="header-left">
      <h1 class="header-title">
        Facility 01 <span class="header-separator">/</span> Zone A
      </h1>
      <div class="status-badge">
        <span class="status-pulse"></span>
        AUTONOMOUS MODE
      </div>
    </div>

    <div class="header-right">
      <div class="next-harvest">
        <div class="harvest-label">Next Harvest</div>
        <div class="harvest-time">12 Days 04:32:01</div>
      </div>
      <button class="notification-btn">
        <iconify-icon icon="lucide:bell" width="20"></iconify-icon>
        <span class="notification-dot"></span>
      </button>
    </div>
  </header>
</template>

<style scoped>
.dashboard-header {
  height: 4rem;
  border-bottom: 1px solid rgba(255, 255, 255, 0.05);
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 0 2rem;
  background-color: rgba(0, 0, 0, 0.2);
  backdrop-filter: blur(4px);
}

@media (max-width: 768px) {
  .dashboard-header {
    padding: 0 1rem;
    flex-wrap: wrap;
    height: auto;
    min-height: 4rem;
  }
}

.header-left {
  display: flex;
  align-items: center;
  gap: 1rem;
  flex-wrap: wrap;
}

.header-title {
  font-size: 1.125rem;
  font-weight: 500;
  letter-spacing: -0.025em;
}

@media (max-width: 640px) {
  .header-title {
    font-size: 0.875rem;
  }
}

.header-separator {
  color: #52525b;
  margin: 0 0.5rem;
}

.status-badge {
  padding: 0.125rem 0.5rem;
  border-radius: 0.25rem;
  font-size: 0.625rem;
  font-family: 'JetBrains Mono', monospace;
  background-color: rgba(16, 185, 129, 0.1);
  color: #34d399;
  border: 1px solid rgba(16, 185, 129, 0.2);
  display: flex;
  align-items: center;
  gap: 0.5rem;
  white-space: nowrap;
}

.status-pulse {
  width: 0.375rem;
  height: 0.375rem;
  border-radius: 50%;
  background-color: #10b981;
  animation: pulse 2s cubic-bezier(0.4, 0, 0.6, 1) infinite;
}

.header-right {
  display: flex;
  align-items: center;
  gap: 1.5rem;
}

@media (max-width: 640px) {
  .header-right {
    gap: 0.75rem;
  }
}

.next-harvest {
  text-align: right;
}

.harvest-label {
  font-size: 0.75rem;
  color: #71717a;
}

.harvest-time {
  font-size: 0.875rem;
  font-family: 'JetBrains Mono', monospace;
  color: #fff;
}

@media (max-width: 640px) {
  .harvest-time {
    font-size: 0.75rem;
  }
}

.notification-btn {
  color: #a1a1aa;
  background: transparent;
  border: none;
  position: relative;
  cursor: pointer;
  transition: color 300ms;
}

.notification-btn:hover {
  color: #fff;
}

.notification-dot {
  position: absolute;
  top: 0;
  right: 0;
  width: 0.5rem;
  height: 0.5rem;
  background-color: #f43f5e;
  border-radius: 50%;
  border: 1px solid #000;
}

@media (max-width: 768px) {
  .next-harvest {
    display: none;
  }
}

@keyframes pulse {
  0%, 100% { opacity: 1; }
  50% { opacity: 0.5; }
}
</style>
