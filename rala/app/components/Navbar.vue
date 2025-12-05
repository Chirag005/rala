<template>
  <nav class="fixed top-0 left-0 right-0 z-40 bg-black/80 backdrop-blur-md transition-all duration-300" :class="{ 'py-2': scrolled, 'py-4': !scrolled }">
    <div class="container mx-auto px-4 flex justify-between items-center">
      <NuxtLink to="/" class="text-2xl font-bold text-emerald-400">RALA</NuxtLink>
      <ul class="hidden md:flex space-x-6">
        <li><NuxtLink to="#mission" class="text-white hover:text-emerald-400 transition">Mission</NuxtLink></li>
        <li><NuxtLink to="#how" class="text-white hover:text-emerald-400 transition">How It Works</NuxtLink></li>
        <li><NuxtLink to="#gtm" class="text-white hover:text-emerald-400 transition">For Investors</NuxtLink></li>
      </ul>
      <button class="bg-emerald-500 text-white px-6 py-2 rounded-full hover:bg-emerald-600 transition">Apply for Pilot</button>
      <button class="md:hidden">☰</button> <!-- Hamburger -->
    </div>
  </nav>
</template>

<script setup>
import { ref, onMounted } from 'vue'

const scrolled = ref(false)
onMounted(() => {
  window.addEventListener('scroll', () => { scrolled.value = window.scrollY > 50 })
})
</script>