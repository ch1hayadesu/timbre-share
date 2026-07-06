<template>
  <span class="tag" :class="`tag-${type}`"><slot /></span>
</template>

<script setup>
defineProps({
  type: { type: String, default: 'default' }
})
</script>

<style scoped>
.tag {
  display: inline-flex;
  align-items: center;
  padding: 2px var(--space-2);
  border-radius: var(--radius-sm);
  font-size: var(--font-size-xs);
  font-weight: 500;
  line-height: 1.5;
}

.tag-default { background: var(--color-bg-section); color: #4B5563; }
.tag-primary { background: var(--color-bg-selected); color: var(--color-primary-6); }
.tag-success { background: #ECFDF5; color: var(--color-success); }
.tag-warning { background: #FFFBEB; color: #D97706; }
.tag-error { background: #FEF2F2; color: var(--color-error); }
.tag-info { background: #EFF6FF; color: var(--color-link); }
</style>
