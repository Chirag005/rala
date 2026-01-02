<script setup lang="ts">
const supabase = useSupabaseClient()
const user = useSupabaseUser()

// Protect this page - redirect to login if not authenticated
watchEffect(() => {
  if (!user.value) {
    navigateTo('/login')
  }
})

const signOut = async () => {
  await supabase.auth.signOut()
  navigateTo('/login')
}
</script>

<template>
  <div v-if="user" class="dashboard-container">
    <div class="dashboard-header">
      <div class="header-content">
        <div class="logo-section">
          <div class="logo-box">
            <span class="logo-letter">R</span>
          </div>
          <span class="logo-text">RALA Dashboard</span>
        </div>
        
        <div class="user-section">
          <div class="user-info">
            <p class="user-email">{{ user.email }}</p>
          </div>
          <button @click="signOut" class="sign-out-btn">
            <iconify-icon icon="lucide:log-out" width="16"></iconify-icon>
            Sign Out
          </button>
        </div>
      </div>
    </div>

    <div class="dashboard-content">
      <div class="welcome-card">
        <h1 class="welcome-title">Welcome to RALA</h1>
        <p class="welcome-text">
          You're successfully authenticated! This is your dashboard.
        </p>
        
        <div class="stats-grid">
          <div class="stat-card">
            <iconify-icon icon="lucide:zap" class="stat-icon" width="24"></iconify-icon>
            <div class="stat-info">
              <div class="stat-label">Energy Saved</div>
              <div class="stat-value">32%</div>
            </div>
          </div>
          
          <div class="stat-card">
            <iconify-icon icon="lucide:trending-up" class="stat-icon" width="24"></iconify-icon>
            <div class="stat-info">
              <div class="stat-label">Yield Increase</div>
              <div class="stat-value">12%</div>
            </div>
          </div>
          
          <div class="stat-card">
            <iconify-icon icon="lucide:activity" class="stat-icon" width="24"></iconify-icon>
            <div class="stat-info">
              <div class="stat-label">System Status</div>
              <div class="stat-value status-active">Active</div>
            </div>
          </div>
        </div>

        <div class="user-meta">
          <h3>User Information</h3>
          <div class="meta-grid">
            <div class="meta-item">
              <span class="meta-label">Email:</span>
              <span class="meta-value">{{ user.email }}</span>
            </div>
            <div class="meta-item">
              <span class="meta-label">User ID:</span>
              <span class="meta-value">{{ user.id }}</span>
            </div>
            <div v-if="user.user_metadata?.first_name" class="meta-item">
              <span class="meta-label">Name:</span>
              <span class="meta-value">{{ user.user_metadata.first_name }} {{ user.user_metadata.last_name }}</span>
            </div>
            <div v-if="user.user_metadata?.company" class="meta-item">
              <span class="meta-label">Company:</span>
              <span class="meta-value">{{ user.user_metadata.company }}</span>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<style scoped>
.dashboard-container {
  min-height: 100vh;
  background-color: #000;
  color: white;
}

.dashboard-header {
  border-bottom: 1px solid rgba(255, 255, 255, 0.05);
  background-color: rgba(0, 0, 0, 0.8);
  backdrop-filter: blur(12px);
  position: sticky;
  top: 0;
  z-index: 50;
}

.header-content {
  max-width: 1280px;
  margin: 0 auto;
  padding: 1.5rem 2rem;
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.logo-section {
  display: flex;
  align-items: center;
  gap: 0.75rem;
}

.logo-box {
  width: 2rem;
  height: 2rem;
  background-color: rgba(16, 185, 129, 0.1);
  border: 1px solid rgba(16, 185, 129, 0.3);
  border-radius: 0.375rem;
  display: flex;
  align-items: center;
  justify-content: center;
  color: rgb(52, 211, 153);
}

.logo-letter {
  font-weight: 700;
  font-size: 1rem;
}

.logo-text {
  font-size: 1.25rem;
  font-weight: 600;
  letter-spacing: -0.025em;
}

.user-section {
  display: flex;
  align-items: center;
  gap: 1.5rem;
}

.user-info {
  text-align: right;
}

.user-email {
  font-size: 0.875rem;
  color: rgb(161, 161, 170);
}

.sign-out-btn {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  padding: 0.625rem 1.25rem;
  background-color: rgba(16, 185, 129, 0.1);
  border: 1px solid rgba(16, 185, 129, 0.3);
  color: rgb(52, 211, 153);
  border-radius: 0.5rem;
  font-size: 0.875rem;
  font-weight: 500;
  cursor: pointer;
  transition: all 0.3s;
}

.sign-out-btn:hover {
  background-color: rgb(16, 185, 129);
  color: #000;
}

.dashboard-content {
  max-width: 1280px;
  margin: 0 auto;
  padding: 3rem 2rem;
}

.welcome-card {
  background: linear-gradient(135deg, rgba(16, 185, 129, 0.05) 0%, rgba(0, 0, 0, 0.3) 100%);
  border: 1px solid rgba(255, 255, 255, 0.1);
  border-radius: 1rem;
  padding: 3rem;
  backdrop-filter: blur(12px);
}

.welcome-title {
  font-size: 2.5rem;
  font-weight: 700;
  margin-bottom: 1rem;
  background: linear-gradient(135deg, #fff 0%, rgb(52, 211, 153) 100%);
  -webkit-background-clip: text;
  background-clip: text;
  -webkit-text-fill-color: transparent;
}

.welcome-text {
  font-size: 1.125rem;
  color: rgb(161, 161, 170);
  margin-bottom: 3rem;
}

.stats-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
  gap: 1.5rem;
  margin-bottom: 3rem;
}

.stat-card {
  display: flex;
  align-items: center;
  gap: 1rem;
  padding: 1.5rem;
  background-color: rgba(255, 255, 255, 0.03);
  border: 1px solid rgba(255, 255, 255, 0.05);
  border-radius: 0.75rem;
  transition: all 0.3s;
}

.stat-card:hover {
  background-color: rgba(16, 185, 129, 0.05);
  border-color: rgba(16, 185, 129, 0.2);
  transform: translateY(-2px);
}

.stat-icon {
  color: rgb(16, 185, 129);
}

.stat-info {
  flex: 1;
}

.stat-label {
  font-size: 0.75rem;
  color: rgb(113, 113, 122);
  margin-bottom: 0.25rem;
  text-transform: uppercase;
  letter-spacing: 0.05em;
}

.stat-value {
  font-size: 1.875rem;
  font-weight: 700;
  color: white;
}

.status-active {
  color: rgb(16, 185, 129);
  font-size: 1.25rem;
}

.user-meta {
  padding-top: 2rem;
  border-top: 1px solid rgba(255, 255, 255, 0.05);
}

.user-meta h3 {
  font-size: 1.25rem;
  font-weight: 600;
  margin-bottom: 1.5rem;
  color: white;
}

.meta-grid {
  display: grid;
  gap: 1rem;
}

.meta-item {
  display: flex;
  gap: 1rem;
  padding: 0.75rem 0;
}

.meta-label {
  font-size: 0.875rem;
  color: rgb(113, 113, 122);
  font-weight: 500;
  min-width: 100px;
}

.meta-value {
  font-size: 0.875rem;
  color: white;
  font-family: 'JetBrains Mono', monospace;
}
</style>
