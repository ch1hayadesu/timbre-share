<template>
  <div>
    <div class="page-header">
      <h1 class="page-title">剧本配音</h1>
      <p class="page-desc">上传剧本文件，AI自动识别角色、分析情感、匹配音色，一键生成多人配音</p>
    </div>

    <!-- Upload -->
    <Card v-if="phase === 'upload'">
      <h3 class="panel-title">📄 上传剧本文件</h3>
      <UploadZone :has-file="hasScriptFile" icon="📝" text="点击上传 TXT 格式剧本文件"
        hint="支持 UTF-8、GBK 编码，文件大小不超过 5MB" @click="triggerScriptUpload" style="margin-bottom:16px;" />
      <input ref="scriptInput" type="file" accept=".txt" style="display:none" @change="onScriptSelect">

      <div class="format-hint">
        <div class="format-title">📋 剧本格式示例：</div>
        <pre>角色A：你好，今天天气真好。
角色B：是啊，我们出去走走吧。
角色A：好的，我马上就来。
角色C：等等我！我也要去！</pre>
      </div>

      <BaseButton type="primary" size="lg" :disabled="!hasScriptFile" @click="parseRoles">下一步：配置音色</BaseButton>
    </Card>

    <!-- Voice & Emotion Mapping -->
    <Card v-if="phase === 'mapping'">
      <h3 class="panel-title">🎤 为每个角色选择音色与情感</h3>
      <p class="panel-desc">已识别到 {{ roleOptions.length }} 个角色，请为每个角色配置音色和朗读情感</p>
      <div class="voice-mapping-list">
        <div v-for="role in roleOptions" :key="role.name" class="voice-mapping-row">
          <span class="mapping-role">{{ role.name }}</span>
          <select class="base-select mapping-select" v-model="role.voiceId">
            <option v-for="v in ttsVoiceOptions" :key="v.value" :value="v.value">{{ v.label }}</option>
          </select>
          <select class="base-select mapping-select emotion-select" v-model="role.emotion">
            <option value="">默认</option>
            <option value="happy">快乐 😊</option>
            <option value="sad">悲伤 😢</option>
            <option value="angry">生气 😠</option>
            <option value="fear">恐惧 😨</option>
            <option value="surprise">惊讶 😲</option>
          </select>
        </div>
      </div>
      <BaseButton type="primary" size="lg" :loading="loading" @click="startDub">开始智能配音</BaseButton>
    </Card>

    <!-- Processing -->
    <Card v-if="phase === 'processing'" style="text-align:center;padding:48px 24px;">
      <StepIndicator :steps="scriptSteps" :current="scriptCurrent" style="margin-bottom:24px;" />
      <AiLoading :text="scriptStatusText" />
      <ProgressBar :percent="scriptProgress" style="margin-top:16px;" />
    </Card>

    <!-- Result -->
    <Card v-if="phase === 'result'">
      <div class="result-header">
        <h3>✓ 配音生成完成</h3>
        <BaseTag type="success">{{ roleCount }}个角色</BaseTag>
      </div>

      <AudioPlayer v-if="audioUrl" title="🎭 完整配音音频" :src="audioUrl" />

      <h3 class="panel-title" style="margin-top:20px;">角色·音色·情感对照表</h3>
      <table class="role-table">
        <thead>
          <tr><th>角色</th><th>台词数</th><th>情感</th></tr>
        </thead>
        <tbody>
          <tr v-for="role in roles" :key="role.name">
            <td class="role-name">{{ role.name }}</td>
            <td>{{ role.lines }}句</td>
            <td>
              <span v-for="e in role.emotions" :key="e.type" class="emotion-tag" :class="`emotion-${e.type}`">
                {{ e.label }}
              </span>
            </td>
          </tr>
        </tbody>
      </table>

      <div class="result-actions">
        <BaseButton @click="resetDub">上传新剧本</BaseButton>
      </div>
    </Card>

    <!-- 配音记录 -->
    <div class="section-title" style="margin-top:32px;">配音记录</div>
    <Card style="padding:0;overflow:hidden;">
      <table class="synthesis-table" v-if="dubHistory.items.length">
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
          <tr v-for="item in dubHistory.items" :key="item.id">
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
                <BaseButton type="default" size="sm" @click="playDubAudio(item)">
                  <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><polygon points="5 3 19 12 5 21 5 3"/></svg>
                  播放
                </BaseButton>
                <BaseButton type="default" size="sm" @click="downloadDubAudio(item)">
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
      <div v-else style="padding:32px;text-align:center;color:var(--color-text-disabled);">暂无配音记录</div>
    </Card>
  </div>
</template>

<script setup>
import { ref, reactive, onMounted } from 'vue'
import Card from '@/components/Card.vue'
import BaseButton from '@/components/BaseButton.vue'
import BaseTag from '@/components/BaseTag.vue'
import UploadZone from '@/components/UploadZone.vue'
import StepIndicator from '@/components/StepIndicator.vue'
import ProgressBar from '@/components/ProgressBar.vue'
import AiLoading from '@/components/AiLoading.vue'
import AudioPlayer from '@/components/AudioPlayer.vue'
import { createScriptDubTask, getScriptDubDetail, getScriptDubList, getTTSVoiceOptions } from '@/services'
import { useToast } from '@/composables/useToast'
import { useAuth } from '@/composables/useAuth'
import { incrementScriptCount } from '@/services/statsCounter'
import StatusBadge from '@/components/StatusBadge.vue'

const { showToast } = useToast()
const { requireAuth } = useAuth()

const phase = ref('upload')
const hasScriptFile = ref(false)
const loading = ref(false)
const scriptInput = ref(null)
const scriptSteps = ['角色分割', '情感分析', '音色匹配', '生成配音']
const scriptCurrent = ref(0)
const scriptProgress = ref(0)
const scriptStatusText = ref('AI 正在分割角色...')

const roles = ref([])
const roleCount = ref(0)
const audioUrl = ref('')
const roleOptions = ref([])
const ttsVoiceOptions = ref([])
const dubHistory = reactive({ items: [] })
const lineRoleRe = /^(.+?)[：:]/
let scriptText = ''

const FALLBACK_VOICES = [
  { value: 1, label: '标准女声' },
  { value: 2, label: '沉稳男声' },
  { value: 3, label: '活泼少女' },
  { value: 4, label: '磁性大叔' },
  { value: 5, label: '知性女声' },
  { value: 6, label: '新闻播音' },
  { value: 7, label: '动漫正太' },
]

onMounted(async () => {
  try { ttsVoiceOptions.value = await getTTSVoiceOptions() } catch (_) { /* guest mode: skip */ }
  if (!ttsVoiceOptions.value.length) ttsVoiceOptions.value = FALLBACK_VOICES
  loadDubHistory()
})

async function loadDubHistory() {
  try {
    const result = await getScriptDubList({ page: 1, pageSize: 10 })
    dubHistory.items = result.items
  } catch (_) { /* guest mode: skip */ }
}

function triggerScriptUpload() {
  if (!requireAuth(triggerScriptUpload)) return
  scriptInput.value?.click()
}

function onScriptSelect(e) {
  const file = e.target.files?.[0]
  if (!file) return
  hasScriptFile.value = true
  const reader = new FileReader()
  reader.onload = () => {
    try {
      const bytes = new Uint8Array(reader.result)
      const decoder = new TextDecoder('utf-8', { fatal: true })
      scriptText = decoder.decode(bytes)
    } catch (_) {
      const decoder = new TextDecoder('gbk', { fatal: false })
      scriptText = decoder.decode(new Uint8Array(reader.result))
    }
  }
  reader.readAsArrayBuffer(file)
}

function parseRoles() {
  if (!requireAuth(parseRoles)) return
  if (!scriptText.trim()) { showToast('warning', '请选择有效的剧本文件'); return }
  const names = new Set()
  for (const line of scriptText.split('\n')) {
    const m = line.match(lineRoleRe)
    if (m) names.add(m[1].trim())
  }
  if (names.size === 0) { showToast('warning', '未识别到角色，请检查剧本格式'); return }

  const opts = ttsVoiceOptions.value.length ? ttsVoiceOptions.value : FALLBACK_VOICES
  const usedVoices = new Set()
  roleOptions.value = Array.from(names).map((name, i) => {
    let v = opts[i % opts.length]
    let attempts = 0
    while (usedVoices.has(v.value) && attempts < opts.length) {
      attempts++; v = opts[(i + attempts) % opts.length]
    }
    usedVoices.add(v.value)
    return { name, voiceId: v.value, emotion: '' }
  })
  phase.value = 'mapping'
}

async function startDub() {
  if (!requireAuth(startDub)) return
  if (!scriptText.trim()) { showToast('warning', '请选择有效的剧本文件'); return }

  const voiceMapping = {}
  const emotionMapping = {}
  const used = new Set()
  for (const role of roleOptions.value) {
    if (used.has(role.voiceId)) { showToast('warning', `${role.name} 的音色与其他角色重复，请选择不同的音色`); return }
    used.add(role.voiceId)
    voiceMapping[role.name] = role.voiceId
    if (role.emotion) emotionMapping[role.name] = role.emotion
  }

  loading.value = true
  phase.value = 'processing'
  scriptCurrent.value = 0
  scriptProgress.value = 0

  try {
    const task = await createScriptDubTask({ script_text: scriptText, voice_mapping: voiceMapping, emotion_mapping: Object.keys(emotionMapping).length ? emotionMapping : undefined })
    const result = await pollTaskResult(task.task_id)
    renderResult(result)
  } catch (err) {
    showToast('error', '配音失败：' + err.message)
    phase.value = 'mapping'
  } finally {
    loading.value = false
  }
}

async function pollTaskResult(taskId, maxWait = 100) {
  for (let i = 0; i < maxWait; i++) {
    const step = Math.min(Math.floor(i / 25), 3)
    scriptCurrent.value = step
    scriptProgress.value = Math.min((i / maxWait) * 100, 95)
    scriptStatusText.value = scriptSteps[step]

    await new Promise(r => setTimeout(r, 3000))
    try {
      const result = await getScriptDubDetail(taskId)
      if (result.status === 1) {
        scriptProgress.value = 100
        scriptCurrent.value = 3
        scriptStatusText.value = '生成完毕'
        return result
      }
      if (result.status === -1) throw new Error(result.error_message || '配音任务失败')
    } catch (err) {
      if (err.message?.includes('任务未就绪') || err.message?.includes('404')) continue
      throw err
    }
  }
  throw new Error('配音任务超时，请稍后重试')
}

function renderResult(result) {
  const emotions = result.emotion_result || []
  const roleMap = {}
  for (const item of emotions) {
    if (!roleMap[item.role]) roleMap[item.role] = { name: item.role, lines: 0, emotions: {} }
    roleMap[item.role].lines++
    roleMap[item.role].emotions[item.emotion] = (roleMap[item.role].emotions[item.emotion] || 0) + 1
  }
  roles.value = Object.values(roleMap).map(r => ({
    name: r.name,
    lines: r.lines,
    emotions: Object.entries(r.emotions).map(([type, count]) => ({ type, label: emotionLabels[type] || type, count })),
  }))
  roleCount.value = roles.value.length
  audioUrl.value = result.output_url ? `/audio/${result.output_url}` : ''
  phase.value = 'result'
  incrementScriptCount()
  loadDubHistory()
  showToast('success', '剧本配音生成完成！')
}

const emotionLabels = { joy: '喜悦', anger: '愤怒', sad: '悲伤', fear: '恐惧', disgust: '厌恶', neutral: '中性' }

function resetDub() {
  phase.value = 'upload'
  hasScriptFile.value = false
  scriptText = ''
  roles.value = []
  audioUrl.value = ''
  roleOptions.value = []
  if (scriptInput.value) scriptInput.value.value = ''
}

function playDubAudio(item) {
  const url = item.outputUrl
  if (!url) {
    showToast('warning', '该记录暂无音频文件')
    return
  }
  const audio = new Audio('/audio/' + url.replace(/^\//, ''))
  audio.play().catch(() => {
    showToast('error', '音频加载失败')
  })
}

function downloadDubAudio(item) {
  const url = item.outputUrl
  if (!url) {
    showToast('warning', '该记录暂无音频文件')
    return
  }
  const fullUrl = '/audio/' + url.replace(/^\//, '')
  const a = document.createElement('a')
  a.href = fullUrl
  a.download = url.split('/').pop() || 'dub_output.mp3'
  document.body.appendChild(a)
  a.click()
  document.body.removeChild(a)
}
</script>

<style scoped>
.panel-title {
  font-size: var(--font-size-md);
  font-weight: 600;
  color: var(--color-text-primary);
  margin-bottom: var(--space-4);
}

.format-hint {
  background: var(--color-bg-section);
  border-radius: var(--radius-md);
  padding: var(--space-4);
  margin-bottom: var(--space-4);
}

.format-title {
  font-size: var(--font-size-sm);
  font-weight: 500;
  color: var(--color-text-body);
  margin-bottom: var(--space-2);
}

.format-hint pre {
  font-size: var(--font-size-xs);
  color: var(--color-text-secondary);
  line-height: 1.8;
  white-space: pre-wrap;
}

.result-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  margin-bottom: var(--space-5);
}

.result-header h3 {
  font-size: var(--font-size-lg);
  font-weight: 600;
  color: var(--color-text-primary);
}

.role-table {
  width: 100%;
  border-collapse: collapse;
  margin-top: var(--space-4);
}

.role-table th,
.role-table td {
  padding: 10px var(--space-3);
  font-size: var(--font-size-sm);
}

.role-table th {
  background: var(--color-bg-section);
  font-weight: 500;
  color: var(--color-text-secondary);
  text-align: left;
}

.role-table td {
  border-bottom: 1px solid var(--color-border-light);
}

.role-name { font-weight: 600; }

.emotion-tag {
  font-size: var(--font-size-xs);
  padding: 2px var(--space-2);
  border-radius: var(--radius-sm);
  margin-right: 4px;
}

.emotion-joy { background: #FEF3C7; color: #D97706; }
.emotion-anger { background: #FEE2E2; color: #DC2626; }
.emotion-sad { background: #DBEAFE; color: #2563EB; }
.emotion-fear { background: #F3E8FF; color: #7C3AED; }
.emotion-disgust { background: #D1FAE5; color: #059669; }
.emotion-neutral { background: var(--color-bg-section); color: var(--color-text-secondary); }

.result-actions {
  display: flex;
  gap: var(--space-3);
  justify-content: flex-end;
  margin-top: var(--space-5);
}

.panel-desc {
  font-size: 13px;
  color: var(--color-text-secondary);
  margin-bottom: var(--space-4);
}
.voice-mapping-list {
  display: flex;
  flex-direction: column;
  gap: var(--space-3);
  margin-bottom: var(--space-5);
}
.voice-mapping-row {
  display: flex;
  align-items: center;
  gap: var(--space-3);
  padding: var(--space-3);
  background: var(--color-bg-section);
  border-radius: var(--radius-md);
}
.mapping-role {
  font-weight: 600;
  min-width: 80px;
  font-size: var(--font-size-base);
}
.mapping-select { flex: 1; }

.section-title {
  font-size: 18px;
  font-weight: 700;
  color: #1a1a2e;
  margin-bottom: 16px;
  display: flex;
  align-items: center;
  justify-content: space-between;
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
