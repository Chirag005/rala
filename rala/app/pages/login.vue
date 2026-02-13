<template>
  <div>
    <!-- Notification Toast -->
    <Transition name="slide-down">
      <div v-if="notification.show" :class="['notification-toast', `notification-${notification.type}`]">
        <iconify-icon 
          :icon="notification.type === 'success' ? 'lucide:check-circle' : notification.type === 'error' ? 'lucide:alert-circle' : 'lucide:info'"
          width="20"
        ></iconify-icon>
        <span>{{ notification.message }}</span>
        <button @click="notification.show = false" class="notification-close">
          <iconify-icon icon="lucide:x" width="16"></iconify-icon>
        </button>
      </div>
    </Transition>

    <div class="auth-container">
    <!-- Left Panel: Form -->
    <div class="auth-panel">
      <!-- Header -->
      <div class="auth-header">
        <NuxtLink to="/" class="auth-logo-link">
          <div class="auth-logo-box">
            <span class="auth-logo-letter">R</span>
          </div>
          <span class="auth-logo-text">RAALA</span>
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
        <!-- Loading Overlay -->
        <Transition name="fade">
          <div v-if="isLoading" class="loading-overlay">
            <div class="loading-spinner"></div>
          </div>
        </Transition>

        <div class="social-auth-grid">
          <button @click="loginWithGithub" class="social-auth-btn" :disabled="isLoading">
            <iconify-icon icon="lucide:github" width="16"></iconify-icon>
            GitHub
          </button>
          <button @click="loginWithGoogle" class="social-auth-btn" :disabled="isLoading">
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
                  <label class="input-label">First Name <span class="required-asterisk">*</span></label>
                  <input 
                    v-model="firstName" 
                    type="text" 
                    class="input-field" 
                    placeholder="John"
                    required
                  >
                </div>
                <div class="input-group">
                  <label class="input-label">Last Name <span class="required-asterisk">*</span></label>
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
            <label class="input-label">Email <span class="required-asterisk">*</span></label>
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
            <!-- Email Error -->
            <Transition name="fade">
              <span v-if="emailError" class="error-message">{{ emailError }}</span>
            </Transition>
          </div>

          <div class="input-group">
            <div class="password-label-row">
              <label class="input-label">Password <span class="required-asterisk">*</span></label>
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
            <!-- Password Error -->
            <Transition name="fade">
              <span v-if="passwordError" class="error-message">{{ passwordError }}</span>
            </Transition>
            <!-- Password Strength Indicator (Sign Up Only) -->
            <Transition name="fade">
              <div v-if="isSignup && password" class="password-strength">
                <div class="strength-label">
                  Password strength: 
                  <span :class="[
                    'strength-text',
                    passwordStrength < 40 ? 'weak' : passwordStrength < 70 ? 'medium' : 'strong'
                  ]">
                    {{ passwordStrength < 40 ? 'Weak' : passwordStrength < 70 ? 'Medium' : 'Strong' }}
                  </span>
                </div>
                <div class="strength-bar">
                  <div 
                    class="strength-fill"
                    :class="[
                      passwordStrength < 40 ? 'weak' : passwordStrength < 70 ? 'medium' : 'strong'
                    ]"
                    :style="{ width: `${passwordStrength}%` }"
                  ></div>
                </div>
                <p class="strength-hint">Use 8+ chars with uppercase, lowercase, and numbers</p>
              </div>
            </Transition>
          </div>

          <button type="submit" class="submit-btn" :disabled="isLoading">
            <div v-if="isLoading" class="button-spinner"></div>
            <span v-else>{{ isSignup ? 'Create Account' : 'Sign In' }}</span>
            <iconify-icon v-if="!isLoading" icon="lucide:arrow-right" class="submit-arrow" width="16"></iconify-icon>
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
          SECURED BY RAALA NEURAL MESH v2.0
        </p>
      </div>
    </div>


    </div>

  </div>
</template>

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

// Loading & notification states
const isLoading = ref(false)
const notification = ref({
  show: false,
  message: '',
  type: 'error' as 'error' | 'success' | 'info'
})

// Form data
const email = ref('')
const password = ref('')
const firstName = ref('')
const lastName = ref('')
const company = ref('')

// Validation states
const emailError = ref('')
const passwordError = ref('')
const passwordStrength = ref(0)

// Email validation
const validateEmail = (email: string): boolean => {
  const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/
  if (!email) {
    emailError.value = 'Email is required'
    return false
  }
  if (!emailRegex.test(email)) {
    emailError.value = 'Please enter a valid email address'
    return false
  }
  emailError.value = ''
  return true
}

// Password validation
const validatePassword = (password: string): boolean => {
  if (!password) {
    passwordError.value = 'Password is required'
    return false
  }
  if (password.length < 8) {
    passwordError.value = 'Password must be at least 8 characters'
    return false
  }
  
  // Check for uppercase, lowercase, and number
  const hasUpperCase = /[A-Z]/.test(password)
  const hasLowerCase = /[a-z]/.test(password)
  const hasNumber = /\d/.test(password)
  
  if (isSignup.value) {
    if (!hasUpperCase || !hasLowerCase || !hasNumber) {
      passwordError.value = 'Password must contain uppercase, lowercase, and number'
      return false
    }
  }
  
  passwordError.value = ''
  return true
}

// Calculate password strength
const calculatePasswordStrength = (password: string): number => {
  let strength = 0
  if (password.length >= 8) strength += 25
  if (password.length >= 12) strength += 15
  if (/[a-z]/.test(password)) strength += 15
  if (/[A-Z]/.test(password)) strength += 15
  if (/\d/.test(password)) strength += 15
  if (/[^A-Za-z0-9]/.test(password)) strength += 15
  return Math.min(strength, 100)
}

// Watch password for strength calculation
watch(password, (newPassword) => {
  if (isSignup.value && newPassword) {
    passwordStrength.value = calculatePasswordStrength(newPassword)
  } else {
    passwordStrength.value = 0
  }
})

// Show notification helper
const showNotification = (message: string, type: 'error' | 'success' | 'info' = 'error') => {
  notification.value = { show: true, message, type }
  setTimeout(() => {
    notification.value.show = false
  }, 5000)
}

// Auth handlers
const loginWithGoogle = async () => {
  isLoading.value = true
  try {
    const { error } = await supabase.auth.signInWithOAuth({
      provider: 'google',
      options: { 
        redirectTo: `${window.location.origin}/auth/callback` 
      }
    })
    if (error) throw error
  } catch (error: any) {
    showNotification(error.message || 'Failed to sign in with Google', 'error')
  } finally {
    isLoading.value = false
  }
}

const loginWithGithub = async () => {
  isLoading.value = true
  try {
    const { error } = await supabase.auth.signInWithOAuth({
      provider: 'github',
      options: { 
        redirectTo: `${window.location.origin}/auth/callback` 
      }
    })
    if (error) throw error
  } catch (error: any) {
    showNotification(error.message || 'Failed to sign in with GitHub', 'error')
  } finally {
    isLoading.value = false
  }
}

const handleSubmit = async () => {
  // Validate inputs
  const isEmailValid = validateEmail(email.value)
  const isPasswordValid = validatePassword(password.value)
  
  if (!isEmailValid || !isPasswordValid) {
    return
  }
  
  isLoading.value = true
  
  try {
    if (isSignup.value) {
      // Validate required fields for signup
      if (!firstName.value.trim() || !lastName.value.trim()) {
        showNotification('Please fill in all required fields', 'error')
        isLoading.value = false
        return
      }
      
      // Sign up
      const { data, error } = await supabase.auth.signUp({
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
      
      if (error) throw error
      
      if (data.user) {
        showNotification('Account created! Please check your email to confirm.', 'success')
        // Clear form
        firstName.value = ''
        lastName.value = ''
        company.value = ''
        email.value = ''
        password.value = ''
      }
    } else {
      // Sign in
      const { data, error } = await supabase.auth.signInWithPassword({
        email: email.value,
        password: password.value
      })
      
      if (error) throw error
      
      if (data.user) {
        showNotification('Welcome back!', 'success')
        // Redirect will happen automatically via watchEffect
        setTimeout(() => {
          navigateTo('/dashboard')
        }, 500)
      }
    }
  } catch (error: any) {
    console.error('Auth error:', error)
    showNotification(error.message || 'Authentication failed', 'error')
  } finally {
    isLoading.value = false
  }
}

const toggleAuthMode = () => {
  isSignup.value = !isSignup.value
  // Clear errors when switching modes
  emailError.value = ''
  passwordError.value = ''
  passwordStrength.value = 0
}

// SEO
useHead({
  title: 'RAALA - Access Control',
  meta: [
    { name: 'description', content: 'Sign in to access your RAALA autonomous greenhouse dashboard' }
  ]
})
</script>

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

.required-asterisk {
  color: rgb(239, 68, 68);
  margin-left: 0.125rem;
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

.submit-btn:disabled {
  opacity: 0.6;
  cursor: not-allowed;
}

.submit-btn:disabled:hover {
  background-color: rgb(16, 185, 129);
  box-shadow: 0 0 20px rgba(16, 185, 129, 0.15);
}

/* Button Loading Spinner */
.button-spinner {
  width: 20px;
  height: 20px;
  border: 2px solid rgba(0, 0, 0, 0.3);
  border-top-color: #000;
  border-radius: 50%;
  animation: spin 0.8s linear infinite;
}

@keyframes spin {
  to { transform: rotate(360deg); }
}

/* Notification Toast */
.notification-toast {
  position: fixed;
  top: 2rem;
  left: 50%;
  transform: translateX(-50%);
  z-index: 9999;
  display: flex;
  align-items: center;
  gap: 0.75rem;
  padding: 1rem 1.5rem;
  border-radius: 0.5rem;
  box-shadow: 0 10px 40px rgba(0, 0, 0, 0.3);
  backdrop-filter: blur(12px);
  min-width: 320px;
  max-width: 500px;
}

.notification-toast iconify-icon {
  flex-shrink: 0;
}

.notification-toast span {
  flex: 1;
  font-size: 0.875rem;
  font-weight: 500;
}

.notification-close {
  background: none;
  border: none;
  cursor: pointer;
  padding: 0.25rem;
  display: flex;
  align-items: center;
  justify-content: center;
  border-radius: 0.25rem;
  transition: background-color 0.2s;
}

.notification-success {
  background-color: rgba(16, 185, 129, 0.95);
  color: white;
  border: 1px solid rgba(255, 255, 255, 0.2);
}

.notification-success .notification-close:hover {
  background-color: rgba(255, 255, 255, 0.2);
}

.notification-error {
  background-color: rgba(239, 68, 68, 0.95);
  color: white;
  border: 1px solid rgba(255, 255, 255, 0.2);
}

.notification-error .notification-close:hover {
  background-color: rgba(255, 255, 255, 0.2);
}

.notification-info {
  background-color: rgba(59, 130, 246, 0.95);
  color: white;
  border: 1px solid rgba(255, 255, 255, 0.2);
}

.notification-info .notification-close:hover {
  background-color: rgba(255, 255, 255, 0.2);
}

/* Slide Down Animation for Toast */
.slide-down-enter-active {
  animation: slide-down 0.3s ease-out;
}

.slide-down-leave-active {
  animation: slide-down 0.3s ease-out reverse;
}

@keyframes slide-down {
  from {
    transform: translateX(-50%) translateY(-100%);
    opacity: 0;
  }
  to {
    transform: translateX(-50%) translateY(0);
    opacity: 1;
  }
}

/* Loading Overlay */
.loading-overlay {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background-color: rgba(0, 0, 0, 0.5);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 9998;
  backdrop-filter: blur(4px);
}

.loading-spinner {
  width: 48px;
  height: 48px;
  border: 4px solid rgba(16, 185, 129, 0.2);
  border-top-color: rgb(16, 185, 129);
  border-radius: 50%;
  animation: spin 0.8s linear infinite;
}

/* Error Message */
.error-message {
  display: block;
  font-size: 0.75rem;
  color: rgb(239, 68, 68);
  margin-top: 0.375rem;
  font-weight: 500;
}

/* Password Strength Indicator */
.password-strength {
  margin-top: 0.75rem;
}

.strength-label {
  font-size: 0.75rem;
  color: rgb(161, 161, 170);
  margin-bottom: 0.375rem;
  display: flex;
  align-items: center;
  gap: 0.25rem;
}

.strength-text {
  font-weight: 600;
}

.strength-text.weak {
  color: rgb(239, 68, 68);
}

.strength-text.medium {
  color: rgb(234, 179, 8);
}

.strength-text.strong {
  color: rgb(16, 185, 129);
}

.strength-bar {
  width: 100%;
  height: 6px;
  background-color: rgb(39, 39, 42);
  border-radius: 3px;
  overflow: hidden;
  margin-bottom: 0.375rem;
}

.strength-fill {
  height: 100%;
  transition: all 0.3s ease;
  border-radius: 3px;
}

.strength-fill.weak {
  background-color: rgb(239, 68, 68);
}

.strength-fill.medium {
  background-color: rgb(234, 179, 8);
}

.strength-fill.strong {
  background-color: rgb(16, 185, 129);
}

.strength-hint {
  font-size: 0.625rem;
  color: rgb(113, 113, 122);
  margin: 0;
}

/* Disabled State for Social Auth Buttons */
.social-auth-btn:disabled {
  opacity: 0.5;
  cursor: not-allowed;
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

</style>
