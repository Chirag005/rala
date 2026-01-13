<template>
  <nav v-show="!isLoading" id="navbar" class="navbar" :class="{ 'scrolled': scrolled }">
    <div id="navbar-bg" class="navbar-bg" :class="{ 'active': scrolled }"></div>
    <div class="navbar-container">
      <a href="#" class="logo-link">
        <span class="logo-text">RAALA</span>
      </a>
      <ul class="nav-links">
        <li><a href="#mission" class="nav-link">The Agent</a></li>
        <li><a href="#comparison" class="nav-link">Market Data</a></li>
        <li><a href="#roadmap" class="nav-link">Roadmap</a></li>
      </ul>
      <div class="nav-actions">
        <NuxtLink to="/login" class="join-beta-btn">
          Join Beta
        </NuxtLink>
      </div>
    </div>
  </nav>
</template>

<script setup>
import { ref, onMounted, onUnmounted } from 'vue'

const { isLoading } = useAppState()
const scrolled = ref(false)

const handleScroll = () => {
  scrolled.value = window.scrollY > 50
}

onMounted(() => {
  window.addEventListener('scroll', handleScroll)
})

onUnmounted(() => {
  window.removeEventListener('scroll', handleScroll)
})
</script>

<style scoped>
/* Navbar */
.navbar {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  z-index: 50;
  transition: all 500ms ease;
  border-bottom: 1px solid transparent;
}

.navbar.scrolled {
  border-bottom-color: rgba(255, 255, 255, 0.1);
}

/* Navbar Background */
.navbar-bg {
  position: absolute;
  inset: 0;
  background-color: rgba(0, 0, 0, 0);
  backdrop-filter: blur(0px);
  transition: all 500ms ease;
}

.navbar-bg.active {
  background-color: rgba(0, 0, 0, 0.8);
  backdrop-filter: blur(12px);
}

/* Navbar Container */
.navbar-container {
  width: 100%;
  max-width: 1280px;
  margin: 0 auto;
  padding: 0 1.5rem;
  height: 5rem;
  display: flex;
  justify-content: space-between;
  align-items: center;
  position: relative;
  z-index: 10;
}

/* Logo */
.logo-link {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  text-decoration: none;
}

.logo-link:hover .logo-text {
  color: #10b981;
}

.logo-text {
  font-size: 1.125rem;
  font-weight: 600;
  letter-spacing: -0.025em;
  color: #fff;
  transition: color 300ms ease;
}

/* Navigation Links */
.nav-links {
  display: none;
  align-items: center;
  gap: 2rem;
  list-style: none;
  margin: 0;
  padding: 0;
}

@media (min-width: 768px) {
  .nav-links {
    display: flex;
  }
}

.nav-link {
  font-size: 0.875rem;
  font-weight: 500;
  color: #a1a1aa;
  text-decoration: none;
  transition: color 300ms ease;
}

.nav-link:hover {
  color: #fff;
}

/* Navigation Actions */
.nav-actions {
  display: flex;
  align-items: center;
  gap: 1rem;
}

/* Join Beta Button */
.join-beta-btn {
  display: inline-block;
  padding: 0.5rem 1.25rem;
  border-radius: 9999px;
  background-color: #fff;
  font-size: 0.875rem;
  font-weight: 600;
  color: #000;
  border: none;
  cursor: pointer;
  text-decoration: none;
  transition: all 300ms ease;
}

.join-beta-btn:hover {
  background-color: #10b981;
}
</style>