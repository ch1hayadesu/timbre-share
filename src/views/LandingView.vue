<template>
  <div class="landing">
    <header class="landing-header">
      <div class="header-inner">
        <div class="header-logo">
          <div class="logo-icon">♪</div>
          <span>音色共享平台</span>
        </div>
        <nav class="header-nav">
          <a href="#features">产品介绍</a>
          <a href="#stats">数据看板</a>
          <a href="#about">关于我们</a>
        </nav>
        <div class="header-actions">
          <router-link to="/admin/login" class="btn-admin-entry" title="管理员登录">
            <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M12 15v2m-6 4h12a2 2 0 0 0 2-2v-6a6 6 0 0 0-6-6H10a6 6 0 0 0-6 6v6a2 2 0 0 0 2 2z"/><circle cx="12" cy="7" r="3"/></svg>
            <span>管理员</span>
          </router-link>
          <button class="btn-outline" @click="showLogin = true">登录</button>
          <button class="btn-primary" @click="enterGuestMode">立即体验</button>
        </div>
      </div>
    </header>

    <section class="hero">
      <div class="hero-bg"></div>
      <div class="hero-content">
        <h1>AI 驱动的<br/>音色共享平台</h1>
        <p class="hero-sub">上传音频样本，AI 智能克隆专属音色<br/>文本转语音，一键生成自然流畅的 MP3</p>
        <div class="hero-actions">
          <button class="btn-primary btn-lg" @click="enterGuestMode">开始使用</button>
          <button class="btn-outline btn-lg" @click="showLogin = true">登录</button>
        </div>
      </div>
      <div class="hero-visual">
        <div class="hero-card hero-card-1">
          <div class="hero-card-icon">🎤</div>
          <div class="hero-card-label">音色克隆</div>
        </div>
        <div class="hero-card hero-card-2">
          <div class="hero-card-icon">🔊</div>
          <div class="hero-card-label">TTS 合成</div>
        </div>
        <div class="hero-card hero-card-3">
          <div class="hero-card-icon">🎬</div>
          <div class="hero-card-label">剧本配音</div>
        </div>
      </div>
    </section>

    <section id="features" class="features">
      <h2 class="section-title">核心功能</h2>
      <p class="section-desc">基于前沿 AI 技术，打造一站式语音解决方案</p>
      <div class="features-grid">
        <div class="feature-card">
          <div class="feature-icon-wrap" style="background:linear-gradient(135deg,#667eea,#764ba2)">
            <span class="feature-icon">🎤</span>
          </div>
          <h3>音色克隆</h3>
          <p>上传 30 秒音频样本，AI 即可精准克隆你的音色，支持即时克隆与深度克隆两种模式</p>
        </div>
        <div class="feature-card">
          <div class="feature-icon-wrap" style="background:linear-gradient(135deg,#f093fb,#f5576c)">
            <span class="feature-icon">🔊</span>
          </div>
          <h3>TTS 合成</h3>
          <p>多模型支持，选择 Edge TTS 或 GPT-SoVITS 模型，精准控制语速、音调、音量</p>
        </div>
        <div class="feature-card">
          <div class="feature-icon-wrap" style="background:linear-gradient(135deg,#4facfe,#00f2fe)">
            <span class="feature-icon">🎬</span>
          </div>
          <h3>剧本配音</h3>
          <p>上传剧本，AI 智能分配角色，多人配音自动生成，支持多语言、多情感表达</p>
        </div>
        <div class="feature-card">
          <div class="feature-icon-wrap" style="background:linear-gradient(135deg,#43e97b,#38f9d7)">
            <span class="feature-icon">🎵</span>
          </div>
          <h3>音色市场</h3>
          <p>探索社区共享的优质音色，一键下载使用，让你的创作更加丰富多彩</p>
        </div>
        <div class="feature-card">
          <div class="feature-icon-wrap" style="background:linear-gradient(135deg,#fa709a,#fee140)">
            <span class="feature-icon">🤖</span>
          </div>
          <h3>GPT 模型</h3>
          <p>集成 GPT-SoVITS 开源模型，表现力更丰富，生成效果更自然流畅</p>
        </div>
        <div class="feature-card">
          <div class="feature-icon-wrap" style="background:linear-gradient(135deg,#a18cd1,#fbc2eb)">
            <span class="feature-icon">📊</span>
          </div>
          <h3>数据分析</h3>
          <p>可视化工作台，实时追踪音色使用情况、合成次数与下载统计</p>
        </div>
      </div>
    </section>

    <section id="stats" class="stats">
      <div class="stats-inner">
        <h2 class="section-title light">平台数据</h2>
        <p class="section-desc light">越来越多的创作者选择我们</p>
        <div class="stats-grid">
          <div class="stat-item">
            <div class="stat-number">10,000+</div>
            <div class="stat-label">注册用户</div>
          </div>
          <div class="stat-item">
            <div class="stat-number">50,000+</div>
            <div class="stat-label">音色模型</div>
          </div>
          <div class="stat-item">
            <div class="stat-number">1,000,000+</div>
            <div class="stat-label">合成次数</div>
          </div>
          <div class="stat-item">
            <div class="stat-number">99.9%</div>
            <div class="stat-label">服务可用率</div>
          </div>
        </div>
      </div>
    </section>

    <section id="about" class="about">
      <h2 class="section-title">技术架构</h2>
      <p class="section-desc">现代化技术栈，保障高性能与可扩展性</p>
      <div class="tech-list">
        <div class="tech-item">FastAPI</div>
        <div class="tech-item">Vue 3</div>
        <div class="tech-item">Python</div>
        <div class="tech-item">edge-tts</div>
        <div class="tech-item">GPT-SoVITS</div>
        <div class="tech-item">SQLite</div>
        <div class="tech-item">Docker</div>
        <div class="tech-item">RESTful API</div>
      </div>
    </section>

    <footer class="landing-footer">
      <div class="footer-inner">
        <div class="footer-brand">
          <div class="footer-logo">
            <div class="logo-icon">♪</div>
            <span>音色共享平台</span>
          </div>
          <p class="footer-desc">AI 驱动的音色克隆与语音合成平台</p>
        </div>
        <div class="footer-links">
          <div class="footer-col">
            <h4>产品</h4>
            <a href="#features">功能介绍</a>
            <a href="#stats">数据看板</a>
            <a href="#" @click.prevent="enterGuestMode">开始使用</a>
          </div>
        <div class="footer-col">
          <h4>支持</h4>
          <router-link to="/help">帮助中心</router-link>
          <a href="#">联系我们</a>
          <a href="#">反馈建议</a>
        </div>
        <div class="footer-col">
          <h4>管理</h4>
          <router-link to="/admin/login" class="admin-footer-link">
            <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M12 15v2m-6 4h12a2 2 0 0 0 2-2v-6a6 6 0 0 0-6-6H10a6 6 0 0 0-6 6v6a2 2 0 0 0 2 2z"/><circle cx="12" cy="7" r="3"/></svg>
            管理员登录
          </router-link>
        </div>
          <div class="footer-col">
            <h4>法律</h4>
            <a href="#">服务条款</a>
            <a href="#">隐私政策</a>
          </div>
        </div>
      </div>
      <div class="footer-bottom">
        <p>&copy; 2026 音色共享平台 Timbre Share. All rights reserved.</p>
      </div>
    </footer>

    <!-- Login Modal -->
    <Teleport to="body">
      <div v-if="showLogin" class="modal-mask" @click.self="showLogin = false">
        <div class="modal-card">
          <button class="modal-close" @click="showLogin = false">✕</button>
          <h2 class="modal-title">登录 / 注册</h2>
          <p class="modal-desc">登录后使用 AI 语音合成、克隆与配音功能</p>
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
    </Teleport>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import BaseButton from '@/components/BaseButton.vue'
import { sendCode, login } from '@/services'
import { useToast } from '@/composables/useToast'
import { useAuth } from '@/composables/useAuth'

const router = useRouter()
const { showToast } = useToast()
const { setToken, clearToken } = useAuth()

const showLogin = ref(false)
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

function enterGuestMode() {
  clearToken()
  router.push('/dashboard')
}

async function handleLogin() {
  if (phone.value.length < 11) { showToast('warning', '请输入正确的手机号'); return }
  if (code.value.length !== 6) { showToast('warning', '请输入 6 位验证码'); return }
  logging.value = true
  try {
    const result = await login(phone.value, code.value)
    setToken(result.token)
    showToast('success', '登录成功')
    showLogin.value = false
    router.push('/dashboard')
  } catch (err) {
    showToast('error', '登录失败：' + err.message)
  } finally {
    logging.value = false
  }
}
</script>

<style scoped>
.landing {
  min-height: 100vh;
  background: #f8faff;
}

/* Header */
.landing-header {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  z-index: 100;
  background: rgba(255,255,255,0.9);
  backdrop-filter: blur(12px);
  border-bottom: 1px solid rgba(0,0,0,0.06);
}
.header-inner {
  max-width: 1200px;
  margin: 0 auto;
  padding: 0 24px;
  height: 64px;
  display: flex;
  align-items: center;
  gap: 40px;
}
.header-logo {
  display: flex;
  align-items: center;
  gap: 10px;
  font-size: 18px;
  font-weight: 700;
  color: #1a1a2e;
}
.logo-icon {
  width: 34px;
  height: 34px;
  border-radius: 8px;
  background: linear-gradient(135deg, #667eea, #764ba2);
  display: flex;
  align-items: center;
  justify-content: center;
  color: white;
  font-size: 18px;
}
.header-nav {
  flex: 1;
  display: flex;
  gap: 24px;
}
.header-nav a {
  font-size: 14px;
  font-weight: 500;
  color: #555;
  text-decoration: none;
  transition: color 0.2s;
}
.header-nav a:hover { color: #667eea; }
.header-actions { display: flex; gap: 12px; align-items: center; }

.btn-admin-entry {
  display: inline-flex;
  align-items: center;
  gap: 6px;
  padding: 8px 16px;
  border-radius: 8px;
  color: #7C3AED;
  background: rgba(124,58,237,0.06);
  text-decoration: none;
  font-size: 13px;
  font-weight: 600;
  transition: all 0.2s;
  border: 1.5px solid rgba(124,58,237,0.2);
}
.btn-admin-entry:hover {
  color: white;
  background: #7C3AED;
  border-color: #7C3AED;
}
.btn-admin-entry svg { width: 16px; height: 16px; }

/* Buttons */
.btn-outline {
  display: inline-flex;
  align-items: center;
  padding: 10px 24px;
  border: 1.5px solid #667eea;
  border-radius: 8px;
  font-size: 14px;
  font-weight: 600;
  color: #667eea;
  background: transparent;
  cursor: pointer;
  text-decoration: none;
  transition: all 0.2s;
}
.btn-outline:hover {
  background: #667eea;
  color: white;
}
.btn-primary {
  display: inline-flex;
  align-items: center;
  padding: 10px 24px;
  border: none;
  border-radius: 8px;
  font-size: 14px;
  font-weight: 600;
  color: white;
  background: linear-gradient(135deg, #667eea, #764ba2);
  cursor: pointer;
  text-decoration: none;
  transition: all 0.2s;
  box-shadow: 0 4px 14px rgba(102,126,234,0.35);
}
.btn-primary:hover {
  transform: translateY(-1px);
  box-shadow: 0 6px 20px rgba(102,126,234,0.45);
}
.btn-lg { padding: 14px 36px; font-size: 16px; }

/* Hero */
.hero {
  position: relative;
  min-height: 100vh;
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 120px 24px 80px;
  overflow: hidden;
}
.hero-bg {
  position: absolute;
  inset: 0;
  background: linear-gradient(135deg, #f5f7ff 0%, #eef0ff 50%, #f8f0ff 100%);
  z-index: 0;
}
.hero-bg::before {
  content: '';
  position: absolute;
  width: 600px;
  height: 600px;
  border-radius: 50%;
  background: radial-gradient(circle, rgba(102,126,234,0.08) 0%, transparent 70%);
  top: -100px;
  right: -100px;
}
.hero-bg::after {
  content: '';
  position: absolute;
  width: 400px;
  height: 400px;
  border-radius: 50%;
  background: radial-gradient(circle, rgba(118,75,162,0.06) 0%, transparent 70%);
  bottom: -50px;
  left: -50px;
}
.hero-content {
  position: relative;
  z-index: 1;
  max-width: 560px;
}
.hero-content h1 {
  font-size: 52px;
  font-weight: 800;
  line-height: 1.15;
  color: #1a1a2e;
  margin-bottom: 20px;
}
.hero-sub {
  font-size: 18px;
  line-height: 1.6;
  color: #666;
  margin-bottom: 36px;
}
.hero-actions { display: flex; gap: 16px; }
.hero-visual {
  position: relative;
  z-index: 1;
  margin-left: 60px;
}
.hero-card {
  width: 180px;
  padding: 24px;
  background: white;
  border-radius: 16px;
  box-shadow: 0 8px 32px rgba(0,0,0,0.08);
  text-align: center;
  position: absolute;
  transition: transform 0.3s;
}
.hero-card:hover { transform: translateY(-4px); }
.hero-card-1 { top: -40px; left: 0; }
.hero-card-2 { top: 80px; left: 100px; }
.hero-card-3 { top: 200px; left: 0; }
.hero-card-icon { font-size: 36px; margin-bottom: 8px; }
.hero-card-label { font-size: 14px; font-weight: 600; color: #333; }

/* Sections */
section { padding: 100px 24px; }
.section-title {
  text-align: center;
  font-size: 32px;
  font-weight: 700;
  color: #1a1a2e;
  margin-bottom: 12px;
}
.section-title.light { color: white; }
.section-desc {
  text-align: center;
  font-size: 16px;
  color: #888;
  margin-bottom: 60px;
  max-width: 500px;
  margin-left: auto;
  margin-right: auto;
}
.section-desc.light { color: rgba(255,255,255,0.7); }

/* Features */
.features {
  max-width: 1100px;
  margin: 0 auto;
}
.features-grid {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 24px;
}
.feature-card {
  background: white;
  border-radius: 16px;
  padding: 32px;
  box-shadow: 0 2px 16px rgba(0,0,0,0.06);
  transition: all 0.3s;
}
.feature-card:hover {
  transform: translateY(-4px);
  box-shadow: 0 8px 32px rgba(0,0,0,0.1);
}
.feature-icon-wrap {
  width: 52px;
  height: 52px;
  border-radius: 14px;
  display: flex;
  align-items: center;
  justify-content: center;
  margin-bottom: 16px;
}
.feature-icon { font-size: 24px; }
.feature-card h3 {
  font-size: 18px;
  font-weight: 600;
  color: #1a1a2e;
  margin-bottom: 10px;
}
.feature-card p {
  font-size: 14px;
  color: #777;
  line-height: 1.6;
}

/* Stats */
.stats {
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
}
.stats-inner { max-width: 900px; margin: 0 auto; }
.stats-grid {
  display: grid;
  grid-template-columns: repeat(4, 1fr);
  gap: 32px;
}
.stat-item { text-align: center; }
.stat-number {
  font-size: 42px;
  font-weight: 800;
  color: white;
  margin-bottom: 8px;
}
.stat-label {
  font-size: 16px;
  color: rgba(255,255,255,0.75);
}

/* About / Tech */
.about { max-width: 900px; margin: 0 auto; }
.tech-list {
  display: flex;
  flex-wrap: wrap;
  justify-content: center;
  gap: 16px;
  max-width: 600px;
  margin: 0 auto;
}
.tech-item {
  padding: 10px 24px;
  background: white;
  border-radius: 10px;
  font-size: 14px;
  font-weight: 600;
  color: #555;
  box-shadow: 0 2px 8px rgba(0,0,0,0.05);
}

/* Footer */
.landing-footer {
  background: #1a1a2e;
  color: rgba(255,255,255,0.7);
  padding: 60px 24px 0;
}
.footer-inner {
  max-width: 1100px;
  margin: 0 auto;
  display: flex;
  gap: 80px;
}
.footer-brand { flex: 1; }
.footer-logo {
  display: flex;
  align-items: center;
  gap: 10px;
  font-size: 18px;
  font-weight: 700;
  color: white;
  margin-bottom: 12px;
}
.footer-desc { font-size: 14px; line-height: 1.6; }
.footer-links {
  display: flex;
  gap: 60px;
}
.footer-col h4 {
  font-size: 14px;
  font-weight: 600;
  color: white;
  margin-bottom: 16px;
}
.footer-col a {
  display: block;
  font-size: 14px;
  color: rgba(255,255,255,0.6);
  text-decoration: none;
  margin-bottom: 10px;
  transition: color 0.2s;
}
.footer-col a:hover { color: white; }

.admin-footer-link {
  display: inline-flex;
  align-items: center;
  gap: 6px;
  color: rgba(255,255,255,0.6);
  text-decoration: none;
  font-size: 14px;
  margin-bottom: 10px;
  transition: color 0.2s;
}
.admin-footer-link svg { width: 14px; height: 14px; }
.admin-footer-link:hover { color: #A78BFA; }
.footer-bottom {
  text-align: center;
  padding: 24px 0;
  margin-top: 60px;
  border-top: 1px solid rgba(255,255,255,0.1);
  font-size: 13px;
}

/* Login Modal */
.modal-mask {
  position: fixed;
  inset: 0;
  background: rgba(0,0,0,0.5);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 10000;
}
.modal-card {
  background: white;
  border-radius: 16px;
  padding: 40px 32px;
  width: 380px;
  position: relative;
  box-shadow: 0 20px 60px rgba(0,0,0,0.15);
}
.modal-close {
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
.modal-close:hover { background: #e0e0e0; }
.modal-title {
  font-size: 22px;
  font-weight: 700;
  text-align: center;
  margin-bottom: 4px;
  color: #1a1a2e;
}
.modal-desc {
  font-size: 13px;
  color: #888;
  text-align: center;
  margin-bottom: 28px;
}
.form-group {
  margin-bottom: 20px;
}
.form-group label {
  font-size: 13px;
  font-weight: 500;
  color: #444;
  display: block;
  margin-bottom: 6px;
}
.login-input {
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
.login-input:focus {
  border-color: #667eea;
  box-shadow: 0 0 0 3px rgba(102,126,234,0.15);
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
