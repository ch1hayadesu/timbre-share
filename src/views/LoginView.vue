<template>
  <div class="login-page" :class="{ 'admin-login': isAdmin }">
    <div class="login-card">
      <!-- Admin Login -->
      <template v-if="isAdmin">
        <div class="login-badge">
          <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M12 15v2m-6 4h12a2 2 0 0 0 2-2v-6a6 6 0 0 0-6-6H10a6 6 0 0 0-6 6v6a2 2 0 0 0 2 2z"/><circle cx="12" cy="7" r="3"/></svg>
          管理员登录
        </div>
        <h1 class="login-title">运维管理平台</h1>
        <p class="login-desc">请使用管理员账号登录</p>

        <div class="form-group">
          <label>用户名</label>
          <input type="text" class="login-input" v-model="adminUsername" placeholder="请输入管理员用户名" @keyup.enter="handleAdminLogin">
        </div>

        <div class="form-group">
          <label>密码</label>
          <input type="password" class="login-input" v-model="adminPassword" placeholder="请输入密码" @keyup.enter="handleAdminLogin">
        </div>

        <BaseButton type="primary" size="lg" class="full-width" :loading="adminLogging" @click="handleAdminLogin">
          登录
        </BaseButton>

        <div class="login-switch">
          <a href="/login">返回用户登录</a>
        </div>
      </template>

      <!-- User Login -->
      <template v-else>
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

        <div class="login-switch">
          <a href="/admin/login">管理员入口</a>
        </div>
      </template>
    </div>
  </div>
</template>

<script setup>
import { ref, computed } from 'vue'
import { useRouter } from 'vue-router'
import BaseButton from '@/components/BaseButton.vue'
import { sendCode as apiSendCode, login as apiLogin } from '@/services'
import { adminLogin } from '@/services/adminApi.js'
import { useToast } from '@/composables/useToast'
import { useAuth } from '@/composables/useAuth'

const props = defineProps({
  mode: { type: String, default: 'user' }
})

const router = useRouter()
const { showToast } = useToast()
const { setToken, setAdminToken } = useAuth()

const isAdmin = computed(() => props.mode === 'admin')

// 用户登录
const phone = ref('13800000000')
const code = ref('')
const sending = ref(false)
const logging = ref(false)
const countdown = ref(0)
let timer = null

// 管理员登录
const adminUsername = ref('admin')
const adminPassword = ref('')
const adminLogging = ref(false)

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
    setToken(result.token)
    showToast('success', '登录成功')
    router.push('/')
  } catch (err) {
    showToast('error', '登录失败：' + err.message)
  } finally {
    logging.value = false
  }
}

async function handleAdminLogin() {
  if (!adminUsername.value) { showToast('warning', '请输入用户名'); return }
  if (!adminPassword.value) { showToast('warning', '请输入密码'); return }
  adminLogging.value = true
  try {
    const result = await adminLogin(adminUsername.value, adminPassword.value)
    if (result.role !== 'admin') {
      showToast('error', '无管理员权限')
      return
    }
    setAdminToken(result.token, result.username)
    showToast('success', '管理员登录成功')
    router.push('/admin/dashboard')
  } catch (err) {
    showToast('error', '登录失败：' + err.message)
  } finally {
    adminLogging.value = false
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

.login-page.admin-login {
  background: linear-gradient(135deg, #1a1a2e 0%, #16213e 50%, #0f3460 100%);
}

.login-card {
  width: 380px;
  padding: 40px 32px;
  background: white;
  border-radius: var(--radius-lg);
  box-shadow: var(--shadow-lg);
}

.admin-login .login-card {
  background: rgba(255,255,255,0.95);
  backdrop-filter: blur(10px);
}

.login-badge {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 8px;
  font-size: 12px;
  font-weight: 600;
  color: #7C3AED;
  text-transform: uppercase;
  letter-spacing: 1px;
  margin-bottom: 12px;
}

.login-badge svg { width: 18px; height: 18px; }

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

.code-row .login-input { flex: 1; }

.full-width { width: 100%; margin-top: 8px; }

.login-switch {
  margin-top: 20px;
  text-align: center;
}

.login-switch a {
  font-size: 13px;
  color: #888;
  text-decoration: none;
  transition: color 0.2s;
}

.login-switch a:hover { color: #7C3AED; }
</style>
