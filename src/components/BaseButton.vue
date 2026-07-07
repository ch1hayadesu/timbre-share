<template>
  <button class="btn" :class="classes" :disabled="disabled" @click="$emit('click', $event)">
    <slot />
  </button>
</template>

<script setup>
import { computed } from 'vue'

const props = defineProps({
  type: { type: String, default: 'default' },
  size: { type: String, default: 'md' },
  disabled: { type: Boolean, default: false },
})

defineEmits(['click'])

const classes = computed(() => ({
  'btn-primary': props.type === 'primary',
  'btn-default': props.type === 'default',
  'btn-danger': props.type === 'danger',
  'btn-text': props.type === 'text',
  'btn-sm': props.size === 'sm',
  'btn-lg': props.size === 'lg',
}))
</script>

<style scoped>
.btn {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  gap: 6px;
  height: 40px;
  padding: 0 var(--space-5);
  border-radius: var(--radius-md);
  font-size: var(--font-size-base);
  font-weight: 500;
  cursor: pointer;
  border: none;
  transition: all var(--duration-fast) var(--ease-out);
  white-space: nowrap;
}

.btn:active {
  transform: scale(0.98);
}

.btn-primary {
  background: var(--color-primary-6);
  color: white;
}

.btn-primary:hover {
  background: var(--color-primary-7);
}

.btn-primary:disabled {
  background: var(--color-text-disabled);
  cursor: not-allowed;
  transform: none;
}

.btn-default {
  background: white;
  color: var(--color-text-body);
  border: 1px solid var(--color-border-default);
}

.btn-default:hover {
  border-color: var(--color-primary-6);
  color: var(--color-primary-6);
  background: var(--color-bg-selected);
}

.btn-danger {
  background: var(--color-error);
  color: white;
}

.btn-danger:hover {
  background: #DC2626;
}

.btn-text {
  background: none;
  color: var(--color-link);
  padding: 0 var(--space-2);
  height: 32px;
}

.btn-text:hover {
  background: var(--color-bg-selected);
}

.btn-sm {
  height: 32px;
  padding: 0 var(--space-3);
  font-size: var(--font-size-sm);
  border-radius: 6px;
}

.btn-lg {
  height: 48px;
  padding: 0 28px;
  font-size: var(--font-size-md);
  font-weight: 600;
  border-radius: 10px;
}
</style>
