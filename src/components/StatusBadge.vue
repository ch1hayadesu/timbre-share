<template>
  <span class="status-badge" :class="type"><slot /></span>
</template>

<script setup>
defineProps({
  type: { type: String, default: 'ready' }
})
</script>

<style scoped>
.status-badge {
  display: inline-flex;
  align-items: center;
  gap: 6px;
  padding: 2px 10px;
  border-radius: var(--radius-full);
  font-size: var(--font-size-xs);
  font-weight: 500;
}

.status-badge::before {
  content: '';
  width: 8px;
  height: 8px;
  border-radius: 50%;
  flex-shrink: 0;
}

.status-badge.ready { background: #ECFDF5; color: var(--color-success); }
.status-badge.ready::before { background: var(--color-success); }

.status-badge.processing { background: #FFFBEB; color: #D97706; }
.status-badge.processing::before { background: var(--color-warning); animation: pulse 1.5s ease-in-out infinite; }

.status-badge.failed { background: #FEF2F2; color: var(--color-error); }
.status-badge.failed::before { background: var(--color-error); }

.status-badge.shared { background: var(--color-bg-selected); color: var(--color-primary-6); }
.status-badge.shared::before { background: var(--color-primary-6); }

@keyframes pulse {
  0%, 100% { opacity: 1; }
  50% { opacity: 0.4; }
}
</style>
