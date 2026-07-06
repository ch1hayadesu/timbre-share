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
              <option v-for="v in ttsVoiceOptions" :key="v.value" :value="v.value">{{ v.label }}</option>
            </select>
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

          <BaseButton type="primary" size="lg" class="full-width" @click="synthesize">
            <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
              <polygon points="11 5 6 9 2 9 2 15 6 15 11 19 11 5" />
            </svg>
            开始合成
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
      <AudioPlayer title="🎵 TTS合成结果" :current-time="'0:00'" :duration="'0:18'" :progress="0"
        info="MP3格式 · 128kbps">
        <template #actions>
          <BaseButton size="sm" style="margin-left:auto;">⬇ 下载 MP3</BaseButton>
          <BaseButton type="text" size="sm" @click="synthesize">重新合成</BaseButton>
        </template>
      </AudioPlayer>
    </Card>
  </div>
</template>

<script setup>
import { ref, computed } from 'vue'
import Card from '@/components/Card.vue'
import BaseButton from '@/components/BaseButton.vue'
import BaseTag from '@/components/BaseTag.vue'
import AudioPlayer from '@/components/AudioPlayer.vue'
import { ttsVoiceOptions } from '@/data/mock'
import { useToast } from '@/composables/useToast'

const { showToast } = useToast()

const ttsText = ref('大家好，欢迎使用音色共享平台。这是一个基于AI技术的语音合成工具，可以帮助你快速将文字转换为自然流畅的语音。只需选择你喜欢的音色，输入文本，点击合成即可获得高质量的MP3音频文件。')
const selectedVoice = ref(1)
const ttsSpeed = ref(1.0)
const ttsVolume = ref(80)
const ttsPitch = ref(0)
const showResult = ref(false)

const charCount = computed(() => ttsText.value.length)

function updateCharCount() { /* computed auto */ }

function synthesize() {
  if (!ttsText.value.trim()) { showToast('warning', '请输入合成文本'); return }
  if (ttsText.value.length > 1000) { showToast('error', '文本超过1000字限制'); return }
  showToast('info', '正在合成语音...')
  setTimeout(() => {
    showResult.value = true
    showToast('success', 'TTS合成完成！')
  }, 2000)
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
</style>
