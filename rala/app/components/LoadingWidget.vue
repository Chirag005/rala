<template>
  <div v-if="loading" class="fixed inset-0 z-50 bg-black flex items-center justify-center">
    <canvas ref="canvas" class="w-full h-full"></canvas>
    <div class="absolute text-center text-white">
      <h1 class="text-4xl font-bold text-emerald-400">RALA</h1>
      <p class="text-sm opacity-75">Booting Autonomous Greenhouse OS...</p>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'

const loading = ref(true)
const canvas = ref(null)

onMounted(() => {
  const { $three } = useNuxtApp()
  
  if ($three && canvas.value) {
    try {
      const scene = $three.createGreenhouseScene(canvas.value)
      const animate = () => {
        requestAnimationFrame(animate)
        $three.animateParticles(scene)
      }
      animate()
    } catch (error) {
      console.error('Error initializing Three.js scene:', error)
    }
  }
  
  setTimeout(() => { loading.value = false }, 2500) // Fade after 2.5s
})
</script>