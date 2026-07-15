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
        <div v-if="showActions" class="voice-card-actions" @click.stop>
          <BaseButton type="default" size="sm" @click="onAction('preview')">
            <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><polygon points="5 3 19 12 5 21 5 3"/></svg>
            试听
          </BaseButton>
          <BaseButton v-if="voice.status === 'ready' && voice.source === 'cloned'" type="default" size="sm" @click="onAction('download-model')">
            <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M21 15v4a2 2 0 01-2 2H5a2 2 0 01-2-2v-4"/><polyline points="7 10 12 15 17 10"/><line x1="12" y1="15" x2="12" y2="3"/></svg>
            下载模型
          </BaseButton>
          <BaseButton v-if="voice.status === 'ready'" type="default" size="sm" @click="onAction('share')">
            <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><circle cx="18" cy="5" r="3"/><circle cx="6" cy="12" r="3"/><circle cx="18" cy="19" r="3"/><line x1="8.59" y1="13.51" x2="15.42" y2="17.49"/><line x1="15.41" y1="6.51" x2="8.59" y2="10.49"/></svg>
            分享
          </BaseButton>
          <BaseButton type="text" size="sm" class="btn-delete" @click="onAction('delete')">
            <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><polyline points="3 6 5 6 21 6"/><path d="M19 6v14a2 2 0 01-2 2H7a2 2 0 01-2-2V6m3 0V4a2 2 0 012-2h4a2 2 0 012 2v2"/></svg>
            删除
          </BaseButton>
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
import { statusMap, sourceMap } from '@/services'

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
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
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
  gap: 6px;
  flex-wrap: wrap;
}

.btn-delete {
  color: var(--color-error) !important;
}

.btn-delete:hover {
  background: rgba(239, 68, 68, 0.08) !important;
  color: #DC2626 !important;
}
</style>
