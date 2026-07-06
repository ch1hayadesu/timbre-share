<template>
  <div>
    <div class="page-header">
      <h1 class="page-title">工作台</h1>
      <p class="page-desc">欢迎回来，小明！以下是你的音色创作概览。</p>
    </div>

    <!-- Stat Cards -->
    <div class="stat-grid">
      <Card v-for="stat in stats" :key="stat.label" class="stat-card">
        <div class="stat-card-icon" :class="stat.color">
          <span v-html="stat.icon"></span>
        </div>
        <div class="stat-card-label">{{ stat.label }}</div>
        <div class="stat-card-value">{{ stat.value }}</div>
        <div class="stat-card-change" :class="stat.changeType">{{ stat.change }}</div>
      </Card>
    </div>

    <!-- Quick Actions -->
    <div class="section-title">快捷操作</div>
    <div class="quick-grid">
      <Card v-for="action in quickActions" :key="action.label" clickable @click="$router.push(action.path)">
        <div class="quick-card-content">
          <div class="quick-card-icon" :class="action.color">
            <span v-html="action.icon"></span>
          </div>
          <div class="quick-card-title">{{ action.label }}</div>
          <div class="quick-card-desc">{{ action.desc }}</div>
        </div>
      </Card>
    </div>

    <!-- Recent Voices -->
    <div class="section-title">
      最近音色
      <span class="section-title-link" @click="$router.push('/voices')">查看全部 →</span>
    </div>
    <div class="voice-grid">
      <VoiceCard v-for="voice in recentVoices" :key="voice.id" :voice="voice" :show-actions="false" />
    </div>

    <!-- Recent Synthesis -->
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
            <td>
              <template v-if="item.status === 'success'">
                <BaseButton type="text" size="sm">▶ 播放</BaseButton>
                <BaseButton type="text" size="sm">⬇ 下载</BaseButton>
              </template>
              <BaseButton v-else type="text" size="sm">重新生成</BaseButton>
            </td>
          </tr>
        </tbody>
      </table>
    </Card>
  </div>
</template>

<script setup>
import { ref, reactive, onMounted } from 'vue'
import Card from '@/components/Card.vue'
import BaseButton from '@/components/BaseButton.vue'
import StatusBadge from '@/components/StatusBadge.vue'
import VoiceCard from './VoiceCard.vue'
import { getVoiceList, getSynthesisList, getDashboardStats } from '@/services'
import { useToast } from '@/composables/useToast'

const { showToast } = useToast()

const recentVoices = ref([])
const synthesisList = reactive({ items: [] })
const dashboardStats = ref({ voiceCount: 0, synthesisCount: 0, scriptCount: 0, downloadCount: 0 })

async function loadData() {
  try {
    const [voiceResult, synthResult, stats] = await Promise.all([
      getVoiceList({ page: 1, pageSize: 4 }),
      getSynthesisList({ page: 1, pageSize: 5 }),
      getDashboardStats(),
    ])
    recentVoices.value = voiceResult.items
    synthesisList.items = synthResult.items
    dashboardStats.value = stats
  } catch (err) {
    showToast('error', '加载工作台数据失败：' + err.message)
  }
}

onMounted(() => loadData())

const stats = computed(() => [
  {
    label: '我的音色', value: String(dashboardStats.value.voiceCount),
    icon: '<svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M9 18V5l12-2v13"/><circle cx="6" cy="18" r="3"/><circle cx="18" cy="16" r="3"/></svg>',
    color: 'purple', change: '↑ 较上月 +3', changeType: 'up'
  },
  {
    label: '合成次数', value: String(dashboardStats.value.synthesisCount),
    icon: '<svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><polygon points="11 5 6 9 2 9 2 15 6 15 11 19 11 5"/><path d="M15.54 8.46a5 5 0 0 1 0 7.07"/></svg>',
    color: 'green', change: '↑ 较上月 +12', changeType: 'up'
  },
  {
    label: '剧本配音', value: String(dashboardStats.value.scriptCount),
    icon: '<svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z"/><polyline points="14 2 14 8 20 8"/></svg>',
    color: 'blue', change: '↑ 较上月 +5', changeType: 'up'
  },
  {
    label: '下载音色', value: String(dashboardStats.value.downloadCount),
    icon: '<svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M21 15v4a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-4"/><polyline points="7 10 12 15 17 10"/><line x1="12" y1="15" x2="12" y2="3"/></svg>',
    color: 'amber', change: '↑ 较上月 +2', changeType: 'up'
  },
])

const quickActions = [
  {
    label: '克隆音色', desc: '上传音频，AI生成专属音色', path: '/clone',
    icon: '<svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M12 1a3 3 0 0 0-3 3v8a3 3 0 0 0 6 0V4a3 3 0 0 0-3-3z"/><path d="M19 10v2a7 7 0 0 1-14 0v-2"/></svg>',
    color: 'clone'
  },
  {
    label: 'TTS合成', desc: '文本转语音，一键生成MP3', path: '/tts',
    icon: '<svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><polygon points="11 5 6 9 2 9 2 15 6 15 11 19 11 5"/><path d="M19.07 4.93a10 10 0 0 1 0 14.14"/></svg>',
    color: 'tts'
  },
  {
    label: '剧本配音', desc: '上传剧本，AI智能多人配音', path: '/script',
    icon: '<svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z"/><polyline points="14 2 14 8 20 8"/></svg>',
    color: 'script'
  },
  {
    label: '音色市场', desc: '探索社区共享的优质音色', path: '/market',
    icon: '<svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><circle cx="9" cy="21" r="1"/><circle cx="20" cy="21" r="1"/><path d="M1 1h4l2.68 13.39a2 2 0 0 0 2 1.61h9.72a2 2 0 0 0 2-1.61L23 6H6"/></svg>',
    color: 'market'
  },
]
</script>

<style scoped>
.stat-card-icon {
  width: 40px;
  height: 40px;
  border-radius: var(--radius-md);
  display: flex;
  align-items: center;
  justify-content: center;
  margin-bottom: var(--space-3);
}

.stat-card-icon.purple { background: var(--color-bg-selected); color: var(--color-primary-6); }
.stat-card-icon.green { background: #ECFDF5; color: var(--color-success); }
.stat-card-icon.blue { background: #EFF6FF; color: var(--color-link); }
.stat-card-icon.amber { background: #FFFBEB; color: var(--color-warning); }

.stat-card-label {
  font-size: var(--font-size-sm);
  color: var(--color-text-secondary);
  margin-bottom: var(--space-2);
}

.stat-card-value {
  font-size: var(--font-size-3xl);
  font-weight: 700;
  color: var(--color-text-primary);
  line-height: 1.3;
}

.stat-card-change {
  font-size: var(--font-size-xs);
  margin-top: var(--space-1);
  display: flex;
  align-items: center;
  gap: var(--space-1);
}

.stat-card-change.up { color: var(--color-success); }
.stat-card-change.down { color: var(--color-error); }

.quick-card-content {
  text-align: center;
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: var(--space-3);
}

.quick-card-icon {
  width: 56px;
  height: 56px;
  border-radius: var(--radius-lg);
  display: flex;
  align-items: center;
  justify-content: center;
}

.quick-card-icon.clone { background: var(--color-bg-selected); color: var(--color-primary-6); }
.quick-card-icon.tts { background: #EFF6FF; color: var(--color-link); }
.quick-card-icon.script { background: #ECFDF5; color: var(--color-success); }
.quick-card-icon.market { background: #FFFBEB; color: var(--color-warning); }

.quick-card-title {
  font-size: 15px;
  font-weight: 600;
  color: var(--color-text-primary);
}

.quick-card-desc {
  font-size: var(--font-size-xs);
  color: var(--color-text-secondary);
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
</style>
