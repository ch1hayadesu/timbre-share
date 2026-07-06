<template>
  <div class="progress-container">
    <div class="progress">
      <div class="progress-fill" :style="{ width: percent + '%' }"></div>
    </div>
    <p class="progress-text">{{ percent }}%</p>
  </div>
</template>

<script setup>
defineProps({
  percent: { type: Number, default: 0 },
})
</script>

<style scoped>
.progress-container {
  max-width: 400px;
  margin: 0 auto;
}

.progress {
  height: 6px;
  border-radius: 3px;
  background: var(--color-border-light);
  overflow: hidden;
  margin-bottom: var(--space-4);
}

.progress-fill {
  height: 100%;
  border-radius: 3px;
  background: var(--gradient-ai);
  transition: width var(--duration-slow) var(--ease-out);
  position: relative;
  overflow: hidden;
}

.progress-fill::after {
  content: '';
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: linear-gradient(90deg, transparent, rgba(255, 255, 255, 0.4), transparent);
  animation: shimmer 1.5s ease-in-out infinite;
}

.progress-text {
  font-size: var(--font-size-sm);
  color: var(--color-text-secondary);
  text-align: center;
}

@keyframes shimmer {
  0% { transform: translateX(-100%); }
  100% { transform: translateX(100%); }
}
</style>
