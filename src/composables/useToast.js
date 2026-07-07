import { reactive } from 'vue'

/**
 * 全局 Toast 管理
 */
const state = reactive({
  toasts: []
})

let toastId = 0

export function useToast() {
  const showToast = (type, message, duration = 3000) => {
    if (type === 'error') duration = 8000
    if (type === 'warning') duration = 5000

    const id = ++toastId
    state.toasts.push({ id, type, message })

    if (duration > 0) {
      setTimeout(() => {
        const idx = state.toasts.findIndex(t => t.id === id)
        if (idx > -1) state.toasts.splice(idx, 1)
      }, duration)
    }
  }

  const closeToast = (id) => {
    const idx = state.toasts.findIndex(t => t.id === id)
    if (idx > -1) state.toasts.splice(idx, 1)
  }

  return { toasts: state.toasts, showToast, closeToast }
}
