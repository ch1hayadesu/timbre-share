<template>
  <div class="wave-animation">
    <div v-for="i in bars" :key="i" class="wave-bar" :style="{ animationDelay: `${(i - 1) * 0.1}s` }"></div>
  </div>
</template>

<script setup>
defineProps({
  bars: { type: Number, default: 10 }
})
</script>

<style scoped>
.wave-animation {
  height: 72px;
  background: var(--gradient-card);
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 3px;
  position: relative;
  overflow: hidden;
}

.wave-animation::after {
  content: '';
  position: absolute;
  bottom: 0;
  left: 0;
  right: 0;
  height: 40px;
  background: linear-gradient(0deg, rgba(124, 58, 237, 0.08) 0%, transparent 100%);
}

.wave-bar {
  width: 3px;
  border-radius: 2px;
  background: var(--color-primary-5);
  animation: waveAnim 1.2s ease-in-out infinite;
}

.wave-bar:nth-child(1) { height: 30%; }
.wave-bar:nth-child(2) { height: 60%; }
.wave-bar:nth-child(3) { height: 85%; }
.wave-bar:nth-child(4) { height: 45%; }
.wave-bar:nth-child(5) { height: 70%; }
.wave-bar:nth-child(6) { height: 55%; }
.wave-bar:nth-child(7) { height: 90%; }
.wave-bar:nth-child(8) { height: 40%; }
.wave-bar:nth-child(9) { height: 65%; }
.wave-bar:nth-child(10) { height: 50%; }
.wave-bar:nth-child(11) { height: 75%; }
.wave-bar:nth-child(12) { height: 35%; }
.wave-bar:nth-child(13) { height: 80%; }
.wave-bar:nth-child(14) { height: 50%; }
.wave-bar:nth-child(15) { height: 60%; }
.wave-bar:nth-child(16) { height: 45%; }

@keyframes waveAnim {
  0%, 100% { transform: scaleY(1); }
  50% { transform: scaleY(0.4); }
}
</style>
