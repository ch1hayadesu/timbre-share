<template>
  <div>
    <div class="page-header">
      <h1 class="page-title">音色克隆</h1>
      <p class="page-desc">上传音频样本，AI将为你生成专属音色模型</p>
    </div>

    <StepIndicator :steps="stepLabels" :current="currentStep" />

    <!-- Step 1: Upload -->
    <Card v-show="phase === 'upload'">
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
        <div class="result-icon">✓</div>
        <h3>克隆成功！</h3>
        <p>音色模型已生成，请为你的音色命名</p>
      </div>
      <div class="result-form">
        <label>音色名称</label>
        <input type="text" class="base-input" v-model="cloneName">
        <AudioPlayer title="🎵 试听样本" :current-time="'0:45'" :duration="'1:30'" :progress="50" />
        <div class="btn-group">
          <BaseButton type="primary" @click="saveResult">保存音色</BaseButton>
          <BaseButton @click="resetClone">重新克隆</BaseButton>
        </div>
      </div>
    </Card>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import Card from '@/components/Card.vue'
import BaseButton from '@/components/BaseButton.vue'
import BaseTag from '@/components/BaseTag.vue'
import UploadZone from '@/components/UploadZone.vue'
import StepIndicator from '@/components/StepIndicator.vue'
import ProgressBar from '@/components/ProgressBar.vue'
import AiLoading from '@/components/AiLoading.vue'
import AudioPlayer from '@/components/AudioPlayer.vue'
import { mockVoices } from '@/data/mock'
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
const statusText = ref('AI 正在预处理音频...')
const cloneName = ref('我的新音色')

function triggerUpload() {
  fileInput.value?.click()
}

function onFileSelect(e) {
  if (e.target.files.length === 0) return
  selectedFile.value = e.target.files[0]
  hasFile.value = true
}

function startClone() {
  phase.value = 'processing'
  updateSteps(0)

  const phases = [
    { p: 20, text: 'AI 正在预处理音频...', step: 0 },
    { p: 40, text: '正在进行降噪处理...', step: 1 },
    { p: 60, text: '正在提取声纹特征...', step: 1 },
    { p: 80, text: 'AI 正在训练音色模型...', step: 2 },
    { p: 100, text: '音色克隆完成！', step: 3 },
  ]

  let idx = 0
  const interval = setInterval(() => {
    if (idx < phases.length) {
      const p = phases[idx]
      progress.value = p.p
      statusText.value = p.text
      updateSteps(p.step)
      idx++
    } else {
      clearInterval(interval)
      setTimeout(() => {
        phase.value = 'result'
        showToast('success', '音色克隆成功！')
      }, 500)
    }
  }, 1200)
}

function updateSteps(step) {
  currentStep.value = step
}

function saveResult() {
  mockVoices.unshift({
    id: mockVoices.length + 1,
    name: cloneName.value,
    source: 'cloned',
    status: 'ready',
    mode: '即时克隆',
    date: new Date().toISOString().split('T')[0],
    downloads: 0
  })
  showToast('success', `音色「${cloneName.value}」已保存！`)
  setTimeout(() => router.push('/voices'), 1000)
}

function resetClone() {
  phase.value = 'upload'
  currentStep.value = 0
  progress.value = 0
  hasFile.value = false
  selectedFile.value = null
  if (fileInput.value) fileInput.value.value = ''
}
</script>

<style scoped>
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
