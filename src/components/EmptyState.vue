<template>
  <div class="empty-state">
    <div class="empty-state-icon">{{ icon }}</div>
    <div class="empty-state-title">{{ title }}</div>
    <div class="empty-state-desc">{{ desc }}</div>
  </div>
</template>

<script setup>
defineProps({
  icon: { type: String, default: '🎤' },
  title: { type: String, default: '暂无数据' },
  desc: { type: String, default: '这里还没有内容，快来添加吧' },
})
</script>

<style scoped>
.empty-state {
  text-align: center;
  padding: 64px var(--space-6);
}

.empty-state-icon {
  font-size: 64px;
  margin-bottom: var(--space-4);
  opacity: 0.5;
}

.empty-state-title {
  font-size: var(--font-size-md);
  font-weight: 500;
  color: var(--color-text-body);
  margin-bottom: var(--space-2);
}

.empty-state-desc {
  font-size: var(--font-size-base);
  color: var(--color-text-secondary);
}
</style>
