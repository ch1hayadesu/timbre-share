<template>
  <div>
    <div class="page-header">
      <h1 class="page-title">设置</h1>
      <p class="page-desc">管理个人资料、账号与系统偏好</p>
    </div>

    <Card>
      <h3 class="panel-title">个人资料</h3>
      <div class="setting-row">
        <span class="setting-label">用户ID</span>
        <span class="setting-value">{{ userId }}</span>
      </div>
      <div class="setting-row">
        <span class="setting-label">手机号</span>
        <span class="setting-value">{{ phone }}</span>
      </div>
      <div class="setting-row">
        <span class="setting-label">音色数量</span>
        <span class="setting-value">{{ voiceCount }} 个</span>
      </div>
    </Card>

    <Card style="margin-top:var(--space-4);">
      <h3 class="panel-title">系统偏好</h3>
      <div class="setting-row">
        <span class="setting-label">默认音色</span>
        <select class="base-select setting-select" v-model="defaultVoice">
          <option v-for="v in voiceOptions" :key="v.value" :value="v.value">{{ v.label }}</option>
        </select>
      </div>
      <div class="setting-row">
        <span class="setting-label">配音轮询间隔</span>
        <select class="base-select setting-select" v-model="pollInterval">
          <option value="3">3 秒</option>
          <option value="5">5 秒</option>
          <option value="10">10 秒</option>
        </select>
      </div>
    </Card>

    <Card style="margin-top:var(--space-4);">
      <h3 class="panel-title">关于</h3>
      <div class="setting-row">
        <span class="setting-label">版本</span>
        <span class="setting-value">正式版 1.0</span>
      </div>
      <div class="setting-row">
        <span class="setting-label">技术栈</span>
        <span class="setting-value">FastAPI + Vue3 + MySQL + edge-tts</span>
      </div>
      <div class="setting-row" style="border:none;">
        <span class="setting-label">项目</span>
        <span class="setting-value">音色共享平台 Timbre Share</span>
      </div>
    </Card>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import Card from '@/components/Card.vue'
import { getTTSVoiceOptions } from '@/services'

const userId = ref(localStorage.getItem('userId') || '1')
const phone = ref('138****0000')
const voiceCount = ref(0)
const defaultVoice = ref(1)
const pollInterval = ref(3)
const voiceOptions = ref([])

onMounted(async () => {
  try {
    voiceOptions.value = await getTTSVoiceOptions()
  } catch (_) {}
  try {
    const { getVoiceList } = await import('@/services')
    const result = await getVoiceList({ page: 1, pageSize: 1 })
    voiceCount.value = result.total || 0
  } catch (_) {}
})
</script>

<style scoped>
.panel-title {
  font-size: var(--font-size-md);
  font-weight: 600;
  color: var(--color-text-primary);
  margin-bottom: var(--space-4);
}

.setting-row {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: var(--space-3) 0;
  border-bottom: 1px solid var(--color-border-light);
}
.setting-row:last-child { border-bottom: none; }

.setting-label {
  font-size: var(--font-size-base);
  color: var(--color-text-body);
}

.setting-value {
  font-size: var(--font-size-base);
  color: var(--color-text-secondary);
}

.setting-select {
  width: 160px;
}
</style>
