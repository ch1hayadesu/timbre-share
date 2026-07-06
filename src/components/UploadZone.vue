<template>
  <div class="upload-zone" :class="{ 'has-file': hasFile }" @click="$emit('click')">
    <div class="upload-icon">{{ hasFile ? '🎵' : icon }}</div>
    <div class="upload-text">{{ hasFile ? '点击重新选择文件' : text }}</div>
    <div class="upload-hint">{{ hint }}</div>
  </div>
</template>

<script setup>
defineProps({
  hasFile: { type: Boolean, default: false },
  icon: { type: String, default: '🎤' },
  text: { type: String, default: '点击或拖拽音频文件到此处上传' },
  hint: { type: String, default: '支持 MP3、WAV、M4A、OGG 格式，文件大小不超过 50MB' },
})

defineEmits(['click'])
</script>

<style scoped>
.upload-zone {
  border: 2px dashed var(--color-border-default);
  border-radius: var(--radius-lg);
  padding: var(--space-12) var(--space-6);
  text-align: center;
  cursor: pointer;
  background: var(--color-bg-section);
  transition: all var(--duration-base) var(--ease-out);
}

.upload-zone:hover {
  border-color: var(--color-primary-5);
  background: var(--color-bg-selected);
}

.upload-zone.has-file {
  border-style: solid;
  border-color: var(--color-success);
  background: #ECFDF5;
}

.upload-icon {
  font-size: 48px;
  margin-bottom: var(--space-4);
  color: var(--color-text-disabled);
}

.upload-text {
  font-size: var(--font-size-base);
  color: var(--color-text-body);
  margin-bottom: var(--space-1);
}

.upload-hint {
  font-size: var(--font-size-xs);
  color: var(--color-text-secondary);
}
</style>
