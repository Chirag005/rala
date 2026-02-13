<template>
  <div class="min-h-screen bg-black text-white selection:bg-emerald-500 selection:text-white font-sans flex flex-col">
    <!-- Global Loading Widget -->
    <LoadingWidget />
    
    <!-- Navigation -->
    <!-- <Navbar /> -->
    
    <!-- Main Content -->
    <main class="flex-grow">
      <slot />
    </main>

    <!-- Footer -->
    <!-- <Footer /> -->
  </div>
</template>

<script setup>
// Layout specific logic can go here
</script>

<style>
/* Global Styles for the App */
html {
  scroll-behavior: smooth;
}

body {
  background-color: black;
  color: white;
}

/* Custom Scrollbar */
::-webkit-scrollbar {
  width: 8px;
}

::-webkit-scrollbar-track {
  background: #09090b; /* Zinc 950 */
}

::-webkit-scrollbar-thumb {
  background: #27272a; /* Zinc 800 */
  border-radius: 4px;
}

::-webkit-scrollbar-thumb:hover {
  background: #10B981; /* Emerald 500 */
}
</style>
