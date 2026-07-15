<template>
  <div class="app-shell">
    <!-- 管理员界面 -->
    <template v-if="isAdminRoute">
      <AdminLayout />
      <ToastContainer />
      <ModalBox />
    </template>
    <!-- 落地页 (无导航) -->
    <template v-else-if="isLanding">
      <router-view />
    </template>
    <!-- 管理员登录页 (无导航) -->
    <template v-else-if="isAdminLogin">
      <router-view />
    </template>
    <!-- 普通用户界面 -->
    <template v-else>
      <TopNav @toggle-sidebar="toggleSidebar" />
      <div v-if="sidebarOpen" class="sidebar-overlay" @click="closeSidebar"></div>
      <SideNav :is-open="sidebarOpen" @toast="handleToast" />
      <MainLayout />
      <ToastContainer />
      <ModalBox />
      <DrawerPanel />
    </template>

    <!-- Global Login Modal -->
    <Teleport to="body">
      <div v-if="showLogin" class="login-modal-mask" @click.self="cancelLogin">
        <div class="login-modal-card">
          <button class="login-modal-close" @click="cancelLogin">✕</button>
          <h2 class="login-modal-title">登录 / 注册</h2>
          <p class="login-modal-desc">登录后可使用 AI 语音合成、克隆与配音功能</p>
          <div class="login-modal-form">
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
      </div>
    </Teleport>
  </div>
</template>

<script setup>
import { ref, computed } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import TopNav from '@/components/TopNav.vue'
import SideNav from '@/components/SideNav.vue'
import MainLayout from '@/components/MainLayout.vue'
import AdminLayout from '@/components/AdminLayout.vue'
import ToastContainer from '@/components/ToastContainer.vue'
import ModalBox from '@/components/ModalBox.vue'
import DrawerPanel from '@/components/DrawerPanel.vue'
import BaseButton from '@/components/BaseButton.vue'
import { useToast } from '@/composables/useToast'
import { useAuth } from '@/composables/useAuth'
import { sendCode, login } from '@/services'

const route = useRoute()
const router = useRouter()
const { showToast } = useToast()
const { showLogin, setToken, onLoginSuccess, cancelLogin } = useAuth()
const sidebarOpen = ref(false)

const isLanding = computed(() => route.meta?.layout === 'landing')
const isAdminRoute = computed(() => route.path.startsWith('/admin') && route.meta?.admin && route.path !== '/admin/login')
const isAdminLogin = computed(() => route.path === '/admin/login')

const phone = ref('13800000000')
const code = ref('')
const sending = ref(false)
const logging = ref(false)
const countdown = ref(0)
let timer = null

function toggleSidebar() {
  sidebarOpen.value = !sidebarOpen.value
}

function closeSidebar() {
  sidebarOpen.value = false
}

function handleToast(type, message) {
  showToast(type, message)
}

async function handleSendCode() {
  if (phone.value.length < 11) { showToast('warning', '请输入正确的手机号'); return }
  sending.value = true
  try {
    await sendCode(phone.value)
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
    const result = await login(phone.value, code.value)
    setToken(result.token)
    showToast('success', '登录成功')
    onLoginSuccess()
  } catch (err) {
    showToast('error', '登录失败：' + err.message)
  } finally {
    logging.value = false
  }
}
</script>

<style scoped>
.app-shell {
  height: 100vh;
  overflow: hidden;
}

.sidebar-overlay {
  display: none;
}

@media (max-width: 1279px) {
  .sidebar-overlay {
    display: block;
    position: fixed;
    inset: 0;
    background: rgba(0, 0, 0, 0.3);
    z-index: 89;
  }
}

.login-modal-mask {
  position: fixed;
  inset: 0;
  background: rgba(0,0,0,0.5);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 10000;
}
.login-modal-card {
  background: white;
  border-radius: 16px;
  padding: 40px 32px;
  width: 380px;
  position: relative;
  box-shadow: 0 20px 60px rgba(0,0,0,0.15);
}
.login-modal-close {
  position: absolute;
  top: 16px;
  right: 16px;
  width: 32px;
  height: 32px;
  border-radius: 50%;
  border: none;
  background: #f0f0f0;
  cursor: pointer;
  font-size: 14px;
  display: flex;
  align-items: center;
  justify-content: center;
  color: #666;
}
.login-modal-close:hover { background: #e0e0e0; }
.login-modal-title {
  font-size: 22px;
  font-weight: 700;
  text-align: center;
  margin-bottom: 4px;
  color: #1a1a2e;
}
.login-modal-desc {
  font-size: 13px;
  color: #888;
  text-align: center;
  margin-bottom: 28px;
}
.login-modal-form .form-group {
  margin-bottom: 20px;
}
.login-modal-form .form-group label {
  font-size: 13px;
  font-weight: 500;
  color: #444;
  display: block;
  margin-bottom: 6px;
}
.login-modal-form .login-input {
  width: 100%;
  height: 40px;
  padding: 0 12px;
  border: 1.5px solid #e0e0e0;
  border-radius: 8px;
  font-size: 14px;
  outline: none;
  transition: border-color 0.2s;
  box-sizing: border-box;
}
.login-modal-form .login-input:focus {
  border-color: #667eea;
  box-shadow: 0 0 0 3px rgba(102,126,234,0.15);
}
.login-modal-form .code-row {
  display: flex;
  gap: 8px;
}
.login-modal-form .code-row .login-input {
  flex: 1;
}
.login-modal-form .full-width { width: 100%; margin-top: 8px; }
</style>
