<template>
  <div>
    <div class="page-header">
      <h1 class="page-title">TTS 合成</h1>
      <p class="page-desc">输入文本，选择音色，一键生成自然流畅的语音</p>
    </div>

    <div class="tts-layout">
      <div class="tts-panel">
        <Card>
          <h3 class="panel-title">文本内容</h3>
          <textarea class="base-textarea" v-model="ttsText" placeholder="请输入要合成的文本内容（不超过1000字）..."
            @input="updateCharCount" rows="8"></textarea>
          <div class="char-count" :class="{ over: charCount > 1000 }">{{ charCount }} / 1000</div>
        </Card>
      </div>

      <div class="tts-panel">
        <Card>
          <h3 class="panel-title">参数设置</h3>

          <div class="form-group">
            <label>选择音色</label>
            <select class="base-select wide" v-model="selectedVoice">
              <optgroup v-if="presetVoices.length" label="预设音色">
                <option v-for="v in presetVoices" :key="v.value" :value="v.value">{{ v.label }}</option>
              </optgroup>
              <optgroup v-if="userVoices.length" label="我的音色">
                <option v-for="v in userVoices" :key="v.value" :value="v.value">{{ v.label }}</option>
              </optgroup>
            </select>
          </div>

          <div class="form-group">
            <label>合成模型</label>
            <select class="base-select wide" v-model="selectedModel">
              <option v-for="m in availableModels" :key="m.name" :value="m.name">
                {{ m.display_name }}
                <template v-if="m.requires_env_setup"> ⚠️ 需配置</template>
              </option>
            </select>
            <p v-if="modelNotice" class="form-notice">{{ modelNotice }}</p>
          </div>

          <div class="form-group">
            <div class="slider-label">
              <span>语速</span>
              <span class="slider-value">{{ ttsSpeed }}x</span>
            </div>
            <input type="range" class="slider" min="0.5" max="2.0" step="0.1" v-model="ttsSpeed">
          </div>

          <div class="form-group">
            <div class="slider-label">
              <span>音量</span>
              <span class="slider-value">{{ ttsVolume }}%</span>
            </div>
            <input type="range" class="slider" min="0" max="100" step="5" v-model="ttsVolume">
          </div>

          <div class="form-group">
            <div class="slider-label">
              <span>音调</span>
              <span class="slider-value">{{ ttsPitch }}</span>
            </div>
            <input type="range" class="slider" min="-12" max="12" step="1" v-model="ttsPitch">
          </div>

          <div class="form-group">
            <label>情感</label>
            <select class="base-select wide" v-model="ttsEmotion">
              <option value="">无（默认）</option>
              <option value="happy">快乐 😊</option>
              <option value="sad">悲伤 😢</option>
              <option value="angry">生气 😠</option>
              <option value="fear">恐惧 😨</option>
              <option value="disgust">厌恶 🤢</option>
              <option value="surprise">惊讶 😲</option>
            </select>
          </div>

          <BaseButton type="primary" size="lg" class="full-width" :loading="synthesizing" @click="synthesize">
            <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
              <polygon points="11 5 6 9 2 9 2 15 6 15 11 19 11 5" />
            </svg>
            {{ synthesizing ? '合成中...' : '开始合成' }}
          </BaseButton>
        </Card>
      </div>
    </div>

    <!-- TTS Result -->
    <Card v-if="showResult" style="margin-top:24px;">
      <div class="result-header">
        <h3>✓ 合成完成</h3>
        <BaseTag type="success">成功</BaseTag>
      </div>
      <AudioPlayer v-if="audioUrl" title="🎵 TTS合成结果" :src="audioUrl" />
      <div class="btn-group" style="margin-top:12px;">
        <BaseButton type="default" size="sm" @click="synthesize">
          <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><polyline points="1 4 1 10 7 10"/><polyline points="23 20 23 14 17 14"/><path d="M20.49 9A9 9 0 005.64 5.64L1 10m22 4l-4.64 4.36A9 9 0 013.51 15"/></svg>
          重新合成
        </BaseButton>
      </div>
    </Card>

    <!-- 合成记录 -->
    <div class="section-title" style="margin-top:32px;">合成记录</div>
    <Card style="padding:0;overflow:hidden;">
      <table class="synthesis-table" v-if="historyList.items.length">
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
          <tr v-for="item in historyList.items" :key="item.id">
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
                <BaseButton type="default" size="sm" @click="playHistoryAudio(item)">
                  <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><polygon points="5 3 19 12 5 21 5 3"/></svg>
                  播放
                </BaseButton>
                <BaseButton type="default" size="sm" @click="downloadHistoryAudio(item)">
                  <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M21 15v4a2 2 0 01-2 2H5a2 2 0 01-2-2v-4"/><polyline points="7 10 12 15 17 10"/><line x1="12" y1="15" x2="12" y2="3"/></svg>
                  下载
                </BaseButton>
              </template>
              <BaseButton v-else type="default" size="sm" @click="retrySynthesize(item)">
                <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><polyline points="1 4 1 10 7 10"/><polyline points="23 20 23 14 17 14"/><path d="M20.49 9A9 9 0 005.64 5.64L1 10m22 4l-4.64 4.36A9 9 0 013.51 15"/></svg>
                重新合成
              </BaseButton>
            </td>
          </tr>
        </tbody>
      </table>
      <div v-else style="padding:32px;text-align:center;color:var(--color-text-disabled);">暂无合成记录</div>
    </Card>
  </div>
</template>

<script setup>
import { ref, reactive, computed, onMounted } from 'vue'
import Card from '@/components/Card.vue'
import BaseButton from '@/components/BaseButton.vue'
import BaseTag from '@/components/BaseTag.vue'
import AudioPlayer from '@/components/AudioPlayer.vue'
import { getTTSVoiceOptions, createSynthesis, getSynthesisList, getTTSModels } from '@/services'
import { incrementSynthesisCount } from '@/services/statsCounter'
import { useToast } from '@/composables/useToast'
import { useAuth } from '@/composables/useAuth'
import StatusBadge from '@/components/StatusBadge.vue'

const { showToast } = useToast()
const { requireAuth } = useAuth()

const ttsText = ref('大家好，欢迎使用音色共享平台。这是一个基于AI技术的语音合成工具，可以帮助你快速将文字转换为自然流畅的语音。只需选择你喜欢的音色，输入文本，点击合成即可获得高质量的MP3音频文件。')
const selectedVoice = ref(1)
const selectedModel = ref('edge-tts')
const availableModels = ref([])
const ttsSpeed = ref(1.0)
const ttsVolume = ref(80)
const ttsPitch = ref(0)
const ttsEmotion = ref('')
const showResult = ref(false)
const synthesizing = ref(false)
const audioUrl = ref('')
const historyList = reactive({ items: [] })

// 从 Service 加载音色选项
const ttsVoiceOptions = ref([])

const presetVoices = computed(() => ttsVoiceOptions.value.filter(v => v.category === 'preset'))
const userVoices = computed(() => ttsVoiceOptions.value.filter(v => v.category === 'user'))

async function loadVoiceOptions() {
  try {
    ttsVoiceOptions.value = await getTTSVoiceOptions()
    if (ttsVoiceOptions.value.length > 0) {
      selectedVoice.value = ttsVoiceOptions.value[0].value
    }
  } catch (err) {
    if (!err.message?.includes('401')) showToast('error', '加载音色选项失败：' + err.message)
  }
}

async function loadModels() {
  try {
    availableModels.value = await getTTSModels()
    if (availableModels.value.length > 0) {
      selectedModel.value = availableModels.value[0].name
    }
  } catch (err) {
    availableModels.value = [{ name: 'edge-tts', display_name: 'Edge TTS (默认)' }]
  }
}

const modelNotice = computed(() => {
  const m = availableModels.value.find(x => x.name === selectedModel.value)
  if (m && m.requires_env_setup) return m.requires_env_setup
  return ''
})

onMounted(() => {
  loadVoiceOptions()
  loadModels()
  loadHistory()
})

async function loadHistory() {
  try {
    const result = await getSynthesisList({ page: 1, pageSize: 10 })
    historyList.items = result.items
  } catch (_) { /* guest mode: skip */ }
}

function retrySynthesize(item) {
  ttsText.value = item.text || ''
  synthesize()
}

function playHistoryAudio(item) {
  const url = item.audio_url
  if (!url) {
    showToast('warning', '该记录暂无音频文件')
    return
  }
  const audio = new Audio('/audio/' + url.replace(/^\//, ''))
  audio.play().catch(() => {
    showToast('error', '音频加载失败')
  })
}

function downloadHistoryAudio(item) {
  const url = item.audio_url
  if (!url) {
    showToast('warning', '该记录暂无音频文件')
    return
  }
  const fullUrl = '/audio/' + url.replace(/^\//, '')
  const a = document.createElement('a')
  a.href = fullUrl
  a.download = url.split('/').pop() || 'tts_output.mp3'
  document.body.appendChild(a)
  a.click()
  document.body.removeChild(a)
}

const charCount = computed(() => ttsText.value.length)

function updateCharCount() { /* computed auto */ }

async function synthesize() {
  if (!requireAuth(synthesize)) return
  if (!ttsText.value.trim()) { showToast('warning', '请输入合成文本'); return }
  if (ttsText.value.length > 1000) { showToast('error', '文本超过1000字限制'); return }

  synthesizing.value = true
  showResult.value = false
  audioUrl.value = ''

  try {
    const rec = await createSynthesis({
      text: ttsText.value,
      voice_id: selectedVoice.value,
      speed: ttsSpeed.value,
      volume: ttsVolume.value,
      pitch: ttsPitch.value,
      emotion: ttsEmotion.value || undefined,
      model: selectedModel.value,
    })
    const result = await pollTaskResult(rec.record_id)
    audioUrl.value = result.audio_url ? `/audio/${result.audio_url}` : ''
    showResult.value = true
    incrementSynthesisCount()
    loadHistory()
    showToast('success', 'TTS合成完成！')
  } catch (err) {
    showToast('error', '合成失败：' + err.message)
  } finally {
    synthesizing.value = false
  }
}

async function pollTaskResult(taskId, maxWait = 60) {
  const { pollTask } = await import('@/services')
  for (let i = 0; i < maxWait; i++) {
    await new Promise(r => setTimeout(r, 3000))
    try {
      const result = await pollTask(taskId)
      if (result.status === 1) return result
      if (result.status === -1) throw new Error(result.error_message || '任务失败')
    } catch (err) {
      if (err.message?.includes('任务未就绪')) continue
      throw err
    }
  }
  throw new Error('任务超时，请稍后重试')
}
</script>

<style scoped>
.panel-title {
  font-size: var(--font-size-md);
  font-weight: 600;
  color: var(--color-text-primary);
  margin-bottom: var(--space-4);
}

.base-textarea {
  min-height: 200px;
  padding: var(--space-3);
  resize: vertical;
  border: 1px solid var(--color-border-default);
  border-radius: var(--radius-md);
  font-size: var(--font-size-base);
  color: var(--color-text-body);
  background: white;
  outline: none;
  transition: all var(--duration-fast);
  width: 100%;
  line-height: 1.8;
}

.base-textarea:focus {
  border-color: var(--color-primary-6);
  box-shadow: var(--shadow-focus);
}

.char-count {
  text-align: right;
  font-size: var(--font-size-xs);
  color: var(--color-text-secondary);
  margin-top: var(--space-2);
}

.char-count.over { color: var(--color-error); }

.form-group { margin-bottom: var(--space-5); }

.form-group label {
  font-size: var(--font-size-sm);
  font-weight: 500;
  color: var(--color-text-body);
  display: block;
  margin-bottom: var(--space-2);
}

.base-select.wide { width: 100%; }

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

.slider-label {
  display: flex;
  justify-content: space-between;
  margin-bottom: var(--space-2);
}

.slider-label span:first-child {
  font-size: var(--font-size-sm);
  font-weight: 500;
  color: var(--color-text-body);
}

.slider-value {
  font-size: var(--font-size-sm);
  color: var(--color-primary-6);
  font-weight: 600;
}

.slider {
  width: 100%;
  height: 4px;
  border-radius: 2px;
  background: var(--color-border-light);
  outline: none;
  -webkit-appearance: none;
  appearance: none;
}

.slider::-webkit-slider-thumb {
  -webkit-appearance: none;
  width: 18px;
  height: 18px;
  border-radius: 50%;
  background: white;
  border: 2px solid var(--color-primary-6);
  cursor: pointer;
  box-shadow: var(--shadow-sm);
}

.slider::-webkit-slider-thumb:hover { border-color: var(--color-primary-7); }

.form-notice {
  font-size: var(--font-size-xs);
  color: var(--color-warning);
  margin-top: var(--space-1);
}

.full-width {
  width: 100%;
  margin-top: var(--space-2);
}

.result-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  margin-bottom: var(--space-4);
}

.result-header h3 {
  font-size: var(--font-size-md);
  font-weight: 600;
  color: var(--color-text-primary);
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
