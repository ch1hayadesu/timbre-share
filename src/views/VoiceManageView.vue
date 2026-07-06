<template>
  <div>
    <div class="page-header">
      <h1 class="page-title">我的音色</h1>
      <p class="page-desc">管理你创建和下载的所有音色模型</p>
    </div>

    <div class="search-bar">
      <div class="search-input-wrap">
        <svg class="search-icon" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
          <circle cx="11" cy="11" r="8" /><line x1="21" y1="21" x2="16.65" y2="16.65" />
        </svg>
        <input type="text" class="search-input" placeholder="搜索音色名称..." v-model="filter" @input="applyFilters">
      </div>
      <select class="base-select" v-model="source" @change="applyFilters">
        <option value="all">全部来源</option>
        <option value="cloned">克隆</option>
        <option value="shared">下载</option>
        <option value="preset">预设</option>
      </select>
      <select class="base-select" v-model="status" @change="applyFilters">
        <option value="all">全部状态</option>
        <option value="ready">就绪</option>
        <option value="processing">处理中</option>
        <option value="failed">失败</option>
        <option value="shared">已分享</option>
      </select>
      <BaseButton type="primary" @click="$router.push('/clone')">+ 克隆新音色</BaseButton>
    </div>

    <div class="voice-grid">
      <template v-if="filteredVoices.length">
        <VoiceCard v-for="voice in filteredVoices" :key="voice.id" :voice="voice"
          @detail="openDetail" @action="handleAction" />
      </template>
      <EmptyState v-else icon="🎤" title="没有找到匹配的音色" desc="试试调整筛选条件或克隆新的音色"
        style="grid-column:1/-1;" />
    </div>

    <div class="pagination">
      <BaseButton size="sm" disabled>上一页</BaseButton>
      <span class="page-info">第 1 页 / 共 2 页</span>
      <BaseButton size="sm">下一页</BaseButton>
    </div>
  </div>
</template>

<script setup>
import { ref, computed } from 'vue'
import BaseButton from '@/components/BaseButton.vue'
import EmptyState from '@/components/EmptyState.vue'
import VoiceCard from './VoiceCard.vue'
import { mockVoices, statusMap, sourceMap } from '@/data/mock'
import { useModal } from '@/composables/useModal'
import { useDrawer } from '@/composables/useDrawer'
import { useToast } from '@/composables/useToast'

const { showModal } = useModal()
const { showDrawer } = useDrawer()
const { showToast } = useToast()

const filter = ref('')
const source = ref('all')
const status = ref('all')

const filteredVoices = computed(() => {
  let voices = mockVoices
  if (filter.value) voices = voices.filter(v => v.name.includes(filter.value))
  if (source.value !== 'all') voices = voices.filter(v => v.source === source.value)
  if (status.value !== 'all') voices = voices.filter(v => v.status === status.value)
  return voices
})

function applyFilters() { /* computed automatically tracks */ }

function openDetail(id) {
  const v = mockVoices.find(v => v.id === id)
  if (!v) return
  const content = `
    <div style="text-align:center;margin-bottom:24px;">
      <div style="height:100px;background:var(--gradient-card);border-radius:var(--radius-lg);margin-bottom:16px;display:flex;align-items:center;justify-content:center;gap:3px;overflow:hidden;">
        ${Array.from({ length: 16 }, () => '<div style="width:3px;border-radius:2px;background:var(--color-primary-5);animation:waveAnim 1.2s ease-in-out infinite;"></div>').join('')}
      </div>
      <h3 style="font-size:20px;color:var(--color-text-primary);margin-bottom:8px;">${v.name}</h3>
      <div style="display:flex;gap:8px;justify-content:center;margin-bottom:16px;">
        <span class="tag tag-primary">${sourceMap[v.source]}</span>
        <span class="status-badge ${v.status}">${statusMap[v.status]}</span>
        <span class="tag tag-default">${v.mode}</span>
      </div>
    </div>
    <div style="background:var(--color-bg-section);border-radius:var(--radius-lg);padding:16px;margin-bottom:20px;">
      <div style="display:flex;align-items:center;gap:10px;margin-bottom:12px;">
        <span style="font-weight:600;font-size:14px;">🎵 试听样本</span>
        <span style="font-size:12px;color:var(--color-text-secondary);margin-left:auto;">0:00 / 0:30</span>
      </div>
      <div style="height:4px;border-radius:2px;background:var(--color-border-default);margin-bottom:12px;">
        <div style="height:100%;border-radius:2px;background:var(--gradient-audio);width:60%;"></div>
      </div>
      <div style="display:flex;align-items:center;gap:12px;">
        <button style="width:40px;height:40px;border-radius:50%;background:var(--color-primary-6);color:white;border:none;cursor:pointer;">▶</button>
        <span style="font-size:13px;color:var(--color-text-secondary);">点击播放试听</span>
      </div>
    </div>
    <div style="background:var(--color-bg-section);border-radius:var(--radius-md);padding:16px;">
      <div style="font-size:13px;color:var(--color-text-secondary);margin-bottom:8px;">音色信息</div>
      <div style="display:grid;grid-template-columns:1fr 1fr;gap:12px;font-size:13px;">
        <div><span style="color:var(--color-text-secondary);">来源：</span>${sourceMap[v.source]}</div>
        <div><span style="color:var(--color-text-secondary);">模式：</span>${v.mode}</div>
        <div><span style="color:var(--color-text-secondary);">状态：</span>${statusMap[v.status]}</div>
        <div><span style="color:var(--color-text-secondary);">日期：</span>${v.date}</div>
        <div><span style="color:var(--color-text-secondary);">下载次数：</span>${v.downloads}</div>
      </div>
    </div>
  `
  showDrawer(v.name + ' - 音色详情', content)
}

function handleAction({ type, voice }) {
  if (type === 'preview') showToast('info', '试听功能演示中')
  else if (type === 'share') {
    showModal('分享音色到平台', '<p style="font-size:14px;">确定要将该音色分享到公共平台吗？分享后其他用户可下载使用。</p>', () => {
      voice.status = 'shared'
      showToast('success', '音色已成功分享到平台！')
    }, '确认分享')
  } else if (type === 'delete') {
    showModal('删除音色', '<p style="font-size:14px;color:var(--color-error);">此操作不可撤销，确定要删除该音色吗？</p>', () => {
      const idx = mockVoices.findIndex(v => v.id === voice.id)
      if (idx > -1) mockVoices.splice(idx, 1)
      showToast('success', '音色已删除')
    }, '确认删除', true)
  }
}
</script>

<style scoped>
.search-input-wrap {
  position: relative;
  flex: 1;
  min-width: 240px;
  max-width: 400px;
}

.search-icon {
  position: absolute;
  left: 12px;
  top: 50%;
  transform: translateY(-50%);
  color: var(--color-text-disabled);
}

.search-input {
  height: 40px;
  padding: 0 12px 0 36px;
  border: 1px solid var(--color-border-default);
  border-radius: var(--radius-md);
  font-size: var(--font-size-base);
  color: var(--color-text-body);
  background: white;
  outline: none;
  transition: all var(--duration-fast);
  width: 100%;
}

.search-input:focus {
  border-color: var(--color-primary-6);
  box-shadow: var(--shadow-focus);
}

.search-input::placeholder { color: var(--color-text-disabled); }

.base-select {
  height: 40px;
  padding: 0 32px 0 12px;
  border: 1px solid var(--color-border-default);
  border-radius: var(--radius-md);
  font-size: var(--font-size-base);
  color: var(--color-text-body);
  background: white;
  outline: none;
  cursor: pointer;
  appearance: none;
  background-image: url("data:image/svg+xml,%3Csvg width='12' height='12' viewBox='0 0 12 12' fill='none' xmlns='http://www.w3.org/2000/svg'%3E%3Cpath d='M3 4.5L6 7.5L9 4.5' stroke='%236B7280' stroke-width='1.5' stroke-linecap='round' stroke-linejoin='round'/%3E%3C/svg%3E");
  background-repeat: no-repeat;
  background-position: right 10px center;
}

.base-select:focus {
  border-color: var(--color-primary-6);
  box-shadow: var(--shadow-focus);
}

.pagination {
  text-align: center;
  margin-top: var(--space-6);
  display: flex;
  align-items: center;
  justify-content: center;
  gap: var(--space-3);
}

.page-info {
  padding: 0 var(--space-3);
  font-size: var(--font-size-sm);
  color: var(--color-text-secondary);
}
</style>
