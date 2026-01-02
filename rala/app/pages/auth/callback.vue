<script setup lang="ts">
// This page handles the OAuth callback from Supabase
const user = useSupabaseUser()

// Wait for auth to complete, then redirect
watchEffect(() => {
  if (user.value) {
    navigateTo('/dashboard')
  }
})
</script>

<template>
  <div class="callback-container">
    <div class="callback-content">
      <div class="loader"></div>
      <h2>Authenticating...</h2>
      <p>Please wait while we sign you in</p>
    </div>
  </div>
</template>

<style scoped>
.callback-container {
  min-height: 100vh;
  display: flex;
  align-items: center;
  justify-content: center;
  background-color: #000;
  color: white;
}

.callback-content {
  text-align: center;
}

.loader {
  width: 48px;
  height: 48px;
  border: 3px solid rgba(16, 185, 129, 0.2);
  border-top-color: rgb(16, 185, 129);
  border-radius: 50%;
  animation: spin 1s linear infinite;
  margin: 0 auto 1.5rem;
}

@keyframes spin {
  to { transform: rotate(360deg); }
}

h2 {
  font-size: 1.5rem;
  font-weight: 600;
  margin-bottom: 0.5rem;
  color: white;
}

p {
  color: rgb(161, 161, 170);
  font-size: 0.875rem;
}
</style>
