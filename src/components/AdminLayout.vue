<template>
  <div class="admin-shell">
    <!-- 顶部导航 -->
    <header class="admin-topbar">
      <div class="admin-topbar-left">
        <button class="admin-menu-toggle" @click="toggleSidebar">
          <span></span><span></span><span></span>
        </button>
        <h1 class="admin-logo">运维管理平台</h1>
      </div>
      <div class="admin-topbar-right">
        <span class="admin-user">{{ adminName }}</span>
        <button class="admin-logout-btn" @click="handleLogout">退出登录</button>
      </div>
    </header>

    <!-- 侧边栏叠加层 (移动端) -->
    <div v-if="sidebarOpen" class="admin-sidebar-overlay" @click="closeSidebar"></div>

    <!-- 侧边栏 -->
    <aside class="admin-sidebar" :class="{ open: sidebarOpen }">
      <nav class="admin-nav">
        <router-link to="/admin/dashboard" class="admin-nav-item" active-class="active" @click="closeSidebar">
          <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><rect x="3" y="3" width="7" height="7"/><rect x="14" y="3" width="7" height="7"/><rect x="3" y="14" width="7" height="7"/><rect x="14" y="14" width="7" height="7"/></svg>
          <span>仪表盘</span>
        </router-link>
        <router-link to="/admin/users" class="admin-nav-item" active-class="active" @click="closeSidebar">
          <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M17 21v-2a4 4 0 0 0-4-4H5a4 4 0 0 0-4 4v2"/><circle cx="9" cy="7" r="4"/><path d="M23 21v-2a4 4 0 0 0-3-3.87"/><path d="M16 3.13a4 4 0 0 1 0 7.75"/></svg>
          <span>用户管理</span>
        </router-link>
        <router-link to="/admin/voices" class="admin-nav-item" active-class="active" @click="closeSidebar">
          <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M9 18V5l12-2v13"/><circle cx="6" cy="18" r="3"/><circle cx="18" cy="16" r="3"/></svg>
          <span>音色管理</span>
        </router-link>
        <router-link to="/admin/logs" class="admin-nav-item" active-class="active" @click="closeSidebar">
          <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z"/><polyline points="14 2 14 8 20 8"/><line x1="16" y1="13" x2="8" y2="13"/><line x1="16" y1="17" x2="8" y2="17"/><polyline points="10 9 9 9 8 9"/></svg>
          <span>操作日志</span>
        </router-link>
      </nav>
    </aside>

    <!-- 主内容区 -->
    <main class="admin-main">
      <router-view v-slot="{ Component }">
        <transition name="page" mode="out-in">
          <component :is="Component" />
        </transition>
      </router-view>
    </main>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import { useAuth } from '@/composables/useAuth'

const router = useRouter()
const { adminName, clearAdminToken } = useAuth()
const sidebarOpen = ref(false)

function toggleSidebar() {
  sidebarOpen.value = !sidebarOpen.value
}

function closeSidebar() {
  sidebarOpen.value = false
}

function handleLogout() {
  clearAdminToken()
  router.push('/admin/login')
}
</script>

<style scoped>
.admin-shell {
  display: flex;
  flex-direction: column;
  height: 100vh;
  background: #f0f2f5;
}

/* Top Bar */
.admin-topbar {
  height: 56px;
  background: #1a1a2e;
  color: #fff;
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 0 24px;
  flex-shrink: 0;
  z-index: 100;
}

.admin-topbar-left {
  display: flex;
  align-items: center;
  gap: 16px;
}

.admin-menu-toggle {
  display: none;
  flex-direction: column;
  gap: 4px;
  background: none;
  border: none;
  cursor: pointer;
  padding: 4px;
}

.admin-menu-toggle span {
  display: block;
  width: 20px;
  height: 2px;
  background: #fff;
  border-radius: 1px;
}

.admin-logo {
  font-size: 17px;
  font-weight: 600;
  letter-spacing: 0.5px;
}

.admin-topbar-right {
  display: flex;
  align-items: center;
  gap: 16px;
}

.admin-user {
  font-size: 13px;
  color: rgba(255,255,255,0.8);
}

.admin-logout-btn {
  padding: 6px 16px;
  background: rgba(255,255,255,0.1);
  color: rgba(255,255,255,0.9);
  border: 1px solid rgba(255,255,255,0.2);
  border-radius: 6px;
  font-size: 13px;
  cursor: pointer;
  transition: all 0.2s;
}

.admin-logout-btn:hover {
  background: rgba(255,255,255,0.2);
}

/* Sidebar */
.admin-sidebar-overlay {
  display: none;
}

.admin-sidebar {
  position: fixed;
  top: 56px;
  left: 0;
  bottom: 0;
  width: 220px;
  background: #1a1a2e;
  border-right: 1px solid rgba(255,255,255,0.05);
  overflow-y: auto;
  z-index: 90;
}

.admin-nav {
  padding: 12px 0;
}

.admin-nav-item {
  display: flex;
  align-items: center;
  gap: 12px;
  padding: 12px 24px;
  color: rgba(255,255,255,0.55);
  font-size: 14px;
  text-decoration: none;
  transition: all 0.2s;
  border-left: 3px solid transparent;
}

.admin-nav-item svg {
  width: 20px;
  height: 20px;
  flex-shrink: 0;
}

.admin-nav-item:hover {
  color: rgba(255,255,255,0.85);
  background: rgba(255,255,255,0.05);
}

.admin-nav-item.active {
  color: #fff;
  background: rgba(124,58,237,0.2);
  border-left-color: #8B5CF6;
}

/* Main Content */
.admin-main {
  margin-left: 220px;
  margin-top: 56px;
  flex: 1;
  overflow-y: auto;
  padding: 24px;
}

/* Page Transition */
.page-enter-active, .page-leave-active {
  transition: opacity 0.2s ease, transform 0.2s ease;
}

.page-enter-from {
  opacity: 0;
  transform: translateY(6px);
}

.page-leave-to {
  opacity: 0;
  transform: translateY(-6px);
}

/* Responsive */
@media (max-width: 1279px) {
  .admin-menu-toggle { display: flex; }

  .admin-sidebar {
    transform: translateX(-100%);
    transition: transform 0.25s ease;
  }

  .admin-sidebar.open {
    transform: translateX(0);
  }

  .admin-sidebar-overlay {
    display: block;
    position: fixed;
    inset: 0;
    top: 56px;
    background: rgba(0,0,0,0.4);
    z-index: 89;
  }

  .admin-main {
    margin-left: 0;
  }
}

@media (max-width: 767px) {
  .admin-topbar { padding: 0 16px; }
  .admin-main { padding: 16px; }
}
</style>
