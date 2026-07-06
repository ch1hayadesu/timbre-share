<template>
  <div class="steps">
    <div v-for="(step, index) in steps" :key="index" class="step"
      :class="{ done: index < current, active: index === current }">
      <div class="step-dot">{{ index < current ? '✓' : (index + 1) }}</div>
      <div class="step-info">{{ step }}</div>
    </div>
  </div>
</template>

<script setup>
defineProps({
  steps: { type: Array, required: true },
  current: { type: Number, default: 0 },
})
</script>

<style scoped>
.steps {
  display: flex;
  margin-bottom: var(--space-8);
}

.step {
  flex: 1;
  display: flex;
  align-items: center;
  gap: var(--space-3);
}

.step:not(:last-child)::after {
  content: '';
  flex: 1;
  height: 2px;
  background: var(--color-border-default);
  margin: 0 var(--space-3);
}

.step.done:not(:last-child)::after {
  background: var(--color-primary-6);
}

.step.active:not(:last-child)::after {
  background: var(--gradient-ai);
}

.step-dot {
  width: 28px;
  height: 28px;
  border-radius: 50%;
  flex-shrink: 0;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: var(--font-size-xs);
  font-weight: 700;
  border: 2px solid var(--color-border-default);
  color: var(--color-text-disabled);
  background: white;
}

.step.done .step-dot {
  border-color: var(--color-primary-6);
  background: var(--color-primary-6);
  color: white;
}

.step.active .step-dot {
  border-color: var(--color-primary-6);
  background: white;
  color: var(--color-primary-6);
  animation: pulse 1.5s ease-in-out infinite;
}

.step-info {
  font-size: var(--font-size-base);
  font-weight: 500;
  color: var(--color-text-disabled);
}

.step.done .step-info { color: var(--color-text-body); }
.step.active .step-info { color: var(--color-primary-6); }

@keyframes pulse {
  0%, 100% { opacity: 1; }
  50% { opacity: 0.4; }
}

@media (max-width: 767px) {
  .steps { flex-wrap: wrap; }
}
</style>
