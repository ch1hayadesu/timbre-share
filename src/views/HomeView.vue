<template>
  <div>
    <div class="page-header">
      <h1 class="page-title">工作台</h1>
      <p class="page-desc">欢迎回来！以下是你的音色创作概览。</p>
    </div>

    <div class="stat-grid">
      <div v-for="s in statCards" :key="s.label" class="stat-card" :style="{ background: s.bg }">
        <div class="stat-card-header">
          <div class="stat-card-icon">{{ s.icon }}</div>
        </div>
        <div class="stat-card-value">{{ s.value }}</div>
        <div class="stat-card-label">{{ s.label }}</div>
      </div>
    </div>

    <div class="section-title">快捷操作</div>
    <div class="quick-grid">
      <div v-for="a in actionCards" :key="a.label" class="quick-card" :style="{ background: a.bg }" @click="$router.push(a.path)">
        <div class="quick-card-layer"></div>
        <div class="quick-card-label">{{ a.label }}</div>
        <div class="quick-card-desc">{{ a.desc }}</div>
      </div>
    </div>

    <div class="section-title">
      最近音色
      <span class="section-title-link" @click="$router.push('/voices')">查看全部 →</span>
    </div>
    <div class="voice-grid">
      <VoiceCard v-for="voice in recentVoices" :key="voice.id" :voice="voice" :show-actions="false" />
    </div>

    <div class="section-title" style="margin-top:32px;">克隆历史</div>
    <Card style="padding:0;overflow:hidden;">
      <table class="synthesis-table" v-if="cloneHistory.items.length">
        <thead>
          <tr>
            <th>音色名称</th>
            <th>克隆模式</th>
            <th>状态</th>
            <th>时间</th>
            <th>操作</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="item in cloneHistory.items" :key="item.id">
            <td>{{ item.name }}</td>
            <td>{{ item.mode }}</td>
            <td>
              <StatusBadge :type="item.status === 'ready' ? 'ready' : 'failed'">
                {{ item.status === 'ready' ? '就绪' : '失败' }}
              </StatusBadge>
            </td>
            <td class="param-cell">{{ item.date }}</td>
            <td class="action-cell">
              <BaseButton v-if="item.status === 'ready'" type="default" size="sm" @click="downloadModel(item)">
                <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M21 15v4a2 2 0 01-2 2H5a2 2 0 01-2-2v-4"/><polyline points="7 10 12 15 17 10"/><line x1="12" y1="15" x2="12" y2="3"/></svg>
                下载模型
              </BaseButton>
              <BaseButton type="default" size="sm" @click="previewVoice(item)">
                <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><polygon points="5 3 19 12 5 21 5 3"/></svg>
                试听
              </BaseButton>
            </td>
          </tr>
        </tbody>
      </table>
      <div v-else style="padding:32px;text-align:center;color:var(--color-text-disabled);">暂无克隆记录，<a href="/clone" style="color:var(--color-primary-6);">去克隆音色 →</a></div>
    </Card>

    <div class="section-title" style="margin-top:32px;">最近合成记录</div>
    <Card style="padding:0;overflow:hidden;">
      <table class="synthesis-table">
        <thead>
          <tr>
            <th>文本内容</th>
            <th>使用音色</th>
            <th>参数</th>
            <th>状态</th>
            <th>时间</th>
            <th>操作</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="item in synthesisList.items" :key="item.id">
            <td class="text-cell">{{ item.text }}</td>
            <td>{{ item.voice }}</td>
            <td class="param-cell">{{ item.params }}</td>
            <td>
              <StatusBadge :type="item.status === 'success' ? 'ready' : 'failed'">
                {{ item.status === 'success' ? '成功' : '失败' }}
              </StatusBadge>
            </td>
            <td class="param-cell">{{ item.date }}</td>
            <td class="action-cell">
              <template v-if="item.status === 'success'">
                <BaseButton type="default" size="sm" @click="playAudio(item.audio_url)">
                  <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><polygon points="5 3 19 12 5 21 5 3"/></svg>
                  播放
                </BaseButton>
                <BaseButton type="default" size="sm" @click="$router.push('/tts')">
                  <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M21 15v4a2 2 0 01-2 2H5a2 2 0 01-2-2v-4"/><polyline points="7 10 12 15 17 10"/><line x1="12" y1="15" x2="12" y2="3"/></svg>
                  下载
                </BaseButton>
              </template>
              <BaseButton v-else type="default" size="sm" @click="$router.push('/tts')">
                <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><polyline points="1 4 1 10 7 10"/><polyline points="23 20 23 14 17 14"/><path d="M20.49 9A9 9 0 005.64 5.64L1 10m22 4l-4.64 4.36A9 9 0 013.51 15"/></svg>
                重新生成
              </BaseButton>
            </td>
          </tr>
        </tbody>
      </table>
      <div v-if="!synthesisList.items.length" style="padding:32px;text-align:center;color:var(--color-text-disabled);">暂无合成记录，<a href="/tts" style="color:var(--color-primary-6);">去 TTS 合成 →</a></div>
    </Card>

    <div class="section-title" style="margin-top:32px;">剧本配音记录</div>
    <Card style="padding:0;overflow:hidden;">
      <table class="synthesis-table" v-if="scriptDubList.items.length">
        <thead>
          <tr>
            <th>剧本名称</th>
            <th>角色数</th>
            <th>状态</th>
            <th>时间</th>
            <th>操作</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="item in scriptDubList.items" :key="item.id">
            <td class="text-cell">{{ item.scriptName }}</td>
            <td>{{ item.roleCount }}个角色</td>
            <td>
              <StatusBadge :type="item.status === 'success' ? 'ready' : item.status === 'processing' ? 'processing' : 'failed'">
                {{ item.status === 'success' ? '成功' : item.status === 'processing' ? '处理中' : '失败' }}
              </StatusBadge>
            </td>
            <td class="param-cell">{{ item.date }}</td>
            <td class="action-cell">
              <template v-if="item.status === 'success'">
                <BaseButton type="default" size="sm" @click="playAudio(item.outputUrl)">
                  <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><polygon points="5 3 19 12 5 21 5 3"/></svg>
                  播放
                </BaseButton>
                <BaseButton type="default" size="sm" @click="$router.push('/script')">
                  <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M21 15v4a2 2 0 01-2 2H5a2 2 0 01-2-2v-4"/><polyline points="7 10 12 15 17 10"/><line x1="12" y1="15" x2="12" y2="3"/></svg>
                  下载
                </BaseButton>
              </template>
              <BaseButton v-else type="default" size="sm" @click="$router.push('/script')">
                <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><polyline points="1 4 1 10 7 10"/><polyline points="23 20 23 14 17 14"/><path d="M20.49 9A9 9 0 005.64 5.64L1 10m22 4l-4.64 4.36A9 9 0 013.51 15"/></svg>
                重新配音
              </BaseButton>
            </td>
          </tr>
        </tbody>
      </table>
      <div v-else style="padding:32px;text-align:center;color:var(--color-text-disabled);">暂无剧本配音记录，<a href="/script" style="color:var(--color-primary-6);">去剧本配音 →</a></div>
    </Card>
  </div>
</template>

<script setup>
import { ref, reactive, onMounted } from 'vue'
import Card from '@/components/Card.vue'
import BaseButton from '@/components/BaseButton.vue'
import StatusBadge from '@/components/StatusBadge.vue'
import VoiceCard from './VoiceCard.vue'
import { getVoiceList, getSynthesisList, getScriptDubList, getCloneHistory, downloadCloneHistoryModel, addCloneHistoryToMyVoices } from '@/services'
import { getStats } from '@/services/statsCounter'
import { useToast } from '@/composables/useToast'

const { showToast } = useToast()

const recentVoices = ref([])
const synthesisList = reactive({ items: [] })
const scriptDubList = reactive({ items: [] })
const cloneHistory = reactive({ items: [] })

async function loadData() {
  try {
    const [voiceResult, synthResult, dubResult, cloneResult] = await Promise.all([
      getVoiceList({ page: 1, pageSize: 4 }),
      getSynthesisList({ page: 1, pageSize: 5 }),
      getScriptDubList({ page: 1, pageSize: 5 }),
      getCloneHistory({ page: 1, pageSize: 5 }),
    ])
    recentVoices.value = voiceResult.items
    synthesisList.items = synthResult.items
    scriptDubList.items = dubResult.items
    cloneHistory.items = cloneResult.items
  } catch (err) {
    if (!err.message?.includes('401')) showToast('error', '加载工作台数据失败：' + err.message)
  }
}

async function downloadModel(voice) {
  try {
    showToast('info', '正在将音色添加到「我的音色」...')
    await addCloneHistoryToMyVoices(voice.historyId)
    showToast('success', '已添加到「我的音色」，正在下载模型文件...')
    await downloadCloneHistoryModel(voice.historyId)
  } catch (err) {
    showToast('error', '操作失败：' + (err.message || '未知错误'))
  }
}

function playAudio(url) {
  if (!url) {
    showToast('warning', '该记录暂无音频文件')
    return
  }
  const audio = new Audio('/audio/' + url.replace(/^\//, ''))
  audio.play().catch(() => {
    showToast('error', '音频加载失败')
  })
}

function previewVoice(voice) {
  playAudio(voice.sample_url)
}

onMounted(() => loadData())

const stats = getStats()

const statCards = [
  {
    label: '我的音色', value: String(stats.voiceCount),
    icon: '🎤',
    bg: 'linear-gradient(135deg, #f5f0ff 0%, #ede5ff 100%)'
  },
  {
    label: '合成次数', value: String(stats.synthesisCount),
    icon: '🔊',
    bg: 'linear-gradient(135deg, #e8faf0 0%, #d4f5e3 100%)'
  },
  {
    label: '剧本配音', value: String(stats.scriptCount),
    icon: '🎬',
    bg: 'linear-gradient(135deg, #e8f0fe 0%, #d4e3fd 100%)'
  },
  {
    label: '下载音色', value: String(stats.downloadCount),
    icon: '📥',
    bg: 'linear-gradient(135deg, #fef3e8 0%, #fde8d4 100%)'
  },
]

const actionCards = [
  {
    label: '音色克隆', desc: '上传音频，AI生成专属音色',
    path: '/clone',
    bg: 'url(/quick-bg/mic.svg) center/cover no-repeat'
  },
  {
    label: 'TTS 合成', desc: '文本转语音，一键生成MP3',
    path: '/tts',
    bg: 'url(/quick-bg/gramophone.svg) center/cover no-repeat'
  },
  {
    label: '剧本配音', desc: '上传剧本，AI智能多人配音',
    path: '/script',
    bg: 'url(/quick-bg/stage.svg) center/cover no-repeat'
  },
  {
    label: '音色市场', desc: '探索社区共享的优质音色',
    path: '/market',
    bg: 'url(/quick-bg/music-store.svg) center/cover no-repeat'
  },
]
</script>

<style scoped>
.stat-grid {
  display: grid;
  grid-template-columns: repeat(4, 1fr);
  gap: 20px;
  margin-bottom: 36px;
}
.stat-card {
  border-radius: 16px;
  padding: 24px;
  position: relative;
  overflow: hidden;
  transition: transform 0.2s;
}
.stat-card:hover { transform: translateY(-2px); }
.stat-card-header {
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
  margin-bottom: 16px;
}
.stat-card-icon { font-size: 28px; line-height: 1; }
.stat-card-value {
  font-size: 36px;
  font-weight: 800;
  color: #1a1a2e;
  line-height: 1.1;
  margin-bottom: 4px;
}
.stat-card-label {
  font-size: 14px;
  color: #666;
  font-weight: 500;
}
.section-title {
  font-size: 18px;
  font-weight: 700;
  color: #1a1a2e;
  margin-bottom: 16px;
  display: flex;
  align-items: center;
  justify-content: space-between;
}
.section-title-link {
  font-size: 13px;
  font-weight: 500;
  color: #667eea;
  cursor: pointer;
}
.section-title-link:hover { text-decoration: underline; }

.quick-grid {
  display: grid;
  grid-template-columns: repeat(4, 1fr);
  gap: 20px;
  margin-bottom: 36px;
}
.quick-card {
  border-radius: 16px;
  padding: 28px 24px;
  position: relative;
  cursor: pointer;
  overflow: hidden;
  transition: transform 0.2s, box-shadow 0.2s;
  min-height: 140px;
  display: flex;
  flex-direction: column;
  justify-content: flex-end;
}
.quick-card:hover {
  transform: translateY(-4px);
  box-shadow: 0 12px 32px rgba(0,0,0,0.2);
}
.quick-card-layer {
  position: absolute;
  inset: 0;
  background: linear-gradient(to top, rgba(0,0,0,0.55) 0%, rgba(0,0,0,0.15) 50%, rgba(0,0,0,0.35) 100%);
  transition: background 0.2s;
}
.quick-card:hover .quick-card-layer { background: linear-gradient(to top, rgba(0,0,0,0.45) 0%, rgba(0,0,0,0.1) 50%, rgba(0,0,0,0.25) 100%); }
.quick-card-label {
  position: relative;
  z-index: 1;
  font-size: 18px;
  font-weight: 700;
  color: white;
  margin-bottom: 4px;
}
.quick-card-desc {
  position: relative;
  z-index: 1;
  font-size: 13px;
  color: rgba(255,255,255,0.8);
}

.voice-grid {
  display: grid;
  grid-template-columns: repeat(4, 1fr);
  gap: 16px;
  margin-bottom: 32px;
}

.synthesis-table {
  width: 100%;
  border-collapse: collapse;
}
.synthesis-table th {
  height: 48px;
  padding: 0 var(--space-4);
  text-align: left;
  font-size: var(--font-size-sm);
  font-weight: 500;
  color: var(--color-text-secondary);
  background: var(--color-bg-section);
  border-bottom: 1px solid var(--color-border-light);
}
.synthesis-table td {
  height: 48px;
  padding: 0 var(--space-4);
  font-size: var(--font-size-base);
  color: var(--color-text-body);
  border-bottom: 1px solid var(--color-border-light);
}
.synthesis-table tr:hover td {
  background: var(--color-bg-hover);
}
.text-cell {
  max-width: 200px;
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
}
.param-cell {
  font-size: var(--font-size-xs);
  color: var(--color-text-secondary);
}

.action-cell {
  display: flex;
  gap: 6px;
  align-items: center;
  height: 48px;
}
</style>
