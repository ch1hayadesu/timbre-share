<template>
  <div>
    <div class="voice-card card-clickable" @click="$emit('detail', voice.id)">
      <WaveAnimation />
      <div class="voice-card-body">
        <div class="voice-card-name">{{ voice.name }}</div>
        <div class="voice-card-meta">
          <BaseTag type="primary">{{ sourceMap[voice.source] }}</BaseTag>
          <StatusBadge :type="voice.status">{{ statusMap[voice.status] }}</StatusBadge>
          <span class="voice-card-mode">{{ voice.mode }}</span>
        </div>
        <div class="voice-card-date">{{ voice.date }}</div>
        <div v-if="showActions" class="voice-card-actions">
          <BaseButton size="sm" @click.stop="onAction('preview')">▶ 试听</BaseButton>
          <BaseButton v-if="voice.status === 'ready'" type="text" size="sm" @click.stop="onAction('share')">分享</BaseButton>
          <BaseButton type="text" size="sm" style="color:var(--color-error)" @click.stop="onAction('delete')">删除</BaseButton>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import WaveAnimation from '@/components/WaveAnimation.vue'
import BaseTag from '@/components/BaseTag.vue'
import StatusBadge from '@/components/StatusBadge.vue'
import BaseButton from '@/components/BaseButton.vue'
import { statusMap, sourceMap } from '@/data/mock'

const props = defineProps({
  voice: { type: Object, required: true },
  showActions: { type: Boolean, default: true },
})

const emit = defineEmits(['detail', 'action'])

function onAction(type) {
  emit('action', { type, voice: props.voice })
}
</script>

<style scoped>
.voice-card {
  overflow: hidden;
  padding: 0;
  background: var(--color-bg-container);
  border-radius: var(--radius-lg);
  border: 1px solid var(--color-border-light);
  box-shadow: var(--shadow-md);
  transition: all var(--duration-base) var(--ease-out);
}

.card-clickable { cursor: pointer; }
.card-clickable:hover { box-shadow: var(--shadow-lg); transform: translateY(-2px); }

.voice-card-body { padding: var(--space-4); }

.voice-card-name {
  font-size: 15px;
  font-weight: 600;
  color: var(--color-text-primary);
  margin-bottom: 6px;
}

.voice-card-meta {
  display: flex;
  align-items: center;
  gap: var(--space-2);
  margin-bottom: var(--space-3);
  flex-wrap: wrap;
}

.voice-card-mode {
  font-size: var(--font-size-xs);
  color: var(--color-text-secondary);
}

.voice-card-date {
  font-size: var(--font-size-xs);
  color: var(--color-text-secondary);
  margin-bottom: var(--space-3);
}

.voice-card-actions {
  display: flex;
  align-items: center;
  gap: var(--space-2);
}
</style>
