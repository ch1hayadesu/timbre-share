<template>
  <div class="ai-loading">
    <div class="ai-loading-dots">
      <div class="ai-loading-dot"></div>
      <div class="ai-loading-dot"></div>
      <div class="ai-loading-dot"></div>
    </div>
    <span class="ai-loading-text">{{ text }}</span>
  </div>
</template>

<script setup>
defineProps({
  text: { type: String, default: 'AI 正在处理...' }
})
</script>

<style scoped>
.ai-loading {
  display: flex;
  align-items: center;
  gap: var(--space-2);
  padding: var(--space-6);
  justify-content: center;
}

.ai-loading-dots {
  display: flex;
  gap: 6px;
}

.ai-loading-dot {
  width: 8px;
  height: 8px;
  border-radius: 50%;
  background: var(--color-primary-5);
  animation: dotBounce 0.6s ease-in-out infinite;
}

.ai-loading-dot:nth-child(2) { animation-delay: 0.1s; }
.ai-loading-dot:nth-child(3) { animation-delay: 0.2s; }

.ai-loading-text {
  font-size: var(--font-size-base);
  color: var(--color-text-secondary);
}

@keyframes dotBounce {
  0%, 100% { transform: translateY(0); }
  50% { transform: translateY(-8px); }
}
</style>
