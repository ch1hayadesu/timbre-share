<template>
  <div class="audio-player">
    <div class="audio-player-header">
      <span class="audio-player-title">{{ title }}</span>
      <span class="audio-player-time">{{ currentTime }} / {{ duration }}</span>
    </div>
    <div class="audio-progress">
      <div class="audio-progress-fill" :style="{ width: progress + '%' }"></div>
    </div>
    <div class="audio-controls">
      <button class="audio-btn audio-btn-play">▶</button>
      <span class="audio-info">{{ info }}</span>
      <slot name="actions" />
    </div>
  </div>
</template>

<script setup>
defineProps({
  title: { type: String, default: '🎵 音频播放器' },
  currentTime: { type: String, default: '0:00' },
  duration: { type: String, default: '0:30' },
  progress: { type: Number, default: 0 },
  info: { type: String, default: '点击播放试听' },
})
</script>

<style scoped>
.audio-player {
  background: var(--color-bg-section);
  border-radius: var(--radius-lg);
  padding: var(--space-4);
}

.audio-player-header {
  display: flex;
  align-items: center;
  gap: 10px;
  margin-bottom: var(--space-3);
}

.audio-player-title {
  font-size: var(--font-size-base);
  font-weight: 600;
  color: var(--color-text-primary);
}

.audio-player-time {
  font-size: var(--font-size-xs);
  color: var(--color-text-secondary);
  margin-left: auto;
}

.audio-progress {
  height: 4px;
  border-radius: 2px;
  background: var(--color-border-default);
  cursor: pointer;
  margin-bottom: var(--space-3);
  position: relative;
}

.audio-progress-fill {
  height: 100%;
  border-radius: 2px;
  background: var(--gradient-audio);
  width: 35%;
  transition: width 0.3s;
}

.audio-controls {
  display: flex;
  align-items: center;
  gap: var(--space-3);
}

.audio-btn {
  width: 36px;
  height: 36px;
  border-radius: 50%;
  border: none;
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: center;
  transition: all var(--duration-fast);
}

.audio-btn-play {
  background: var(--color-primary-6);
  color: white;
  width: 40px;
  height: 40px;
}

.audio-btn-play:hover {
  background: var(--color-primary-7);
}

.audio-info {
  font-size: var(--font-size-sm);
  color: var(--color-text-secondary);
}
</style>
