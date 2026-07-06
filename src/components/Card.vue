<template>
  <div class="card" :class="{ 'card-clickable': clickable }" @click="$emit('click')">
    <slot />
  </div>
</template>

<script setup>
defineProps({
  clickable: { type: Boolean, default: false }
})
defineEmits(['click'])
</script>

<style scoped>
.card {
  background: var(--color-bg-container);
  border-radius: var(--radius-lg);
  border: 1px solid var(--color-border-light);
  box-shadow: var(--shadow-md);
  padding: var(--space-5);
  transition: all var(--duration-base) var(--ease-out);
}

.card-clickable {
  cursor: pointer;
}

.card-clickable:hover {
  box-shadow: var(--shadow-lg);
  transform: translateY(-2px);
}
</style>
