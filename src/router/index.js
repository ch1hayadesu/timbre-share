import { createRouter, createWebHistory } from 'vue-router'

const routes = [
  {
    path: '/login',
    name: 'login',
    component: () => import('@/views/LoginView.vue'),
    meta: { title: '登录', guest: true }
  },
  {
    path: '/',
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
]

const router = createRouter({
  history: createWebHistory(),
  routes,
})

router.beforeEach((to, from, next) => {
  const token = localStorage.getItem('authToken')
  if (!token && !to.meta?.guest) {
    next('/login')
  } else if (token && to.path === '/login') {
    next('/')
  } else {
    next()
  }
})

export default router
