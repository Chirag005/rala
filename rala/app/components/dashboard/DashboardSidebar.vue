<template>
  <aside class="sidebar">
    <a href="#" class="logo-link">
      <span class="logo-text">RAALA</span>
    </a>

    <nav class="nav-menu">
      <NuxtLink to="/dashboard" class="nav-btn nav-btn-active">
        <iconify-icon icon="lucide:layout-grid" width="20"></iconify-icon>
      </NuxtLink>
      <button class="nav-btn">
        <iconify-icon icon="lucide:sprout" width="20"></iconify-icon>
      </button>
      <button class="nav-btn">
        <iconify-icon icon="lucide:cpu" width="20"></iconify-icon>
      </button>
      <button class="nav-btn">
        <iconify-icon icon="lucide:settings-2" width="20"></iconify-icon>
      </button>
    </nav>

    <div class="user-avatar">OP</div>
  </aside>
</template>

<style scoped>

.logo-link {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  text-decoration: none;
  width: 2rem;
  height: 2rem;
  border-radius: 0.75rem;
  justify-content: center;
  color: #fff;
  font-weight: 700;
  box-shadow: 0 0 15px rgba(16, 185, 129, 0.3);
  margin-bottom: 2rem;

}

.logo-link:hover .logo-text:hover {
  color: #10b981;
}

.logo-text {
  font-size: 1.125rem;
  font-weight: 600;
  letter-spacing: -0.025em;
  color: #fff;
  transition: color 300ms ease;
}

.sidebar {
  width: 5rem;
  border-right: 1px solid rgba(255, 255, 255, 0.05);
  background-color: rgba(16, 185, 129, 0.03);
  backdrop-filter: blur(24px);
  display: flex;
  flex-direction: column;
  align-items: center;
  padding: 2rem 0 1.5rem 0;
  z-index: 20;
}


@media (max-width: 768px) {
  .sidebar {
    width: 100%;
    height: 4rem;
    flex-direction: row;
    justify-content: space-between;
    padding: 0 1rem;
    border-right: none;
    border-bottom: 1px solid rgba(255, 255, 255, 0.05);
  }
}

.logo {
  
}

@media (max-width: 768px) {
  .logo {
    margin-bottom: 0;
  }
}

.nav-menu {
  flex: 1;
  display: flex;
  flex-direction: column;
  gap: 1.5rem;
  width: 100%;
  align-items: center;
}

@media (max-width: 768px) {
  .nav-menu {
    flex-direction: row;
    gap: 1rem;
    width: auto;
  }
}

.nav-btn {
  width: 2.5rem;
  height: 2.5rem;
  border-radius: 0.5rem;
  color: #71717a;
  background: transparent;
  border: none;
  display: flex;
  align-items: center;
  justify-content: center;
  transition: all 300ms ease;
  cursor: pointer;
  text-decoration: none;
}

.nav-btn:hover {
  color: #e4e4e7;
  background-color: rgba(255, 255, 255, 0.05);
}

.nav-btn-active {
  background-color: rgba(16, 185, 129, 0.1);
  color: #34d399;
  border: 1px solid rgba(16, 185, 129, 0.2);
}

.nav-btn-active:hover {
  background-color: #10b981;
  color: #000;
}

.user-avatar {
  width: 2rem;
  height: 2rem;
  border-radius: 50%;
  background-color: #27272a;
  border: 1px solid #3f3f46;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 0.625rem;
  cursor: pointer;
  transition: border-color 300ms;
}

.user-avatar:hover {
  border-color: #10b981;
}

@media (max-width: 768px) {
  .user-avatar {
    margin-left: 1rem;
  }
}
</style>
