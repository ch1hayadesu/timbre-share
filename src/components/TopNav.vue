<template>
  <div class="topnav">
    <button class="topnav-btn topnav-hamburger" @click="$emit('toggle-sidebar')">
      <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
        <line x1="3" y1="6" x2="21" y2="6" /><line x1="3" y1="12" x2="21" y2="12" /><line x1="3" y1="18" x2="21" y2="18" />
      </svg>
    </button>

    <router-link to="/dashboard" class="topnav-logo">
      <div class="topnav-logo-icon">♪</div>
      <span>音色共享平台</span>
    </router-link>

    <div class="topnav-nav">
      <router-link v-for="item in navItems" :key="item.path" :to="item.path"
        class="topnav-nav-item" active-class="active">
        {{ item.label }}
      </router-link>
    </div>

    <div class="topnav-right">
      <button class="topnav-btn" title="通知">
        <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
          <path d="M18 8A6 6 0 0 0 6 8c0 7-3 9-3 9h18s-3-2-3-9" />
          <path d="M13.73 21a2 2 0 0 1-3.46 0" />
        </svg>
        <span class="topnav-badge"></span>
      </button>
      <div class="topnav-user">
        <div class="topnav-avatar">X</div>
        <span class="topnav-username">小明</span>
        <svg width="12" height="12" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
          <path d="M6 9l6 6 6-6" />
        </svg>
      </div>
    </div>
  </div>
</template>

<script setup>
defineEmits(['toggle-sidebar'])

const navItems = [
  { path: '/dashboard', label: '工作台' },
  { path: '/clone', label: '音色克隆' },
  { path: '/tts', label: 'TTS合成' },
  { path: '/script', label: '剧本配音' },
  { path: '/market', label: '音色市场' },
]
</script>

<style scoped>
.topnav {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  z-index: 100;
  height: var(--topnav-h);
  background: var(--color-bg-container);
  border-bottom: 1px solid var(--color-border-light);
  display: flex;
  align-items: center;
  padding: 0 var(--space-6);
  box-shadow: var(--shadow-sm);
}

.topnav-logo {
  display: flex;
  align-items: center;
  gap: 10px;
  font-size: var(--font-size-lg);
  font-weight: 700;
  color: var(--color-text-primary);
  margin-right: var(--space-10);
  cursor: pointer;
}

.topnav-logo-icon {
  width: 34px;
  height: 34px;
  border-radius: var(--radius-md);
  background: var(--gradient-ai);
  display: flex;
  align-items: center;
  justify-content: center;
  color: white;
  font-size: var(--font-size-lg);
}

.topnav-nav {
  display: flex;
  gap: var(--space-1);
  flex: 1;
}

.topnav-nav-item {
  padding: var(--space-2) var(--space-4);
  border-radius: var(--radius-md);
  font-size: var(--font-size-base);
  font-weight: 500;
  color: var(--color-text-body);
  cursor: pointer;
  transition: all var(--duration-fast) var(--ease-out);
  border: none;
  background: none;
  white-space: nowrap;
}

.topnav-nav-item:hover {
  background: var(--color-bg-hover);
  color: var(--color-primary-6);
}

.topnav-nav-item.active {
  background: var(--color-bg-selected);
  color: var(--color-primary-6);
}

.topnav-right {
  display: flex;
  align-items: center;
  gap: var(--space-4);
}

.topnav-btn {
  width: 36px;
  height: 36px;
  border-radius: var(--radius-md);
  border: none;
  background: none;
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: center;
  color: var(--color-text-secondary);
  transition: all var(--duration-fast);
  position: relative;
}

.topnav-btn:hover {
  background: var(--color-bg-hover);
  color: var(--color-text-primary);
}

.topnav-badge {
  position: absolute;
  top: 4px;
  right: 4px;
  width: 8px;
  height: 8px;
  border-radius: 50%;
  background: var(--color-error);
}

.topnav-user {
  display: flex;
  align-items: center;
  gap: var(--space-2);
  cursor: pointer;
  padding: var(--space-1) var(--space-2);
  border-radius: var(--radius-md);
  transition: background var(--duration-fast);
}

.topnav-user:hover {
  background: var(--color-bg-hover);
}

.topnav-avatar {
  width: 32px;
  height: 32px;
  border-radius: 50%;
  background: var(--gradient-ai);
  color: white;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: var(--font-size-base);
  font-weight: 600;
}

.topnav-username {
  font-size: var(--font-size-base);
  font-weight: 500;
  color: var(--color-text-primary);
}

.topnav-hamburger {
  display: none !important;
  margin-right: var(--space-2);
}

@media (max-width: 1279px) {
  .topnav-hamburger {
    display: flex !important;
  }
  .topnav-nav {
    display: none;
  }
}
</style>
