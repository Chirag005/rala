<template>
  <div v-if="isVisible" class="loader-wrapper" :class="{ 'fade-out': fadeOut }">
    
    <!-- Particle Background -->
    <div class="particles">
      <div v-for="i in 30" :key="i" class="particle" :style="getParticleStyle(i)"></div>
    </div>
    
    <!-- Radial Gradient Glow -->
    <div class="radial-glow"></div>
    
    <!-- Main Loader Content -->
    <div class="loader-content">
      
      <!-- Rotating Rings -->
      <div class="rings-container">
        <div class="ring ring-1"></div>
        <div class="ring ring-2"></div>
        <div class="ring ring-3"></div>
      </div>
      
      <!-- Logo Container with Animation -->
      <div class="logo-container" :class="{ 'logo-loaded': logoLoaded }">
        <div class="logo-glow-effect"></div>
        <img 
          src="/raala-logo.png" 
          alt="RAALA" 
          class="logo-image"
          @load="onLogoLoad"
        />
        <!-- Logo nodes pulse effect -->
        <div class="node-pulse node-1"></div>
        <div class="node-pulse node-2"></div>
        <div class="node-pulse node-3"></div>
        <div class="node-pulse node-4"></div>
        <div class="node-pulse node-5"></div>
        <div class="node-pulse node-6"></div>
      </div>
      
      <!-- Brand Name with Stagger Animation -->
      <div class="brand-section">
        <h1 class="brand-name">
          <span class="letter" v-for="(letter, i) in 'RAALA'" :key="i" :style="{ animationDelay: `${0.8 + i * 0.1}s` }">
            {{ letter }}
          </span>
        </h1>
        <p class="tagline">Autonomous Greenhouse OS</p>
      </div>
      
      <!-- Progress Section -->
      <div class="progress-wrapper">
        <!-- Circular Progress -->
        <svg class="progress-ring" width="120" height="120">
          <circle
            class="progress-ring-bg"
            stroke="#18181b"
            stroke-width="2"
            fill="transparent"
            r="54"
            cx="60"
            cy="60"
          />
          <circle
            class="progress-ring-circle"
            stroke="url(#gradient)"
            stroke-width="2"
            fill="transparent"
            r="54"
            cx="60"
            cy="60"
            :stroke-dasharray="circumference"
            :stroke-dashoffset="progressOffset"
          />
          <defs>
            <linearGradient id="gradient" x1="0%" y1="0%" x2="100%" y2="100%">
              <stop offset="0%" style="stop-color:#10b981;stop-opacity:1" />
              <stop offset="100%" style="stop-color:#34d399;stop-opacity:1" />
            </linearGradient>
          </defs>
        </svg>
        
        <!-- Percentage Counter -->
        <div class="progress-percentage">{{ Math.round(progress) }}%</div>
      </div>
      
      <!-- Status Text -->
      <div class="status-section">
        <div class="status-text">{{ statusText }}</div>
        <div class="status-dots">
          <span class="dot"></span>
          <span class="dot"></span>
          <span class="dot"></span>
        </div>
      </div>
      
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'

const isVisible = ref(true)
const fadeOut = ref(false)
const progress = ref(0)
const logoLoaded = ref(false)
const statusText = ref('Initializing system')

const statusMessages = [
  'Initializing system',
  'Calibrating sensors',
  'Syncing neural mesh',
  'Loading AI models',
  'Optimizing parameters',
  'Ready to launch'
]

// Circle progress calculations
const radius = 54
const circumference = 2 * Math.PI * radius
const progressOffset = computed(() => {
  const offset = circumference - (progress.value / 100) * circumference
  return offset
})

// Particle positioning
const getParticleStyle = (index) => {
  const angle = (index / 30) * 360
  const distance = 30 + Math.random() * 40
  const x = Math.cos(angle * Math.PI / 180) * distance
  const y = Math.sin(angle * Math.PI / 180) * distance
  const delay = Math.random() * 2
  const duration = 3 + Math.random() * 2
  
  return {
    left: `calc(50% + ${x}vw)`,
    top: `calc(50% + ${y}vh)`,
    animationDelay: `${delay}s`,
    animationDuration: `${duration}s`
  }
}

const onLogoLoad = () => {
  logoLoaded.value = true
}

onMounted(() => {
  let currentMessageIndex = 0
  const totalDuration = 4000 // 4 seconds
  const intervalTime = 50
  const increment = 100 / (totalDuration / intervalTime)
  
  // Progress animation
  const progressTimer = setInterval(() => {
    progress.value += increment
    
    // Add organic easing
    if (progress.value > 95) {
      progress.value = Math.min(progress.value, 100)
    }
    
    // Update status messages
    const progressThresholds = [0, 20, 40, 60, 80, 95]
    progressThresholds.forEach((threshold, index) => {
      if (progress.value >= threshold && currentMessageIndex === index) {
        statusText.value = statusMessages[index]
        currentMessageIndex++
      }
    })
    
    // Complete
    if (progress.value >= 100) {
      clearInterval(progressTimer)
      
      // Fade out after completion
      setTimeout(() => {
        fadeOut.value = true
        setTimeout(() => {
          isVisible.value = false
        }, 800)
      }, 600)
    }
  }, intervalTime)
})
</script>

<style scoped>
/* Main Container */
.loader-wrapper {
  position: fixed;
  inset: 0;
  z-index: 9999;
  display: flex;
  align-items: center;
  justify-content: center;
  background: #000;
  overflow: hidden;
  transition: opacity 800ms cubic-bezier(0.4, 0, 0.2, 1);
}

.loader-wrapper.fade-out {
  opacity: 0;
}

/* Particles */
.particles {
  position: absolute;
  inset: 0;
  pointer-events: none;
}

.particle {
  position: absolute;
  width: 2px;
  height: 2px;
  background: #10b981;
  border-radius: 50%;
  opacity: 0;
  animation: particleFloat 4s ease-in-out infinite;
  box-shadow: 0 0 10px #10b981;
}

@keyframes particleFloat {
  0%, 100% {
    opacity: 0;
    transform: translateY(0) scale(1);
  }
  50% {
    opacity: 0.6;
    transform: translateY(-20px) scale(1.5);
  }
}

/* Radial Glow */
.radial-glow {
  position: absolute;
  width: 800px;
  height: 800px;
  background: radial-gradient(circle, rgba(16, 185, 129, 0.15) 0%, transparent 70%);
  animation: pulseGlow 4s ease-in-out infinite;
  pointer-events: none;
}

@keyframes pulseGlow {
  0%, 100% {
    transform: scale(1);
    opacity: 0.3;
  }
  50% {
    transform: scale(1.2);
    opacity: 0.5;
  }
}

/* Main Content */
.loader-content {
  position: relative;
  z-index: 10;
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 2.5rem;
}

/* Rotating Rings */
.rings-container {
  position: absolute;
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);
  width: 400px;
  height: 400px;
  pointer-events: none;
}

.ring {
  position: absolute;
  border: 1px solid rgba(16, 185, 129, 0.1);
  border-radius: 50%;
  animation: rotateRing 20s linear infinite;
}

.ring-1 {
  width: 300px;
  height: 300px;
  top: 50px;
  left: 50px;
  border-top-color: rgba(16, 185, 129, 0.3);
  animation-duration: 15s;
}

.ring-2 {
  width: 350px;
  height: 350px;
  top: 25px;
  left: 25px;
  border-right-color: rgba(16, 185, 129, 0.2);
  animation-duration: 20s;
  animation-direction: reverse;
}

.ring-3 {
  width: 400px;
  height: 400px;
  top: 0;
  left: 0;
  border-bottom-color: rgba(16, 185, 129, 0.15);
  animation-duration: 25s;
}

@keyframes rotateRing {
  from {
    transform: rotate(0deg);
  }
  to {
    transform: rotate(360deg);
  }
}

/* Logo Container */
.logo-container {
  position: relative;
  width: 180px;
  height: 180px;
  display: flex;
  align-items: center;
  justify-content: center;
  opacity: 0;
  transform: scale(0.5);
  animation: logoAppear 1s cubic-bezier(0.34, 1.56, 0.64, 1) forwards;
  animation-delay: 0.3s;
}

.logo-container.logo-loaded {
  /* Additional class for when image loads */
}

@keyframes logoAppear {
  to {
    opacity: 1;
    transform: scale(1);
  }
}

.logo-glow-effect {
  position: absolute;
  inset: -20px;
  background: radial-gradient(circle, rgba(16, 185, 129, 0.3), transparent 70%);
  border-radius: 50%;
  animation: logoGlowPulse 2s ease-in-out infinite;
  animation-delay: 1s;
}

@keyframes logoGlowPulse {
  0%, 100% {
    transform: scale(1);
    opacity: 0.5;
  }
  50% {
    transform: scale(1.3);
    opacity: 0.8;
  }
}

.logo-image {
  width: 100%;
  height: 100%;
  object-fit: contain;
  filter: drop-shadow(0 0 20px rgba(16, 185, 129, 0.6));
  animation: logoFloat 3s ease-in-out infinite;
  animation-delay: 1.2s;
}

@keyframes logoFloat {
  0%, 100% {
    transform: translateY(0);
  }
  50% {
    transform: translateY(-10px);
  }
}

/* Node Pulses - simulating the nodes in the logo */
.node-pulse {
  position: absolute;
  width: 12px;
  height: 12px;
  background: #10b981;
  border-radius: 50%;
  opacity: 0;
  animation: nodePulse 2s ease-in-out infinite;
  box-shadow: 0 0 15px #10b981;
}

.node-1 { top: 20%; left: 50%; animation-delay: 1.3s; }
.node-2 { top: 40%; left: 35%; animation-delay: 1.4s; }
.node-3 { top: 40%; right: 35%; animation-delay: 1.5s; }
.node-4 { bottom: 30%; left: 30%; animation-delay: 1.6s; }
.node-5 { bottom: 30%; right: 30%; animation-delay: 1.7s; }
.node-6 { bottom: 20%; left: 50%; animation-delay: 1.8s; }

@keyframes nodePulse {
  0%, 100% {
    opacity: 0;
    transform: translate(-50%, -50%) scale(0.5);
  }
  50% {
    opacity: 1;
    transform: translate(-50%, -50%) scale(1);
  }
}

/* Brand Section */
.brand-section {
  text-align: center;
}

.brand-name {
  font-size: 3rem;
  font-weight: 600;
  letter-spacing: 0.1em;
  color: #fff;
  margin-bottom: 0.5rem;
  display: flex;
  gap: 0.2rem;
}

.letter {
  display: inline-block;
  opacity: 0;
  animation: letterAppear 0.6s cubic-bezier(0.34, 1.56, 0.64, 1) forwards;
}

@keyframes letterAppear {
  from {
    opacity: 0;
    transform: translateY(20px) rotate(10deg);
  }
  to {
    opacity: 1;
    transform: translateY(0) rotate(0deg);
  }
}

.tagline {
  font-size: 0.875rem;
  color: #10b981;
  text-transform: uppercase;
  letter-spacing: 0.15em;
  font-weight: 500;
  opacity: 0;
  animation: fadeInUp 0.8s ease forwards;
  animation-delay: 1.5s;
}

@keyframes fadeInUp {
  from {
    opacity: 0;
    transform: translateY(10px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

/* Progress Ring */
.progress-wrapper {
  position: relative;
  opacity: 0;
  animation: fadeInUp 0.8s ease forwards;
  animation-delay: 1.8s;
}

.progress-ring {
  transform: rotate(-90deg);
  filter: drop-shadow(0 0 10px rgba(16, 185, 129, 0.5));
}

.progress-ring-circle {
  transition: stroke-dashoffset 0.3s cubic-bezier(0.4, 0, 0.2, 1);
  stroke-linecap: round;
}

.progress-percentage {
  position: absolute;
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);
  font-size: 1.5rem;
  font-weight: 600;
  color: #10b981;
  font-family: 'JetBrains Mono', monospace;
}

/* Status Section */
.status-section {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 0.75rem;
  opacity: 0;
  animation: fadeInUp 0.8s ease forwards;
  animation-delay: 2s;
}

.status-text {
  font-size: 0.875rem;
  color: #a1a1aa;
  text-transform: uppercase;
  letter-spacing: 0.1em;
  font-weight: 500;
  font-family: 'JetBrains Mono', monospace;
}

.status-dots {
  display: flex;
  gap: 0.5rem;
}

.dot {
  width: 6px;
  height: 6px;
  background: #10b981;
  border-radius: 50%;
  animation: dotPulse 1.4s ease-in-out infinite;
}

.dot:nth-child(2) {
  animation-delay: 0.2s;
}

.dot:nth-child(3) {
  animation-delay: 0.4s;
}

@keyframes dotPulse {
  0%, 100% {
    opacity: 0.3;
    transform: scale(1);
  }
  50% {
    opacity: 1;
    transform: scale(1.3);
  }
}

/* Responsive */
@media (max-width: 768px) {
  .logo-container {
    width: 120px;
    height: 120px;
  }
  
  .brand-name {
    font-size: 2rem;
  }
  
  .rings-container {
    width: 300px;
    height: 300px;
  }
  
  .ring-1 {
    width: 200px;
    height: 200px;
    top: 50px;
    left: 50px;
  }
  
  .ring-2 {
    width: 250px;
    height: 250px;
    top: 25px;
    left: 25px;
  }
  
  .ring-3 {
    width: 300px;
    height: 300px;
  }
}
</style>
