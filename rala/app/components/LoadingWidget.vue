<template>
  <div v-if="isLoading" class="loader-container">
    
    <!-- Background Ambient Effects -->
    <div class="bg-gradient"></div>
    <div class="bg-pattern"></div>

    <!-- Loader Widget Container -->
    <div class="loader-content">
      
      <!-- Logo Section -->
      <div class="logo-section">
        <div class="logo-glow"></div>
        <h1 class="logo-text">
          RAALA
          <span class="logo-indicator"></span>
        </h1>
      </div>

      <!-- Progress Section -->
      <div class="progress-section">
        <!-- Status Labels -->
        <div class="status-labels">
          <span class="status-text" :class="{ 'pulsing': progress < 100, 'completed': progress >= 100 }">{{ loadingText }}</span>
          <span class="percentage">{{ progress }}%</span>
        </div>

        <!-- Progress Bar Rail -->
        <div class="progress-rail">
          <!-- Active Bar -->
          <div class="progress-bar" :style="{ width: `${progress}%` }">
            <!-- Shimmer Effect -->
            <div class="shimmer-effect"></div>
          </div>
        </div>

        <!-- Meta Data -->
        <div class="meta-data">
          <span>version 0.0.1</span>
          <span class="connection-status">SECURE CONNECTION</span>
          <span>EST: 0.2s</span>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'

const { isLoading, setLoading } = useAppState()
const progress = ref(0)
const loadingText = ref('Initializing core...')

const loadingStates = [
  "Booting Kernel...",
  "Calibrating Sensors...",
  "Syncing Mesh Network...",
  "Loading Modules...",
  "Optimizing...",
  "Ready."
]

onMounted(() => {
  let stateIndex = 0
  const duration = 3000 // 3 seconds
  const intervalTime = 30
  const increment = 100 / (duration / intervalTime)

  const timer = setInterval(() => {
    progress.value += increment
    
    // Add subtle randomness to movement
    const noise = (Math.random() - 0.5) * 1.5
    const currentProgress = Math.min(Math.round(progress.value + noise), 100)
    progress.value = currentProgress

    // State Text Logic
    if (currentProgress > 15 && stateIndex === 0) {
      loadingText.value = loadingStates[1]
      stateIndex++
    }
    if (currentProgress > 35 && stateIndex === 1) {
      loadingText.value = loadingStates[2]
      stateIndex++
    }
    if (currentProgress > 60 && stateIndex === 2) {
      loadingText.value = loadingStates[3]
      stateIndex++
    }
    if (currentProgress > 80 && stateIndex === 3) {
      loadingText.value = loadingStates[4]
      stateIndex++
    }
    if (currentProgress >= 100 && stateIndex === 4) {
      loadingText.value = loadingStates[5]
      stateIndex++
      clearInterval(timer)
      
      // Hide loader after completion
      setTimeout(() => {
        setLoading(false)
      }, 500)
    }
  }, intervalTime)
})
</script>

<style scoped>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600&family=JetBrains+Mono:wght@400;500&display=swap');

/* Container */
.loader-container {
  position: fixed;
  inset: 0;
  z-index: 50;
  display: flex;
  align-items: center;
  justify-content: center;
  min-height: 100vh;
  background-color: #000;
  color: #d4d4d8;
  overflow: hidden;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
}

/* Background Effects */
.bg-gradient {
  position: absolute;
  inset: 0;
  background: radial-gradient(circle at center, rgba(6, 78, 59, 0.3), #000, #000);
}

.bg-pattern {
  position: absolute;
  inset: 0;
  opacity: 0.2;
  background-image: url('data:image/svg+xml;base64,PHN2ZyB4bWxucz0iaHR0cDovL3d3dy53My5vcmcvMjAwMC9zdmciIHdpZHRoPSI0MCIgaGVpZ2h0PSI0MCIgdmlld0JveD0iMCAwIDQwIDQwIj48ZyBmaWxsLXJ1bGU9ImV2ZW5vZGQiPjxwYXRoIGQ9Ik0wIDQwaDQwVjBIOHYzMmgzMnY4eiIgZmlsbD0iIzIyMiIgb3BhY2l0eT0iMC4wNSIvPjwvZz48L3N2Zz4=');
}

/* Loader Content */
.loader-content {
  position: relative;
  z-index: 10;
  width: 100%;
  max-width: 28rem;
  padding: 0 2rem;
  display: flex;
  flex-direction: column;
  align-items: center;
}

/* Logo Section */
.logo-section {
  position: relative;
  margin-bottom: 3.5rem;
  user-select: none;
}

.logo-glow {
  position: absolute;
  inset: -2rem;
  background-color: rgba(16, 185, 129, 0.1);
  border-radius: 9999px;
  filter: blur(2rem);
  opacity: 0.5;
}

.logo-text {
  position: relative;
  z-index: 10;
  font-size: 4.5rem;
  font-weight: 600;
  letter-spacing: -0.05em;
  color: #fff;
  font-family: 'Inter', sans-serif;
}

.logo-indicator {
  position: absolute;
  top: -0.25rem;
  right: -0.75rem;
  width: 0.5rem;
  height: 0.5rem;
  background-color: #10b981;
  border-radius: 9999px;
  animation: pulse 2s cubic-bezier(0.4, 0, 0.6, 1) infinite;
  box-shadow: 0 0 12px #10b981;
}

/* Progress Section */
.progress-section {
  width: 100%;
  display: flex;
  flex-direction: column;
  gap: 1.25rem;
}

/* Status Labels */
.status-labels {
  display: flex;
  justify-content: space-between;
  align-items: flex-end;
  font-size: 0.75rem;
  font-family: 'JetBrains Mono', monospace;
  text-transform: uppercase;
  letter-spacing: 0.1em;
  color: rgba(16, 185, 129, 0.9);
}

.status-text.pulsing {
  animation: pulse 2s cubic-bezier(0.4, 0, 0.6, 1) infinite;
}

.status-text.completed {
  color: #fff;
}

.percentage {
  color: rgba(16, 185, 129, 0.9);
}

/* Progress Bar */
.progress-rail {
  position: relative;
  width: 100%;
  height: 2px;
  background-color: #18181b;
  border-radius: 9999px;
  overflow: hidden;
}

.progress-bar {
  position: relative;
  height: 100%;
  background-color: #10b981;
  box-shadow: 0 0 20px rgba(16, 185, 129, 0.6);
  transition: all 75ms ease-out;
}

.shimmer-effect {
  position: absolute;
  inset: 0;
  width: 100%;
  background-color: rgba(255, 255, 255, 0.4);
  filter: blur(1px);
  animation: shimmer 2s infinite;
}

/* Meta Data */
.meta-data {
  display: flex;
  justify-content: space-between;
  font-size: 0.625rem;
  color: #52525b;
  font-family: 'JetBrains Mono', monospace;
  padding-top: 0.25rem;
}

.connection-status {
  color: rgba(6, 78, 59, 0.4);
}

/* Animations */
@keyframes shimmer {
  0% { transform: translateX(-100%); }
  100% { transform: translateX(100%); }
}

@keyframes pulse {
  0%, 100% {
    opacity: 1;
  }
  50% {
    opacity: 0.5;
  }
}
</style>