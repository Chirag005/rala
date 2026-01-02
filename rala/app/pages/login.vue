<script setup lang="ts">
const supabase = useSupabaseClient()
const user = useSupabaseUser()

// Redirect if already logged in
watchEffect(() => {
  if (user.value) { 
    navigateTo('/dashboard') 
  }
})

// Auth mode toggle
const isSignup = ref(false)

// Form data
const email = ref('')
const password = ref('')
const firstName = ref('')
const lastName = ref('')
const company = ref('')

// Auth handlers
const loginWithGoogle = async () => {
  const { error } = await supabase.auth.signInWithOAuth({
    provider: 'google',
    options: { 
      redirectTo: `${window.location.origin}/auth/callback` 
    }
  })
  if (error) console.error('Google login error:', error)
}

const loginWithGithub = async () => {
  const { error } = await supabase.auth.signInWithOAuth({
    provider: 'github',
    options: { 
      redirectTo: `${window.location.origin}/auth/callback` 
    }
  })
  if (error) console.error('GitHub login error:', error)
}

const handleSubmit = async () => {
  if (isSignup.value) {
    // Sign up
    const { error } = await supabase.auth.signUp({
      email: email.value,
      password: password.value,
      options: {
        data: {
          first_name: firstName.value,
          last_name: lastName.value,
          company: company.value
        }
      }
    })
    if (error) {
      console.error('Sign up error:', error)
      alert(error.message)
    } else {
      alert('Please check your email to confirm your account!')
    }
  } else {
    // Sign in
    const { error } = await supabase.auth.signInWithPassword({
      email: email.value,
      password: password.value
    })
    if (error) {
      console.error('Sign in error:', error)
      alert(error.message)
    }
  }
}

const toggleAuthMode = () => {
  isSignup.value = !isSignup.value
}

// SEO
useHead({
  title: 'RALA - Access Control',
  meta: [
    { name: 'description', content: 'Sign in to access your RALA autonomous greenhouse dashboard' }
  ]
})
</script>

<template>
  <div class="auth-container">
    <!-- Left Panel: Form -->
    <div class="auth-panel">
      <!-- Header -->
      <div class="auth-header">
        <NuxtLink to="/" class="auth-logo-link">
          <div class="auth-logo-box">
            <span class="auth-logo-letter">R</span>
          </div>
          <span class="auth-logo-text">RALA</span>
        </NuxtLink>
        <NuxtLink to="/" class="auth-back-link">BACK TO SITE</NuxtLink>
      </div>

      <!-- Auth Content -->
      <div class="auth-content">
        <div class="auth-title-section">
          <h1 class="auth-title">
            {{ isSignup ? 'Create an account' : 'Welcome back' }}
          </h1>
          <p class="auth-subtitle">
            {{ isSignup ? 'Start optimizing your facility today.' : 'Enter your credentials to access the agent dashboard.' }}
          </p>
        </div>

        <!-- Social Auth -->
        <div class="social-auth-grid">
          <button @click="loginWithGithub" class="social-auth-btn">
            <iconify-icon icon="lucide:github" width="16"></iconify-icon>
            GitHub
          </button>
          <button @click="loginWithGoogle" class="social-auth-btn">
            <iconify-icon icon="lucide:chrome" width="16"></iconify-icon>
            Google
          </button>
        </div>

        <div class="auth-divider">
          <div class="auth-divider-line"></div>
          <div class="auth-divider-content">
            <span class="auth-divider-text">Or continue with</span>
          </div>
        </div>

        <!-- Main Form -->
        <form @submit.prevent="handleSubmit" class="auth-form">
          <!-- Sign Up Fields -->
          <Transition name="fade">
            <div v-if="isSignup" class="signup-fields">
              <div class="name-grid">
                <div class="input-group">
                  <label class="input-label">First Name</label>
                  <input 
                    v-model="firstName" 
                    type="text" 
                    class="input-field" 
                    placeholder="John"
                    required
                  >
                </div>
                <div class="input-group">
                  <label class="input-label">Last Name</label>
                  <input 
                    v-model="lastName" 
                    type="text" 
                    class="input-field" 
                    placeholder="Doe"
                    required
                  >
                </div>
              </div>
              <div class="input-group">
                <label class="input-label">Company / Facility</label>
                <div class="input-wrapper">
                  <input 
                    v-model="company" 
                    type="text" 
                    class="input-field input-with-icon" 
                    placeholder="Greenhouse Corp"
                  >
                  <iconify-icon icon="lucide:building-2" class="input-icon" width="14"></iconify-icon>
                </div>
              </div>
            </div>
          </Transition>

          <!-- Common Fields -->
          <div class="input-group">
            <label class="input-label">Email</label>
            <div class="input-wrapper">
              <input 
                v-model="email" 
                type="email" 
                class="input-field input-with-icon" 
                placeholder="name@company.com"
                required
              >
              <iconify-icon icon="lucide:mail" class="input-icon" width="14"></iconify-icon>
            </div>
          </div>

          <div class="input-group">
            <div class="password-label-row">
              <label class="input-label">Password</label>
              <a v-if="!isSignup" href="#" class="forgot-password-link">Forgot password?</a>
            </div>
            <div class="input-wrapper">
              <input 
                v-model="password" 
                type="password" 
                class="input-field input-with-icon" 
                placeholder="••••••••"
                required
              >
              <iconify-icon icon="lucide:lock" class="input-icon" width="14"></iconify-icon>
            </div>
          </div>

          <button type="submit" class="submit-btn">
            <span>{{ isSignup ? 'Create Account' : 'Sign In' }}</span>
            <iconify-icon icon="lucide:arrow-right" class="submit-arrow" width="16"></iconify-icon>
          </button>
        </form>

        <div class="toggle-section">
          <p class="toggle-text">
            <span>{{ isSignup ? 'Already have an account?' : "Don't have an account?" }}</span>
            <button @click="toggleAuthMode" class="toggle-btn">
              {{ isSignup ? 'Sign in' : 'Sign up' }}
            </button>
          </p>
        </div>
      </div>

      <!-- Footer -->
      <div class="auth-footer">
        <p class="auth-footer-text">
          SECURED BY RALA NEURAL MESH v2.0
        </p>
      </div>
    </div>

    <!-- Right Panel: Visual Visualization -->
    <div class="visual-panel">
      <!-- Background Effects -->
      <div class="visual-grid"></div>
      <div class="visual-gradient"></div>
      
      <!-- Animated Blob -->
      <div class="visual-blob"></div>

      <!-- Digital Twin Card -->
      <div class="digital-twin-card">
        <!-- Card Header -->
        <div class="card-header">
          <div class="card-status">
            <div class="status-dot"></div>
            <span class="status-text">Live Agent</span>
          </div>
          <span class="card-id">ID: GH-2049-X</span>
        </div>

        <!-- Visualization Area -->
        <div class="visualization-area">
          <!-- Bars Simulation -->
          <div class="bar-wrapper">
            <div class="bar-fill bar-1"></div>
          </div>
          <div class="bar-wrapper bar-70">
            <div class="bar-fill bar-2"></div>
          </div>
          <div class="bar-wrapper bar-50">
            <div class="bar-fill bar-3"></div>
          </div>
          <div class="bar-wrapper bar-80">
            <div class="bar-fill bar-4"></div>
          </div>
          <div class="bar-wrapper bar-30">
            <div class="bar-fill bar-5"></div>
          </div>
          
          <!-- Overlay Grid Line -->
          <div class="grid-line"></div>
        </div>

        <!-- Stats Grid -->
        <div class="stats-grid">
          <div class="stat-card">
            <div class="stat-label">Energy Saving</div>
            <div class="stat-value">
              32% <span class="stat-indicator stat-up">▲</span>
            </div>
          </div>
          <div class="stat-card">
            <div class="stat-label">Grid Load</div>
            <div class="stat-value">
              12kW <span class="stat-indicator stat-down">▼</span>
            </div>
          </div>
        </div>

        <!-- Terminal Output -->
        <div class="terminal-output">
          <div class="terminal-line">
            <span class="terminal-prompt">➜</span>
            <span>Optimizing HVAC setpoints...</span>
          </div>
          <div class="terminal-line">
            <span class="terminal-prompt">➜</span>
            <span>PPO Model confidence: 98.4%</span>
          </div>
        </div>
      </div>

      <!-- Floating Quote -->
      <div class="floating-quote">
        <p class="quote-text">
          "RALA autonomously reduced our operational costs by 28% in the first quarter."
        </p>
        <div class="quote-attribution">
          <span>GreenLeaf Industries</span>
          <span class="quote-dot"></span>
          <span>Series B Partner</span>
        </div>
      </div>
    </div>
  </div>
</template>

<style scoped>
/* Import Fonts */
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600&family=JetBrains+Mono:wght@400;500&display=swap');

/* CSS Variables */
:root {
  --font-sans: 'Inter', sans-serif;
  --font-mono: 'JetBrains Mono', monospace;
}

/* Container */
.auth-container {
  font-family: var(--font-sans);
  background-color: #000;
  color: #fff;
  min-height: 100vh;
  display: flex;
  overflow: hidden;
}

::selection {
  background-color: rgba(16, 185, 129, 0.3);
  color: rgb(167, 243, 208);
}

/* Left Panel */
.auth-panel {
  width: 100%;
  display: flex;
  flex-direction: column;
  position: relative;
  z-index: 20;
  background-color: #000;
  height: 100vh;
  overflow-y: auto;
}

/* Header */
.auth-header {
  padding: 2rem;
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.auth-logo-link {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  text-decoration: none;
  transition: all 0.3s;
}

.auth-logo-box {
  width: 1.5rem;
  height: 1.5rem;
  background-color: rgba(16, 185, 129, 0.1);
  border: 1px solid rgba(16, 185, 129, 0.3);
  border-radius: 0.25rem;
  display: flex;
  align-items: center;
  justify-content: center;
  color: rgb(52, 211, 153);
  transition: all 0.3s;
}

.auth-logo-link:hover .auth-logo-box {
  background-color: rgb(16, 185, 129);
  color: #000;
}

.auth-logo-letter {
  font-weight: 700;
  font-size: 0.75rem;
  letter-spacing: -0.025em;
}

.auth-logo-text {
  font-size: 1.125rem;
  font-weight: 600;
  letter-spacing: -0.025em;
  color: white;
}

.auth-back-link {
  font-size: 0.75rem;
  font-family: var(--font-mono);
  color: rgb(113, 113, 122);
  text-decoration: none;
  transition: color 0.3s;
}

.auth-back-link:hover {
  color: white;
}

/* Auth Content */
.auth-content {
  flex: 1;
  display: flex;
  flex-direction: column;
  justify-content: center;
  padding: 2rem;
  max-width: 36rem;
  margin: 0 auto;
  width: 100%;
}

.auth-title-section {
  margin-bottom: 2rem;
}

.auth-title {
  font-size: 1.875rem;
  font-weight: 600;
  letter-spacing: -0.025em;
  color: white;
  margin-bottom: 0.5rem;
}

.auth-subtitle {
  color: rgb(113, 113, 122);
  font-size: 0.875rem;
}

/* Social Auth */
.social-auth-grid {
  display: grid;
  grid-template-columns: repeat(2, 1fr);
  gap: 0.75rem;
  margin-bottom: 1.5rem;
}

.social-auth-btn {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 0.5rem;
  padding: 0.625rem 1rem;
  border-radius: 0.5rem;
  background-color: rgb(24, 24, 27);
  border: 1px solid rgb(39, 39, 42);
  color: rgb(161, 161, 170);
  font-size: 0.875rem;
  font-weight: 500;
  cursor: pointer;
  transition: all 0.3s;
}

.social-auth-btn:hover {
  background-color: rgb(39, 39, 42);
  border-color: rgb(63, 63, 70);
  color: white;
}

/* Divider */
.auth-divider {
  position: relative;
  margin-bottom: 1.5rem;
}

.auth-divider-line {
  position: absolute;
  inset: 0;
  display: flex;
  align-items: center;
}

.auth-divider-line::before {
  content: '';
  width: 100%;
  border-top: 1px solid rgb(39, 39, 42);
}

.auth-divider-content {
  position: relative;
  display: flex;
  justify-content: center;
  font-size: 0.75rem;
  text-transform: uppercase;
}

.auth-divider-text {
  background-color: #000;
  padding: 0 0.5rem;
  color: rgb(82, 82, 91);
  font-family: var(--font-mono);
  letter-spacing: 0.1em;
}

/* Form */
.auth-form {
  display: flex;
  flex-direction: column;
  gap: 1rem;
}

.signup-fields {
  display: flex;
  flex-direction: column;
  gap: 1rem;
}

.name-grid {
  display: grid;
  grid-template-columns: repeat(2, 1fr);
  gap: 1rem;
}

.input-group {
  display: flex;
  flex-direction: column;
  gap: 0.375rem;
}

.input-label {
  font-size: 0.75rem;
  font-weight: 500;
  color: rgb(161, 161, 170);
}

.password-label-row {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.forgot-password-link {
  font-size: 0.625rem;
  color: rgb(113, 113, 122);
  text-decoration: none;
  transition: color 0.3s;
}

.forgot-password-link:hover {
  color: rgb(16, 185, 129);
}

.input-wrapper {
  position: relative;
}

.input-field {
  width: 100%;
  background-color: rgba(24, 24, 27, 0.5);
  border: 1px solid rgb(39, 39, 42);
  color: white;
  font-size: 0.875rem;
  border-radius: 0.5rem;
  padding: 0.625rem 0.75rem;
  transition: all 0.3s;
}

.input-field:focus {
  outline: none;
  border-color: rgba(16, 185, 129, 0.5);
  box-shadow: 0 0 0 1px rgba(16, 185, 129, 0.5);
}

.input-field::placeholder {
  color: rgb(63, 63, 70);
}

.input-with-icon {
  padding-left: 2.25rem;
}

.input-icon {
  position: absolute;
  left: 0.75rem;
  top: 0.75rem;
  color: rgb(82, 82, 91);
}

/* Input Autofill Override */
.input-field:-webkit-autofill,
.input-field:-webkit-autofill:hover,
.input-field:-webkit-autofill:focus,
.input-field:-webkit-autofill:active {
  -webkit-box-shadow: 0 0 0 30px #09090b inset !important;
  -webkit-text-fill-color: white !important;
  transition: background-color 5000s ease-in-out 0s;
}

/* Submit Button */
.submit-btn {
  width: 100%;
  background-color: rgb(16, 185, 129);
  color: #000;
  font-weight: 600;
  font-size: 0.875rem;
  border-radius: 0.5rem;
  padding: 0.625rem;
  margin-top: 0.5rem;
  border: none;
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 0.5rem;
  transition: all 0.3s;
  box-shadow: 0 0 20px rgba(16, 185, 129, 0.15);
}

.submit-btn:hover {
  background-color: rgb(52, 211, 153);
  box-shadow: 0 0 30px rgba(16, 185, 129, 0.3);
}

.submit-arrow {
  transition: transform 0.3s;
}

.submit-btn:hover .submit-arrow {
  transform: translateX(0.125rem);
}

/* Toggle Section */
.toggle-section {
  margin-top: 1.5rem;
  text-align: center;
}

.toggle-text {
  font-size: 0.875rem;
  color: rgb(113, 113, 122);
}

.toggle-btn {
  color: rgb(16, 185, 129);
  font-weight: 500;
  margin-left: 0.25rem;
  background: none;
  border: none;
  cursor: pointer;
  transition: color 0.3s;
  font-size: 0.875rem;
}

.toggle-btn:hover {
  color: rgb(52, 211, 153);
}

/* Footer */
.auth-footer {
  padding: 1.5rem 2rem;
  text-align: center;
}

.auth-footer-text {
  font-size: 0.625rem;
  color: rgb(82, 82, 91);
  font-family: var(--font-mono);
}

/* Right Panel: Visual */
.visual-panel {
  display: none;
  flex: 1;
  background-color: rgb(9, 9, 11);
  position: relative;
  overflow: hidden;
  align-items: center;
  justify-content: center;
  border-left: 1px solid rgba(255, 255, 255, 0.05);
}

.visual-grid {
  position: absolute;
  inset: 0;
  background-image: 
    linear-gradient(rgba(255, 255, 255, 0.02) 1px, transparent 1px),
    linear-gradient(90deg, rgba(255, 255, 255, 0.02) 1px, transparent 1px);
  background-size: 60px 60px;
}

.visual-gradient {
  position: absolute;
  inset: 0;
  background: linear-gradient(to top, #000 0%, transparent 50%, transparent 100%);
}

.visual-blob {
  position: absolute;
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);
  width: 600px;
  height: 600px;
  background-color: rgba(16, 185, 129, 0.1);
  border-radius: 50%;
  filter: blur(120px);
  animation: pulse 4s ease-in-out infinite;
}

/* Digital Twin Card */
.digital-twin-card {
  position: relative;
  z-index: 10;
  width: 24rem;
  backdrop-filter: blur(24px);
  background-color: rgba(0, 0, 0, 0.4);
  border: 1px solid rgba(255, 255, 255, 0.1);
  border-radius: 1rem;
  padding: 1.5rem;
  box-shadow: 0 25px 50px -12px rgba(0, 0, 0, 0.5);
  animation: fade-in 0.5s cubic-bezier(0.16, 1, 0.3, 1) forwards;
}

.card-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  margin-bottom: 1.5rem;
}

.card-status {
  display: flex;
  align-items: center;
  gap: 0.75rem;
}

.status-dot {
  width: 0.5rem;
  height: 0.5rem;
  border-radius: 50%;
  background-color: rgb(16, 185, 129);
  animation: pulse 2s ease-in-out infinite;
  box-shadow: 0 0 10px rgb(16, 185, 129);
}

.status-text {
  font-size: 0.75rem;
  font-family: var(--font-mono);
  color: rgb(52, 211, 153);
  letter-spacing: 0.1em;
  text-transform: uppercase;
}

.card-id {
  font-size: 0.625rem;
  color: rgb(113, 113, 122);
  font-family: var(--font-mono);
}

/* Visualization Area */
.visualization-area {
  height: 8rem;
  border-radius: 0.5rem;
  background-color: rgba(24, 24, 27, 0.5);
  border: 1px solid rgba(255, 255, 255, 0.05);
  position: relative;
  overflow: hidden;
  margin-bottom: 1.5rem;
  display: flex;
  align-items: flex-end;
  justify-content: space-between;
  padding: 0.5rem;
  gap: 0.25rem;
}

.bar-wrapper {
  width: 100%;
  background-color: rgba(16, 185, 129, 0.2);
  height: 40%;
  border-radius: 0.125rem;
  position: relative;
  overflow: hidden;
}

.bar-70 { height: 70%; }
.bar-50 { height: 50%; }
.bar-80 { height: 80%; }
.bar-30 { height: 30%; }

.bar-fill {
  position: absolute;
  bottom: 0;
  width: 100%;
  background-color: rgb(16, 185, 129);
  height: 60%;
}

.bar-1 { animation: pulse 2s ease-in-out infinite; }
.bar-2 { height: 40%; animation: pulse 3s ease-in-out infinite; }
.bar-3 { height: 80%; animation: pulse 1.5s ease-in-out infinite; }
.bar-4 { height: 50%; animation: pulse 2.5s ease-in-out infinite; }
.bar-5 { height: 70%; animation: pulse 2s ease-in-out infinite; }

.grid-line {
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 1px;
  background-color: rgba(16, 185, 129, 0.5);
  animation: grid-move 3s linear infinite;
}

@keyframes grid-move {
  0% { transform: translateY(0); }
  100% { transform: translateY(40px); }
}

/* Stats Grid */
.stats-grid {
  display: grid;
  grid-template-columns: repeat(2, 1fr);
  gap: 1rem;
}

.stat-card {
  padding: 0.75rem;
  border-radius: 0.5rem;
  background-color: rgba(255, 255, 255, 0.05);
  border: 1px solid rgba(255, 255, 255, 0.05);
}

.stat-label {
  font-size: 0.625rem;
  color: rgb(113, 113, 122);
  font-weight: 500;
  margin-bottom: 0.25rem;
}

.stat-value {
  font-size: 1.25rem;
  font-weight: 600;
  color: white;
  letter-spacing: -0.025em;
  display: flex;
  align-items: flex-end;
  gap: 0.25rem;
}

.stat-indicator {
  font-size: 0.625rem;
  margin-bottom: 0.25rem;
}

.stat-up {
  color: rgb(16, 185, 129);
}

.stat-down {
  color: rgb(16, 185, 129);
}

/* Terminal Output */
.terminal-output {
  margin-top: 1rem;
  padding-top: 1rem;
  border-top: 1px solid rgba(255, 255, 255, 0.05);
  font-family: var(--font-mono);
  font-size: 0.625rem;
  line-height: 1.75;
  color: rgb(113, 113, 122);
}

.terminal-line {
  display: flex;
  gap: 0.5rem;
}

.terminal-prompt {
  color: rgb( 16, 185, 129);
}

/* Floating Quote */
.floating-quote {
  position: absolute;
  bottom: 3rem;
  left: 3rem;
  right: 3rem;
  text-align: center;
}

.quote-text {
  font-size: 1.125rem;
  color: rgb(161, 161, 170);
  font-weight: 500;
  line-height: 1.75;
}

.quote-attribution {
  margin-top: 1rem;
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 0.5rem;
  font-size: 0.75rem;
  font-family: var(--font-mono);
  color: rgb(82, 82, 91);
  text-transform: uppercase;
  letter-spacing: 0.1em;
}

.quote-dot {
  width: 0.25rem;
  height: 0.25rem;
  border-radius: 50%;
  background-color: rgb(82, 82, 91);
}

/* Animations */
@keyframes fade-in {
  from {
    opacity: 0;
    transform: translateY(10px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

@keyframes pulse {
  0%, 100% {
    opacity: 1;
  }
  50% {
    opacity: 0.7;
  }
}

/* Transitions */
.fade-enter-active, .fade-leave-active {
  transition: opacity 0.3s ease, transform 0.3s ease;
}

.fade-enter-from, .fade-leave-to {
  opacity: 0;
  transform: translateY(-10px);
}

/* Responsive */
@media (min-width: 768px) {
  .auth-header {
    padding: 3rem;
  }
  
  .auth-content {
    padding: 5rem;
  }
  
  .auth-footer {
    text-align: left;
  }
}

@media (min-width: 1024px) {
  .auth-panel {
    width: 45%;
  }
  
  .visual-panel {
    display: flex;
  }
}
</style>
