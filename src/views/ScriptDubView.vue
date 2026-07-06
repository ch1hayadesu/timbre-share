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

      <BaseButton type="primary" size="lg" :loading="loading" :disabled="!hasScriptFile" @click="startDub">开始智能配音</BaseButton>
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
  </div>
</template>

<script setup>
import { ref } from 'vue'
import Card from '@/components/Card.vue'
import BaseButton from '@/components/BaseButton.vue'
import BaseTag from '@/components/BaseTag.vue'
import UploadZone from '@/components/UploadZone.vue'
import StepIndicator from '@/components/StepIndicator.vue'
import ProgressBar from '@/components/ProgressBar.vue'
import AiLoading from '@/components/AiLoading.vue'
import AudioPlayer from '@/components/AudioPlayer.vue'
import { createScriptDubTask, getScriptDubDetail } from '@/services'
import { useToast } from '@/composables/useToast'

const { showToast } = useToast()

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
let scriptText = ''

function triggerScriptUpload() { scriptInput.value?.click() }

function onScriptSelect(e) {
  const file = e.target.files?.[0]
  if (!file) return
  hasScriptFile.value = true
  const reader = new FileReader()
  reader.onload = () => { scriptText = reader.result }
  reader.readAsText(file)
}

async function startDub() {
  if (!scriptText.trim()) { showToast('warning', '请选择有效的剧本文件'); return }

  loading.value = true
  phase.value = 'processing'
  scriptCurrent.value = 0
  scriptProgress.value = 0

  try {
    const task = await createScriptDubTask({ script_text: scriptText })
    const result = await pollTaskResult(task.task_id)
    renderResult(result)
  } catch (err) {
    showToast('error', '配音失败：' + err.message)
    phase.value = 'upload'
  } finally {
    loading.value = false
  }
}

async function pollTaskResult(taskId, maxWait = 300) {
  for (let i = 0; i < maxWait; i++) {
    const step = Math.min(Math.floor(i / 75), 3)
    scriptCurrent.value = step
    scriptProgress.value = Math.min((i / maxWait) * 100, 95)
    scriptStatusText.value = scriptSteps[step]

    await new Promise(r => setTimeout(r, 1000))
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
  showToast('success', '剧本配音生成完成！')
}

const emotionLabels = { joy: '喜悦', anger: '愤怒', sad: '悲伤', fear: '恐惧', disgust: '厌恶', neutral: '中性' }

function resetDub() {
  phase.value = 'upload'
  hasScriptFile.value = false
  scriptText = ''
  roles.value = []
  audioUrl.value = ''
  if (scriptInput.value) scriptInput.value.value = ''
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
</style>
