<template>
  <Teleport to="body">
    <div class="toast-container">
      <div v-for="toast in toasts" :key="toast.id" class="toast" :class="`toast-${toast.type}`" @click="closeToast(toast.id)">
        <span>{{ iconMap[toast.type] }}</span>
        <span class="toast-msg">{{ toast.message }}</span>
        <span class="toast-close">✕</span>
      </div>
    </div>
  </Teleport>
</template>

<script setup>
import { useToast } from '@/composables/useToast'

const { toasts, closeToast } = useToast()

const iconMap = { success: '✓', warning: '⚠', error: '✕', info: 'ℹ' }
</script>

<style scoped>
.toast-container {
  position: fixed;
  top: 80px;
  left: 50%;
  transform: translateX(-50%);
  z-index: 2000;
  display: flex;
  flex-direction: column;
  gap: var(--space-2);
}

.toast {
  min-width: 320px;
  max-width: 480px;
  padding: 0 var(--space-4);
  height: 40px;
  border-radius: var(--radius-md);
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
  font-size: var(--font-size-base);
  display: flex;
  align-items: center;
  gap: var(--space-2);
  animation: toastIn var(--duration-base) var(--ease-spring);
  cursor: pointer;
}
.toast-msg { flex: 1; }
.toast-close { font-size: 12px; opacity: 0.5; }

.toast-success { background: #ECFDF5; border: 1px solid #A7F3D0; color: var(--color-success); }
.toast-warning { background: #FFFBEB; border: 1px solid #FDE68A; color: #D97706; }
.toast-error { background: #FEF2F2; border: 1px solid #FECACA; color: var(--color-error); }
.toast-info { background: var(--color-bg-selected); border: 1px solid #DDD6FE; color: var(--color-primary-6); }

@keyframes toastIn {
  from { opacity: 0; transform: translateY(-16px); }
  to { opacity: 1; transform: translateY(0); }
}
</style>
