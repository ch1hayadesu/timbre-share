<template>
  <div class="login-page">
    <div class="login-card">
      <h1 class="login-title">音色共享平台</h1>
      <p class="login-desc">登录后使用 AI 语音合成、克隆与配音功能</p>

      <div class="form-group">
        <label>手机号</label>
        <input type="tel" class="login-input" v-model="phone" placeholder="请输入手机号" maxlength="11">
      </div>

      <div class="form-group">
        <label>验证码</label>
        <div class="code-row">
          <input type="text" class="login-input" v-model="code" placeholder="6 位验证码" maxlength="6">
          <BaseButton size="sm" :disabled="sending || countdown > 0" @click="handleSendCode">
            {{ countdown > 0 ? `${countdown}s` : sending ? '发送中...' : '获取验证码' }}
          </BaseButton>
        </div>
      </div>

      <BaseButton type="primary" size="lg" class="full-width" :loading="logging" @click="handleLogin">
        登录 / 注册
      </BaseButton>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import BaseButton from '@/components/BaseButton.vue'
import { sendCode as apiSendCode, login as apiLogin } from '@/services'
import { useToast } from '@/composables/useToast'

const router = useRouter()
const { showToast } = useToast()

const phone = ref('13800000000')
const code = ref('')
const sending = ref(false)
const logging = ref(false)
const countdown = ref(0)

let timer = null

async function handleSendCode() {
  if (phone.value.length < 11) { showToast('warning', '请输入正确的手机号'); return }
  sending.value = true
  try {
    await apiSendCode(phone.value)
    showToast('success', '验证码已发送')
    countdown.value = 60
    timer = setInterval(() => { countdown.value--; if (countdown.value <= 0) clearInterval(timer) }, 1000)
  } catch (err) {
    showToast('error', '发送失败：' + err.message)
  } finally {
    sending.value = false
  }
}

async function handleLogin() {
  if (phone.value.length < 11) { showToast('warning', '请输入正确的手机号'); return }
  if (code.value.length !== 6) { showToast('warning', '请输入 6 位验证码'); return }
  logging.value = true
  try {
    const result = await apiLogin(phone.value, code.value)
    localStorage.setItem('authToken', result.token)
    showToast('success', '登录成功')
    router.push('/')
  } catch (err) {
    showToast('error', '登录失败：' + err.message)
  } finally {
    logging.value = false
  }
}
</script>

<style scoped>
.login-page {
  min-height: 100vh;
  display: flex;
  align-items: center;
  justify-content: center;
  background: var(--color-bg-page);
}
.login-card {
  width: 380px;
  padding: 40px 32px;
  background: white;
  border-radius: var(--radius-lg);
  box-shadow: var(--shadow-lg);
}
.login-title {
  font-size: 24px;
  font-weight: 700;
  text-align: center;
  margin-bottom: 4px;
}
.login-desc {
  font-size: 13px;
  color: var(--color-text-secondary);
  text-align: center;
  margin-bottom: 28px;
}
.form-group {
  margin-bottom: 20px;
}
.form-group label {
  font-size: 13px;
  font-weight: 500;
  color: var(--color-text-body);
  display: block;
  margin-bottom: 6px;
}
.login-input {
  width: 100%;
  height: 40px;
  padding: 0 12px;
  border: 1px solid var(--color-border-default);
  border-radius: var(--radius-md);
  font-size: 14px;
  outline: none;
  transition: border-color var(--duration-fast);
  box-sizing: border-box;
}
.login-input:focus {
  border-color: var(--color-primary-6);
  box-shadow: var(--shadow-focus);
}
.code-row {
  display: flex;
  gap: 8px;
}
.code-row .login-input {
  flex: 1;
}
.full-width { width: 100%; margin-top: 8px; }
</style>
