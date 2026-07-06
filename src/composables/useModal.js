import { ref, reactive } from 'vue'

/**
 * 全局 Modal 管理
 */
const modalState = reactive({
  visible: false,
  title: '',
  content: '',
  confirmText: '确认',
  danger: false,
  onConfirm: null,
})

export function useModal() {
  const showModal = (title, content, onConfirm, confirmText = '确认', danger = false) => {
    modalState.visible = true
    modalState.title = title
    modalState.content = content
    modalState.confirmText = confirmText
    modalState.danger = danger
    modalState.onConfirm = onConfirm
  }

  const closeModal = () => {
    modalState.visible = false
    modalState.onConfirm = null
  }

  const handleConfirm = () => {
    if (modalState.onConfirm) modalState.onConfirm()
    closeModal()
  }

  return { modalState, showModal, closeModal, handleConfirm }
}
