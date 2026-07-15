import { createRouter, createWebHistory } from 'vue-router'

const routes = [
  {
    path: '/login',
    name: 'login',
    component: () => import('@/views/LoginView.vue'),
    meta: { title: '登录', guest: true, layout: 'blank' }
  },
  {
    path: '/',
    name: 'landing',
    component: () => import('@/views/LandingView.vue'),
    meta: { title: '音色共享平台', guest: true, layout: 'landing' }
  },
  {
    path: '/dashboard',
    name: 'home',
    component: () => import('@/views/HomeView.vue'),
    meta: { title: '工作台', icon: 'home' }
  },
  {
    path: '/voices',
    name: 'voices',
    component: () => import('@/views/VoiceManageView.vue'),
    meta: { title: '我的音色', icon: 'music' }
  },
  {
    path: '/clone',
    name: 'clone',
    component: () => import('@/views/VoiceCloneView.vue'),
    meta: { title: '音色克隆', icon: 'mic' }
  },
  {
    path: '/tts',
    name: 'tts',
    component: () => import('@/views/TTSSynthesisView.vue'),
    meta: { title: 'TTS合成', icon: 'volume' }
  },
  {
    path: '/script',
    name: 'script',
    component: () => import('@/views/ScriptDubView.vue'),
    meta: { title: '剧本配音', icon: 'file' }
  },
  {
    path: '/market',
    name: 'market',
    component: () => import('@/views/VoiceMarketView.vue'),
    meta: { title: '音色市场', icon: 'cart' }
  },
  {
    path: '/settings',
    name: 'settings',
    component: () => import('@/views/SettingsView.vue'),
    meta: { title: '设置', icon: 'settings' }
  },
  {
    path: '/help',
    name: 'help',
    component: () => import('@/views/HelpView.vue'),
    meta: { title: '帮助', icon: 'help' }
  },
  // ========== Admin Routes ==========
  {
    path: '/admin/login',
    name: 'adminLogin',
    component: () => import('@/views/LoginView.vue'),
    props: { mode: 'admin' },
    meta: { admin: true, layout: 'blank' }
  },
  {
    path: '/admin',
    redirect: '/admin/dashboard',
    meta: { admin: true }
  },
  {
    path: '/admin/dashboard',
    name: 'adminDashboard',
    component: () => import('@/views/admin/DashboardView.vue'),
    meta: { admin: true, title: '仪表盘' }
  },
  {
    path: '/admin/users',
    name: 'adminUsers',
    component: () => import('@/views/admin/UserManageView.vue'),
    meta: { admin: true, title: '用户管理' }
  },
  {
    path: '/admin/voices',
    name: 'adminVoices',
    component: () => import('@/views/admin/VoiceManageView.vue'),
    meta: { admin: true, title: '音色管理' }
  },
  {
    path: '/admin/logs',
    name: 'adminLogs',
    component: () => import('@/views/admin/LogsView.vue'),
    meta: { admin: true, title: '操作日志' }
  },
]

const router = createRouter({
  history: createWebHistory(),
  routes,
})

router.beforeEach((to, from, next) => {
  const authToken = localStorage.getItem('authToken')
  const adminToken = localStorage.getItem('adminToken')

  // 普通用户已登录访问 /login -> 重定向到 dashboard
  if (authToken && to.path === '/login') {
    next('/dashboard')
    return
  }

  // 管理员路由守卫
  if (to.meta?.admin && to.path !== '/admin/login') {
    if (!adminToken) {
      next('/admin/login')
      return
    }
  }

  // 管理员已登录访问 /admin/login -> 重定向到 admin dashboard
  if (adminToken && to.path === '/admin/login') {
    next('/admin/dashboard')
    return
  }

  next()
})

export default router
