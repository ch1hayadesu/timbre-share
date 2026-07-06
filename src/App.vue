<template>
  <div class="app-shell">
    <TopNav @toggle-sidebar="toggleSidebar" />
    <div v-if="sidebarOpen" class="sidebar-overlay" @click="closeSidebar"></div>
    <SideNav :is-open="sidebarOpen" @toast="handleToast" />
    <MainLayout />
    <ToastContainer />
    <ModalBox />
    <DrawerPanel />
  </div>
</template>

<script setup>
import { ref } from 'vue'
import TopNav from '@/components/TopNav.vue'
import SideNav from '@/components/SideNav.vue'
import MainLayout from '@/components/MainLayout.vue'
import ToastContainer from '@/components/ToastContainer.vue'
import ModalBox from '@/components/ModalBox.vue'
import DrawerPanel from '@/components/DrawerPanel.vue'
import { useToast } from '@/composables/useToast'

const { showToast } = useToast()
const sidebarOpen = ref(false)

function toggleSidebar() {
  sidebarOpen.value = !sidebarOpen.value
}

function closeSidebar() {
  sidebarOpen.value = false
}

function handleToast(type, message) {
  showToast(type, message)
}
</script>

<style scoped>
.app-shell {
  height: 100vh;
  overflow: hidden;
}

.sidebar-overlay {
  display: none;
}

@media (max-width: 1279px) {
  .sidebar-overlay {
    display: block;
    position: fixed;
    inset: 0;
    background: rgba(0, 0, 0, 0.3);
    z-index: 89;
  }
}
</style>
