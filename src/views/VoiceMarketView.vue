<template>
  <div>
    <div class="page-header">
      <h1 class="page-title">音色市场</h1>
      <p class="page-desc">探索社区分享的优质音色，下载到你的语音库即可使用</p>
    </div>

    <div class="search-bar">
      <div class="search-input-wrap">
        <svg class="search-icon" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
          <circle cx="11" cy="11" r="8" /><line x1="21" y1="21" x2="16.65" y2="16.65" />
        </svg>
        <input type="text" class="search-input" placeholder="搜索共享音色..." v-model="filter">
      </div>
      <select class="base-select" v-model="sort">
        <option value="newest">最新发布</option>
        <option value="popular">最多下载</option>
      </select>
    </div>

    <div class="market-grid">
      <div v-for="voice in filteredVoices" :key="voice.id" class="market-card card-clickable" @click="openDetail(voice)">
        <WaveAnimation />
        <div class="market-card-body">
          <div class="market-card-name">{{ voice.name }}</div>
          <div class="market-card-author">分享者：{{ voice.author }}</div>
          <div class="market-card-stats">
            <span class="stat">⬇ {{ voice.downloads }} 次下载</span>
            <span class="stat">📅 {{ voice.date }}</span>
          </div>
          <div class="market-card-actions">
            <BaseButton size="sm" @click.stop="showToast('info','试听功能演示中')">▶ 试听</BaseButton>
            <BaseButton type="primary" size="sm" @click.stop="download(voice)">下载</BaseButton>
          </div>
        </div>
      </div>
    </div>

    <div class="pagination">
      <BaseButton size="sm" disabled>上一页</BaseButton>
      <span class="page-info">第 1 页 / 共 1 页</span>
      <BaseButton size="sm" disabled>下一页</BaseButton>
    </div>
  </div>
</template>

<script setup>
import { ref, computed } from 'vue'
import BaseButton from '@/components/BaseButton.vue'
import WaveAnimation from '@/components/WaveAnimation.vue'
import { mockMarketVoices, mockVoices } from '@/data/mock'
import { useModal } from '@/composables/useModal'
import { useToast } from '@/composables/useToast'

const { showModal } = useModal()
const { showToast } = useToast()

const filter = ref('')
const sort = ref('newest')

const filteredVoices = computed(() => {
  let voices = [...mockMarketVoices]
  if (filter.value) voices = voices.filter(v => v.name.includes(filter.value))
  if (sort.value === 'popular') voices.sort((a, b) => b.downloads - a.downloads)
  return voices
})

function openDetail(voice) {
  const content = `
    <div style="text-align:center;margin-bottom:20px;">
      <div style="width:100%;height:80px;background:var(--gradient-card);border-radius:var(--radius-lg);display:flex;align-items:center;justify-content:center;gap:3px;margin-bottom:16px;overflow:hidden;">
        ${Array.from({ length: 16 }, () => '<div style="width:3px;border-radius:2px;background:var(--color-primary-5);animation:waveAnim 1.2s ease-in-out infinite;"></div>').join('')}
      </div>
      <p style="font-size:13px;color:var(--color-text-secondary);">分享者：${voice.author} · 下载 ${voice.downloads} 次 · ${voice.date}</p>
    </div>
    <div style="background:var(--color-bg-section);border-radius:var(--radius-lg);padding:16px;margin-bottom:16px;">
      <div style="display:flex;align-items:center;gap:10px;margin-bottom:12px;">
        <span style="font-weight:600;font-size:14px;">🎵 试听样本</span>
      </div>
      <div style="height:4px;border-radius:2px;background:var(--color-border-default);margin-bottom:12px;">
        <div style="height:100%;border-radius:2px;background:var(--gradient-audio);width:40%;"></div>
      </div>
      <div style="display:flex;align-items:center;gap:12px;">
        <button style="width:40px;height:40px;border-radius:50%;background:var(--color-primary-6);color:white;border:none;cursor:pointer;">▶</button>
      </div>
    </div>
    <p style="font-size:13px;color:var(--color-text-secondary);">下载后该音色将添加到你的语音库，可用于TTS合成和剧本配音。</p>
  `
  showModal(voice.name, content, () => download(voice), '下载到我的语音库')
}

function download(voice) {
  showToast('info', `正在下载「${voice.name}」...`)
  setTimeout(() => {
    mockVoices.push({
      id: mockVoices.length + 1,
      name: voice.name,
      source: 'shared',
      status: 'ready',
      mode: '下载',
      date: new Date().toISOString().split('T')[0],
      downloads: 0
    })
    showToast('success', `「${voice.name}」已下载到你的语音库！`)
  }, 1500)
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

.market-card {
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

.market-card-body { padding: var(--space-4); }

.market-card-name {
  font-size: 15px;
  font-weight: 600;
  color: var(--color-text-primary);
  margin-bottom: 4px;
}

.market-card-author {
  font-size: var(--font-size-xs);
  color: var(--color-text-secondary);
  margin-bottom: var(--space-2);
}

.market-card-stats {
  display: flex;
  align-items: center;
  gap: var(--space-4);
  margin-bottom: var(--space-3);
}

.stat {
  font-size: var(--font-size-xs);
  color: var(--color-text-secondary);
  display: flex;
  align-items: center;
  gap: 4px;
}

.market-card-actions {
  display: flex;
  gap: var(--space-2);
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
