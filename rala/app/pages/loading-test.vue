<template>
  <div class="test-container">
    <LoadingWidgetNew />
    <div class="controls">
      <button @click="restartAnimation" class="restart-btn">
        Restart Animation
      </button>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import LoadingWidgetNew from '../components/LoadingWidgetNew.vue'

const key = ref(0)

const restartAnimation = () => {
  key.value++
  location.reload()
}
</script>

<style scoped>
.test-container {
  position: relative;
  min-height: 100vh;
  background-color: #000;
}

.controls {
  position: fixed;
  bottom: 2rem;
  right: 2rem;
  z-index: 100;
}

.restart-btn {
  padding: 0.75rem 1.5rem;
  background-color: #10b981;
  color: #000;
  font-weight: 600;
  border-radius: 0.5rem;
  border: none;
  cursor: pointer;
  transition: all 300ms ease;
  font-size: 0.875rem;
}

.restart-btn:hover {
  background-color: #34d399;
  transform: translateY(-2px);
  box-shadow: 0 10px 30px rgba(16, 185, 129, 0.3);
}
</style>
