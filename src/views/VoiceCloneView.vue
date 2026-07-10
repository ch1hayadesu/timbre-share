<template>
  <div>
    <div class="page-header">
      <h1 class="page-title">音色克隆</h1>
      <p class="page-desc">上传音频样本，AI将为你生成专属音色模型</p>
    </div>

    <StepIndicator :steps="stepLabels" :current="currentStep" />

    <!-- Step 1: Upload -->
    <Card v-show="phase === 'upload'">
      <div class="form-group">
        <label>合成模型</label>
        <select class="base-select wide" v-model="selectedModel">
          <option v-for="m in availableModels" :key="m.name" :value="m.name">
            {{ m.display_name }}
          </option>
        </select>
        <p v-if="modelNotice" class="form-notice">{{ modelNotice }}</p>
      </div>

      <div style="margin-bottom:20px;">
        <label style="font-size:14px;font-weight:500;display:block;margin-bottom:8px;">克隆模式</label>
        <div style="display:flex;gap:16px;">
          <label style="display:flex;align-items:center;gap:6px;cursor:pointer;">
            <input type="radio" name="clone_mode" value="instant" v-model="cloneMode" />
            <span>即时克隆（快速生成）</span>
          </label>
          <label style="display:flex;align-items:center;gap:6px;cursor:pointer;">
            <input type="radio" name="clone_mode" value="deep" v-model="cloneMode" />
            <span>深度克隆（高质量）</span>
          </label>
        </div>
      </div>
      <UploadZone :has-file="hasFile" @click="triggerUpload" />
      <input ref="fileInput" type="file" accept="audio/*" style="display:none" @change="onFileSelect">
      <div v-if="hasFile" class="file-info">
        <div class="file-info-box">
          <span class="file-icon">🎵</span>
          <div class="file-detail">
            <div class="file-name">{{ selectedFile.name }}</div>
            <div class="file-meta">{{ (selectedFile.size / 1024 / 1024).toFixed(2) }} MB · {{ selectedFile.type }}</div>
          </div>
          <BaseTag type="success">已选择</BaseTag>
        </div>
      </div>
      <div style="margin-top:20px;text-align:right;">
        <BaseButton type="primary" size="lg" :disabled="!hasFile" @click="startClone">开始克隆</BaseButton>
      </div>
    </Card>

    <!-- Step 2-3: Processing -->
    <Card v-show="phase === 'processing'" style="text-align:center;padding:48px 24px;">
      <AiLoading :text="statusText" style="margin-bottom:20px;" />
      <ProgressBar :percent="progress" />
    </Card>

    <!-- Step 4: Result -->
    <Card v-show="phase === 'result'">
      <div class="result-success">
        <div class="result-icon" :class="{ 'result-fail': cloneFailed }">{{ cloneFailed ? '✕' : '✓' }}</div>
        <h3>{{ cloneFailed ? '克隆失败' : '克隆成功！' }}</h3>
        <p>{{ cloneFailed ? (errorMessage || '请重试或更换音频') : '音色模型已生成' }}</p>
      </div>
      <div v-if="!cloneFailed" class="result-form">
        <label>音色名称</label>
        <input type="text" class="base-input" v-model="cloneName">
        <div v-if="sampleUrl" style="margin-bottom:16px;">
          <audio :src="sampleUrl" controls style="width:100%;" />
        </div>
        <div class="btn-group">
          <BaseButton type="primary" @click="goToManage">查看音色管理</BaseButton>
          <BaseButton @click="resetClone">重新克隆</BaseButton>
        </div>
      </div>
      <div v-else style="text-align:center;margin-top:16px;">
        <BaseButton @click="resetClone">重新克隆</BaseButton>
      </div>
    </Card>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import Card from '@/components/Card.vue'
import BaseButton from '@/components/BaseButton.vue'
import BaseTag from '@/components/BaseTag.vue'
import UploadZone from '@/components/UploadZone.vue'
import StepIndicator from '@/components/StepIndicator.vue'
import ProgressBar from '@/components/ProgressBar.vue'
import AiLoading from '@/components/AiLoading.vue'
import { getTTSModels } from '@/services'
import { useToast } from '@/composables/useToast'

const router = useRouter()
const { showToast } = useToast()

const stepLabels = ['上传音频', '预处理', '克隆中', '完成']

const phase = ref('upload')
const currentStep = ref(0)
const hasFile = ref(false)
const selectedFile = ref(null)
const fileInput = ref(null)
const progress = ref(0)
const statusText = ref('')
const cloneName = ref('我的新音色')
const cloneMode = ref('instant')
const cloneFailed = ref(false)
const errorMessage = ref('')
const sampleUrl = ref('')
const selectedModel = ref('edge-tts')
const availableModels = ref([])
const modelNotice = ref('')

let pollTimer = null
let safetyTimer = null

const modelNotices = {
  'edge-tts': '标准模型，稳定快速，支持多种语言。',
  'moss-tts': 'GPT模型，表现力更丰富。',
}

onMounted(async () => {
  try {
    const resp = await getTTSModels()
    availableModels.value = resp?.data || resp || []
    if (availableModels.value.length > 0) {
      selectedModel.value = availableModels.value[0].name
      modelNotice.value = modelNotices[selectedModel.value] || ''
    }
  } catch (err) {
    showToast('error', '加载模型列表失败：' + err.message)
  }
})

function onModelChange() {
  modelNotice.value = modelNotices[selectedModel.value] || ''
}

function triggerUpload() {
  fileInput.value?.click()
}

function onFileSelect(e) {
  if (e.target.files.length === 0) return
  selectedFile.value = e.target.files[0]
  hasFile.value = true
}

async function startClone() {
  cloneFailed.value = false
  errorMessage.value = ''
  sampleUrl.value = ''
  phase.value = 'processing'
  updateSteps(0)
  progress.value = 10
  statusText.value = '正在上传音频...'

  if (!selectedFile.value) {
    showToast('warning', '请先选择音频文件')
    return
  }

  try {
    const formData = new FormData()
    formData.append('file', selectedFile.value)
    formData.append('voice_name', cloneName.value)
    formData.append('clone_mode', cloneMode.value === 'deep' ? '1' : '0')
    formData.append('model', selectedModel.value)

    const resp = await fetch('/api/v1/voice/clone', {
      method: 'POST',
      headers: { 'Authorization': `Bearer ${localStorage.getItem('authToken') || '1'}` },
      body: formData,
    })
    if (!resp.ok) {
      const text = await resp.text()
      throw new Error(`服务器错误: ${text.substring(0, 100)}`)
    }
    const data = await resp.json()
    if (data.code !== 0) throw new Error(data.message)

    const voice = data.data
    const voiceId = voice.voice_id

    if (voice.status === 1) {
      progress.value = 100
      statusText.value = '克隆完成！'
      updateSteps(3)
      if (voice.sample_url) {
        sampleUrl.value = '/audio/' + voice.sample_url
      }
      setTimeout(() => {
        phase.value = 'result'
        showToast('success', '音色克隆成功！')
      }, 500)
      return
    }

    if (voice.status === -1) {
      progress.value = 100
      statusText.value = '克隆失败'
      cloneFailed.value = true
      errorMessage.value = voice.error_message || '未知错误'
      updateSteps(2)
      setTimeout(() => {
        phase.value = 'result'
        showToast('error', '音色克隆失败：' + (voice.error_message || '未知错误'))
      }, 500)
      return
    }

    progress.value = 30
    statusText.value = '克隆已提交，AI 正在处理...'
    updateSteps(1)
    showToast('info', '音色克隆任务已提交，后台处理中')

    pollTimer = setInterval(async () => {
      try {
        const detailResp = await fetch(`/api/v1/voice/detail/${voiceId}`, {
          headers: { 'Authorization': `Bearer ${localStorage.getItem('authToken') || '1'}` },
        })
        const detail = await detailResp.json()
        if (detail.code !== 0) return
        const v = detail.data
        const st = v.status
        if (st === 1) {
          clearInterval(pollTimer)
          clearTimeout(safetyTimer)
          progress.value = 100
          statusText.value = '克隆完成！'
          updateSteps(3)
          if (v.sample_url) {
            sampleUrl.value = '/audio/' + v.sample_url
          }
          setTimeout(() => {
            phase.value = 'result'
            showToast('success', '音色克隆成功！')
          }, 500)
        } else if (st === -1) {
          clearInterval(pollTimer)
          clearTimeout(safetyTimer)
          progress.value = 100
          statusText.value = '克隆失败'
          cloneFailed.value = true
          errorMessage.value = v.error_message || '未知错误'
          updateSteps(2)
          setTimeout(() => {
            phase.value = 'result'
            showToast('error', '音色克隆失败：' + (v.error_message || '未知错误'))
          }, 500)
        } else {
          const pct = Math.min(30 + (pollCount || 0) * 5, 80)
          pollCount = (pollCount || 0) + 1
          progress.value = pct
          statusText.value = 'AI 正在处理音频...'
          updateSteps(1)
        }
      } catch (_) {}
    }, 3000)

    let pollCount = 0
    safetyTimer = setTimeout(() => {
      clearInterval(pollTimer)
      if (phase.value === 'processing') {
        statusText.value = '处理超时，请到音色管理查看状态'
        showToast('warning', '处理时间较长，请稍后到音色管理查看')
      }
    }, 300000)
  } catch (err) {
    progress.value = 0
    statusText.value = '提交失败：' + (err.message || '网络错误')
    showToast('error', '克隆提交失败：' + (err.message || '网络错误'))
    setTimeout(() => resetClone(), 2000)
  }
}

function updateSteps(step) {
  currentStep.value = step
}

function goToManage() {
  router.push('/voices')
}

function resetClone() {
  if (pollTimer) clearInterval(pollTimer)
  if (safetyTimer) clearTimeout(safetyTimer)
  phase.value = 'upload'
  currentStep.value = 0
  progress.value = 0
  hasFile.value = false
  selectedFile.value = null
  cloneFailed.value = false
  errorMessage.value = ''
  sampleUrl.value = ''
  if (fileInput.value) fileInput.value.value = ''
}
</script>

<style scoped>
.form-group {
  margin-bottom: 20px;
}
.form-group label {
  font-size: 14px;
  font-weight: 500;
  display: block;
  margin-bottom: 8px;
}
.form-notice {
  font-size: 12px;
  color: var(--color-text-secondary);
  margin-top: 4px;
}
.base-select.wide {
  width: 100%;
  height: 40px;
  padding: 0 12px;
  border: 1px solid var(--color-border-default);
  border-radius: 6px;
  font-size: 14px;
  background: white;
  outline: none;
}
.file-info { margin-top: var(--space-4); }

.file-info-box {
  display: flex;
  align-items: center;
  gap: var(--space-3);
  padding: var(--space-3);
  background: var(--color-bg-section);
  border-radius: var(--radius-md);
}

.file-icon { font-size: 24px; }
.file-detail { flex: 1; }

.file-name {
  font-size: var(--font-size-base);
  font-weight: 500;
}

.file-meta {
  font-size: var(--font-size-xs);
  color: var(--color-text-secondary);
}

.result-success {
  text-align: center;
  margin-bottom: var(--space-6);
}

.result-icon {
  font-size: 48px;
  color: var(--color-success);
  margin-bottom: var(--space-3);
}

.result-success h3 {
  font-size: var(--font-size-xl);
  color: var(--color-text-primary);
  margin-bottom: var(--space-2);
}

.result-success p {
  font-size: var(--font-size-base);
  color: var(--color-text-secondary);
}

.result-form {
  max-width: 400px;
  margin: 0 auto;
}

.result-form label {
  font-size: var(--font-size-sm);
  font-weight: 500;
  color: var(--color-text-body);
  display: block;
  margin-bottom: var(--space-2);
}

.base-input {
  height: 40px;
  padding: 0 var(--space-3);
  border: 1px solid var(--color-border-default);
  border-radius: var(--radius-md);
  font-size: var(--font-size-base);
  color: var(--color-text-body);
  background: white;
  outline: none;
  transition: all var(--duration-fast);
  width: 100%;
  margin-bottom: var(--space-4);
}

.base-input:focus {
  border-color: var(--color-primary-6);
  box-shadow: var(--shadow-focus);
}

.btn-group {
  display: flex;
  gap: var(--space-3);
  justify-content: center;
  margin-top: var(--space-5);
}
</style>
