<template>
  <div class="dashboard-layout">
    <!-- Global Loading Widget -->
    <LoadingWidget />
    
    <!-- Dashboard Content (No Navbar/Footer) -->
    <slot />
  </div>
</template>

<script setup>
// Dashboard layout - full screen, no nav/footer
</script>

<style>
.dashboard-layout {
  min-height: 100vh;
  background-color: #000;
  color: #fff;
  font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;
}

/* Ensure smooth scrolling for dashboard */
html {
  scroll-behavior: smooth;
}

body {
  background-color: black;
  color: white;
}

/* Custom Scrollbar for Dashboard */
::-webkit-scrollbar {
  width: 8px;
}

::-webkit-scrollbar-track {
  background: #09090b;
}

::-webkit-scrollbar-thumb {
  background: #27272a;
  border-radius: 4px;
}

::-webkit-scrollbar-thumb:hover {
  background: #10B981;
}
</style>
