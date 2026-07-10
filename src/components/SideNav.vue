<template>
  <aside class="sidenav" :class="{ open: isOpen }">
    <div class="sidenav-section">
      <div class="sidenav-label">主要功能</div>
      <router-link v-for="item in mainItems" :key="item.path" :to="item.path"
        class="sidenav-item" active-class="active">
        <component :is="item.icon" class="sidenav-icon" />
        <span>{{ item.label }}</span>
      </router-link>
    </div>
    <div class="sidenav-section">
      <div class="sidenav-label">其他</div>
      <router-link to="/settings" class="sidenav-item" active-class="active">
        <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" class="sidenav-icon">
          <circle cx="12" cy="12" r="3" />
          <path d="M19.4 15a1.65 1.65 0 0 0 .33 1.82l.06.06a2 2 0 0 1 0 2.83 2 2 0 0 1-2.83 0l-.06-.06a1.65 1.65 0 0 0-1.82-.33 1.65 1.65 0 0 0-1 1.51V21a2 2 0 0 1-2 2 2 2 0 0 1-2-2v-.09A1.65 1.65 0 0 0 9 19.4a1.65 1.65 0 0 0-1.82.33l-.06.06a2 2 0 0 1-2.83 0 2 2 0 0 1 0-2.83l.06-.06A1.65 1.65 0 0 0 4.68 15a1.65 1.65 0 0 0-1.51-1H3a2 2 0 0 1-2-2 2 2 0 0 1 2-2h.09A1.65 1.65 0 0 0 4.6 9a1.65 1.65 0 0 0-.33-1.82l-.06-.06a2 2 0 0 1 0-2.83 2 2 0 0 1 2.83 0l.06.06A1.65 1.65 0 0 0 9 4.68a1.65 1.65 0 0 0 1-1.51V3a2 2 0 0 1 2-2 2 2 0 0 1 2 2v.09a1.65 1.65 0 0 0 1 1.51 1.65 1.65 0 0 0 1.82-.33l.06-.06a2 2 0 0 1 2.83 0 2 2 0 0 1 0 2.83l-.06.06A1.65 1.65 0 0 0 19.4 9a1.65 1.65 0 0 0 1.51 1H21a2 2 0 0 1 2 2 2 2 0 0 1-2 2h-.09a1.65 1.65 0 0 0-1.51 1z" />
        </svg>
        <span>设置</span>
      </router-link>
      <router-link to="/help" class="sidenav-item" active-class="active">
        <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" class="sidenav-icon">
          <circle cx="12" cy="12" r="10" />
          <path d="M9.09 9a3 3 0 0 1 5.83 1c0 2-3 3-3 3" />
          <line x1="12" y1="17" x2="12.01" y2="17" />
        </svg>
        <span>帮助</span>
      </router-link>
      <div class="sidenav-item logout-btn" @click="handleLogout">
        <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" class="sidenav-icon">
          <path d="M9 21H5a2 2 0 0 1-2-2V5a2 2 0 0 1 2-2h4" />
          <polyline points="16 17 21 12 16 7" />
          <line x1="21" y1="12" x2="9" y2="12" />
        </svg>
        <span>退出登录</span>
      </div>
    </div>
  </aside>
</template>

<script setup>
import { h } from 'vue'
import { useRouter } from 'vue-router'

defineProps({
  isOpen: { type: Boolean, default: false }
})

const emit = defineEmits(['toast'])
const router = useRouter()

function handleLogout() {
  localStorage.removeItem('authToken')
  router.push('/login')
}

const HomeIcon = {
  render() {
    return h('svg', { viewBox: '0 0 24 24', fill: 'none', stroke: 'currentColor', 'stroke-width': '2' }, [
      h('path', { d: 'M3 9l9-7 9 7v11a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2z' }),
      h('polyline', { points: '9 22 9 12 15 12 15 22' })
    ])
  }
}

const MusicIcon = {
  render() {
    return h('svg', { viewBox: '0 0 24 24', fill: 'none', stroke: 'currentColor', 'stroke-width': '2' }, [
      h('path', { d: 'M9 18V5l12-2v13' }),
      h('circle', { cx: '6', cy: '18', r: '3' }),
      h('circle', { cx: '18', cy: '16', r: '3' })
    ])
  }
}

const MicIcon = {
  render() {
    return h('svg', { viewBox: '0 0 24 24', fill: 'none', stroke: 'currentColor', 'stroke-width': '2' }, [
      h('path', { d: 'M12 1a3 3 0 0 0-3 3v8a3 3 0 0 0 6 0V4a3 3 0 0 0-3-3z' }),
      h('path', { d: 'M19 10v2a7 7 0 0 1-14 0v-2' }),
      h('line', { x1: '12', y1: '19', x2: '12', y2: '23' })
    ])
  }
}

const VolumeIcon = {
  render() {
    return h('svg', { viewBox: '0 0 24 24', fill: 'none', stroke: 'currentColor', 'stroke-width': '2' }, [
      h('polygon', { points: '11 5 6 9 2 9 2 15 6 15 11 19 11 5' }),
      h('path', { d: 'M19.07 4.93a10 10 0 0 1 0 14.14M15.54 8.46a5 5 0 0 1 0 7.07' })
    ])
  }
}

const FileIcon = {
  render() {
    return h('svg', { viewBox: '0 0 24 24', fill: 'none', stroke: 'currentColor', 'stroke-width': '2' }, [
      h('path', { d: 'M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z' }),
      h('polyline', { points: '14 2 14 8 20 8' }),
      h('line', { x1: '16', y1: '13', x2: '8', y2: '13' }),
      h('line', { x1: '16', y1: '17', x2: '8', y2: '17' })
    ])
  }
}

const CartIcon = {
  render() {
    return h('svg', { viewBox: '0 0 24 24', fill: 'none', stroke: 'currentColor', 'stroke-width': '2' }, [
      h('circle', { cx: '9', cy: '21', r: '1' }),
      h('circle', { cx: '20', cy: '21', r: '1' }),
      h('path', { d: 'M1 1h4l2.68 13.39a2 2 0 0 0 2 1.61h9.72a2 2 0 0 0 2-1.61L23 6H6' })
    ])
  }
}

const ClockIcon = {
  render() {
    return h('svg', { viewBox: '0 0 24 24', fill: 'none', stroke: 'currentColor', 'stroke-width': '2' }, [
      h('circle', { cx: '12', cy: '12', r: '10' }),
      h('polyline', { points: '12 6 12 12 16 14' })
    ])
  }
}

const mainItems = [
  { path: '/', label: '工作台', icon: HomeIcon },
  { path: '/voices', label: '我的音色', icon: MusicIcon },
  { path: '/clone', label: '音色克隆', icon: MicIcon },
  { path: '/tts', label: 'TTS合成', icon: VolumeIcon },
  { path: '/script', label: '剧本配音', icon: FileIcon },
  { path: '/market', label: '音色市场', icon: CartIcon },
  { path: '/history', label: '历史/收藏', icon: ClockIcon },
]
</script>

<style scoped>
.sidenav {
  position: fixed;
  top: var(--topnav-h);
  left: 0;
  bottom: 0;
  width: var(--sidenav-w);
  background: var(--color-bg-container);
  border-right: 1px solid var(--color-border-light);
  padding: var(--space-4) var(--space-3);
  overflow-y: auto;
  z-index: 90;
  transition: transform var(--duration-base) var(--ease-out);
}

.sidenav-section {
  margin-bottom: var(--space-5);
}

.sidenav-label {
  padding: var(--space-2) var(--space-4);
  font-size: var(--font-size-xs);
  font-weight: 600;
  color: var(--color-text-disabled);
  text-transform: uppercase;
  letter-spacing: 0.5px;
}

.sidenav-item {
  display: flex;
  align-items: center;
  gap: var(--space-3);
  padding: 10px var(--space-4);
  border-radius: var(--radius-md);
  cursor: pointer;
  transition: all var(--duration-fast) var(--ease-out);
  font-size: var(--font-size-base);
  font-weight: 500;
  color: var(--color-text-body);
  margin-bottom: 2px;
  position: relative;
}

.sidenav-item:hover {
  background: var(--color-bg-hover);
}

.sidenav-item.active {
  background: var(--color-bg-selected);
  color: var(--color-primary-6);
}

.sidenav-item.active::before {
  content: '';
  position: absolute;
  left: 0;
  top: 50%;
  transform: translateY(-50%);
  width: 3px;
  height: 20px;
  background: var(--color-primary-6);
  border-radius: 0 3px 3px 0;
}

.sidenav-icon {
  width: 20px;
  height: 20px;
  flex-shrink: 0;
}

@media (max-width: 1279px) {
  .sidenav {
    transform: translateX(-100%);
  }
  .sidenav.open {
    transform: translateX(0);
  }
}
</style>
