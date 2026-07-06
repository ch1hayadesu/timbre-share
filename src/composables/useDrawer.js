import { reactive } from 'vue'

/**
 * 全局 Drawer 管理
 */
const state = reactive({
  visible: false,
  title: '',
  content: '',
})

export function useDrawer() {
  const showDrawer = (title, content) => {
    state.visible = true
    state.title = title
    state.content = content
  }

  const closeDrawer = () => {
    state.visible = false
    state.content = ''
  }

  return { drawerState: state, showDrawer, closeDrawer }
}
