<template>
  <Teleport to="body">
    <div v-if="drawerState.visible" class="drawer-overlay" @click="closeDrawer"></div>
    <div v-if="drawerState.visible" class="drawer">
      <div class="drawer-header">
        <h4 class="drawer-title">{{ drawerState.title }}</h4>
        <button class="drawer-close" @click="closeDrawer">✕</button>
      </div>
      <div class="drawer-body" v-html="drawerState.content"></div>
      <div class="drawer-footer">
        <BaseButton @click="closeDrawer">关闭</BaseButton>
      </div>
    </div>
  </Teleport>
</template>

<script setup>
import BaseButton from './BaseButton.vue'
import { useDrawer } from '@/composables/useDrawer'

const { drawerState, closeDrawer } = useDrawer()
</script>

<style scoped>
.drawer-overlay {
  position: fixed;
  inset: 0;
  z-index: 900;
  background: rgba(0, 0, 0, 0.3);
  animation: fadeIn var(--duration-base) var(--ease-out);
}

.drawer {
  position: fixed;
  top: 0;
  right: 0;
  bottom: 0;
  width: 420px;
  max-width: 90vw;
  background: white;
  z-index: 901;
  box-shadow: var(--shadow-xl);
  animation: drawerIn var(--duration-base) var(--ease-out);
  display: flex;
  flex-direction: column;
}

.drawer-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: var(--space-5) var(--space-6);
  border-bottom: 1px solid var(--color-border-light);
  flex-shrink: 0;
}

.drawer-title {
  font-size: var(--font-size-lg);
  font-weight: 500;
  color: var(--color-text-primary);
}

.drawer-close {
  width: 32px;
  height: 32px;
  border-radius: var(--radius-md);
  border: none;
  background: none;
  cursor: pointer;
  font-size: var(--font-size-lg);
  color: var(--color-text-secondary);
  display: flex;
  align-items: center;
  justify-content: center;
}

.drawer-close:hover {
  background: var(--color-bg-hover);
}

.drawer-body {
  flex: 1;
  overflow-y: auto;
  padding: var(--space-6);
}

.drawer-footer {
  padding: var(--space-4) var(--space-6);
  border-top: 1px solid var(--color-border-light);
  flex-shrink: 0;
}

@keyframes fadeIn {
  from { opacity: 0; }
  to { opacity: 1; }
}

@keyframes drawerIn {
  from { transform: translateX(100%); }
  to { transform: translateX(0); }
}
</style>
