<template>
  <div class="dashboard-wrapper">
    <!-- Background Effects -->
    <div class="bg-grid"></div>
    <div class="bg-glow"></div>

    <!-- Main Dashboard Layout -->
    <div class="dashboard-layout">
      <!-- Sidebar -->
      <ClientOnly>
        <DashboardSidebar />
      </ClientOnly>

      <!-- Main Content -->
      <main class="main-dashboard">
        <!-- Dashboard Header -->
        <ClientOnly>
          <DashboardHeader />
        </ClientOnly>

        <!-- Content Area -->
        <div class="content-area">
          <!-- Metrics Grid -->
          <ClientOnly>
            <MetricsGrid />
          </ClientOnly>

          <!-- Sensor Mesh & Agent Logs Grid -->
          <div class="lower-grid">
            <ClientOnly>
              <SensorMesh />
            </ClientOnly>
            <ClientOnly>
              <AgentLogs />
            </ClientOnly>
          </div>

          <!-- Hardware Interactions -->
          <ClientOnly>
            <HardwareSection />
          </ClientOnly>
        </div>
      </main>
    </div>
  </div>
</template>

<script setup>
import { onMounted } from 'vue'

// Explicitly import all dashboard components
const DashboardSidebar = defineAsyncComponent(() => 
  import('~/components/dashboard/DashboardSidebar.vue')
)
const DashboardHeader = defineAsyncComponent(() => 
  import('~/components/dashboard/DashboardHeader.vue')
)
const MetricsGrid = defineAsyncComponent(() => 
  import('~/components/dashboard/MetricsGrid.vue')
)
const SensorMesh = defineAsyncComponent(() => 
  import('~/components/dashboard/SensorMesh.vue')
)
const AgentLogs = defineAsyncComponent(() => 
  import('~/components/dashboard/AgentLogs.vue')
)
const HardwareSection = defineAsyncComponent(() => 
  import('~/components/dashboard/HardwareSection.vue')
)

onMounted(() => {
  console.log('Dashboard mounted!')
  
  // Load Iconify
  if (!document.querySelector('script[src*="iconify"]')) {
    const script = document.createElement('script')
    script.src = 'https://code.iconify.design/iconify-icon/1.0.7/iconify-icon.min.js'
    document.head.appendChild(script)
    console.log('Iconify script loaded')
  }
})
</script>

<style scoped>
/* Dashboard Wrapper */
.dashboard-wrapper {
  min-height: calc(100vh - 5rem); /* Account for navbar */
  background-color: #000;
  color: #fff;
  font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;
  display: flex;
  flex-direction: column;
  position: relative;
}

.bg-grid {
  position: fixed;
  inset: 0;
  background-image: 
    linear-gradient(rgba(255, 255, 255, 0.02) 1px, transparent 1px),
    linear-gradient(90deg, rgba(255, 255, 255, 0.02) 1px, transparent 1px);
  background-size: 50px 50px;
  pointer-events: none;
  z-index: 0;
}

.bg-glow {
  position: fixed;
  top: 0;
  right: 0;
  width: 500px;
  height: 500px;
  background-color: rgba(16, 185, 129, 0.1);
  filter: blur(120px);
  pointer-events: none;
  border-radius: 50%;
  z-index: 0;
}

/* Dashboard Layout */
.dashboard-layout {
  display: flex;
  flex: 1;
  position: relative;
  z-index: 10;
}

@media (max-width: 768px) {
  .dashboard-layout {
    flex-direction: column;
  }
}

/* Main Dashboard */
.main-dashboard {
  flex: 1;
  display: flex;
  flex-direction: column;
  overflow: hidden;
}

/* Content Area */
.content-area {
  flex: 1;
  overflow-y: auto;
  padding: 2rem;
  display: flex;
  flex-direction: column;
  gap: 1.5rem;
}

@media (max-width: 768px) {
  .content-area {
    padding: 1rem;
    gap: 1rem;
  }
}

/* Lower Grid */
.lower-grid {
  display: grid;
  grid-template-columns: 1fr;
  gap: 1.5rem;
  min-height: 500px;
}

@media (min-width: 1024px) {
  .lower-grid {
    grid-template-columns: 2fr 1fr;
  }
}

@media (max-width: 768px) {
  .lower-grid {
    min-height: auto;
    gap: 1rem;
  }
}

/* Scrollbar Styling */
.content-area::-webkit-scrollbar {
  width: 8px;
}

.content-area::-webkit-scrollbar-track {
  background: transparent;
}

.content-area::-webkit-scrollbar-thumb {
  background-color: rgba(255, 255, 255, 0.1);
  border-radius: 4px;
}

.content-area::-webkit-scrollbar-thumb:hover {
  background-color: rgba(255, 255, 255, 0.2);
}
</style>
