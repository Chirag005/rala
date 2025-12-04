<template>
  <div class="min-h-screen bg-black text-white overflow-x-hidden">
    <LoadingWidget />
    <Navbar />
    
    <!-- Hero: Hook with Problem + Teaser -->
    <section class="h-screen flex items-center justify-center relative">
      <canvas class="absolute inset-0 opacity-20" ref="bgCanvas"></canvas> <!-- Three.js energy waves -->
      <div class="container mx-auto text-center z-10 px-4">
        <h1 class="text-6xl md:text-8xl font-bold mb-4 animate-fadeIn">Autonomous Greenhouse OS</h1>
        <p class="text-xl md:text-2xl mb-8 max-w-2xl mx-auto">AI Agents + RL + Digital Twins: Cut Energy 30%, Boost Yields 12%. Immediate Savings on Your #1 Cost.</p>
        <button class="bg-emerald-500 text-white px-8 py-4 rounded-full text-lg hover:bg-emerald-600 gsap-trigger">See the Demo</button>
      </div>
    </section>

    <!-- Mission Section -->
    <section id="mission" class="py-20 bg-gray-900">
      <div class="container mx-auto px-4">
        <div class="text-center mb-16 gsap-trigger">
          <h2 class="text-4xl font-bold mb-4">Why Energy Optimization First?</h2>
          <p class="text-lg max-w-3xl mx-auto">In a $110B market, we're the YC-backed agent automating physical processes. 28% avg savings, &lt;30-day pilots.</p>
        </div>
        <!-- Table from your data: Head-to-Head -->
        <div class="overflow-x-auto">
          <table class="w-full text-left border-collapse">
            <thead><tr class="bg-emerald-800"><th>Criteria</th><th>Yield Prediction</th><th>Pest Detection</th><th>Energy Optimization</th></tr></thead>
            <tbody>
              <tr><td>Market Size</td><td>$25B</td><td>$12B</td><td class="text-emerald-400 font-bold">$110B</td></tr>
              <tr><td>ROI Speed</td><td>6-12 mo</td><td>3-9 mo</td><td class="text-emerald-400 font-bold">3-6 mo</td></tr>
              <!-- Add all rows from your breakdown -->
            </tbody>
          </table>
        </div>
      </div>
    </section>

    <!-- How It Works -->
    <section id="how" class="py-20">
      <div class="container mx-auto px-4">
        <h2 class="text-4xl font-bold text-center mb-16 gsap-trigger">RL Agent in Action</h2>
        <div class="grid md:grid-cols-3 gap-8">
          <div class="gsap-trigger text-center"> <!-- Slide-in cards -->
            <h3>Digital Twin</h3>
            <p>Simulate your greenhouse in real-time.</p>
            <!-- Embed Three.js mini-scene -->
          </div>
          <!-- Cards for RL Control, Measurable ROI, Patent Moat -->
        </div>
      </div>
    </section>

    <!-- GTM Playbook -->
    <section id="gtm" class="py-20 bg-gray-900">
      <div class="container mx-auto px-4">
        <h2 class="text-4xl font-bold text-center mb-16">Path to $100M Valuation</h2>
        <div class="grid md:grid-cols-4 gap-8"> <!-- Timeline cards: Month 0-3, etc. -->
          <div class="gsap-trigger">MVP: 1 Greenhouse<br>Pre-seed $1-2M</div>
          <!-- ... -->
        </div>
        <div class="text-center mt-8">
          <p>"We're the Source.ag of North America."</p>
          <button class="bg-emerald-500...">Download Pitch Deck</button>
        </div>
      </div>
    </section>

    <!-- CTA -->
    <section class="py-20 text-center">
      <h2 class="text-4xl font-bold mb-4">Ready to Optimize?</h2>
      <p class="mb-8">Join 10 Pilots – $500K Builds the Future</p>
      <button class="bg-emerald-500 text-white px-8 py-4 rounded-full text-lg">Contact for Funding</button>
    </section>
  </div>
</template>

<script setup>
// GSAP Scroll Triggers
const { $gsap } = useNuxtApp()
onMounted(() => {
  gsap.registerPlugin(ScrollTrigger)
  gsap.utils.toArray('.gsap-trigger').forEach(el => {
    gsap.from(el, { y: 50, opacity: 0, duration: 1, scrollTrigger: { trigger: el, start: 'top 80%' } })
  })
  // Cursor-follow for WebGL bg
  const mouse = { x: 0, y: 0 }
  window.addEventListener('mousemove', (e) => { mouse.x = e.clientX / window.innerWidth; mouse.y = e.clientY / window.innerHeight })
  // Animate hero canvas with mouse
})

// Three.js for Hero BG: Energy grid
onMounted(() => {
  const scene = useNuxtApp().$three.createEnergyGrid(bgCanvas.value, mouse) // Responsive shader
})
</script>

<style>
/* Custom animations */
@keyframes fadeIn { from { opacity: 0; transform: translateY(20px); } to { opacity: 1; transform: translateY(0); } }
.animate-fadeIn { animation: fadeIn 1s ease-out; }
</style>