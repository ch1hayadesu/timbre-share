import { ref, computed } from 'vue'

const token = ref(localStorage.getItem('authToken'))
const adminToken = ref(localStorage.getItem('adminToken'))
const isAdmin = ref(localStorage.getItem('isAdmin') === 'true')
const adminName = ref(localStorage.getItem('adminName') || '')
const showLogin = ref(false)
let pendingAction = null

export function useAuth() {
  const isLoggedIn = computed(() => !!token.value)
  const isAdminLoggedIn = computed(() => !!adminToken.value)

  // 普通用户
  function setToken(t) {
    token.value = t
    localStorage.setItem('authToken', t)
  }

  function clearToken() {
    token.value = null
    localStorage.removeItem('authToken')
  }

  // 管理员
  function setAdminToken(t, name) {
    adminToken.value = t
    isAdmin.value = true
    adminName.value = name || ''
    localStorage.setItem('adminToken', t)
    localStorage.setItem('isAdmin', 'true')
    if (name) localStorage.setItem('adminName', name)
  }

  function clearAdminToken() {
    adminToken.value = null
    isAdmin.value = false
    adminName.value = ''
    localStorage.removeItem('adminToken')
    localStorage.removeItem('isAdmin')
    localStorage.removeItem('adminName')
  }

  function requireAuth(action) {
    if (isLoggedIn.value) return true
    pendingAction = action
    showLogin.value = true
    return false
  }

  function onLoginSuccess() {
    showLogin.value = false
    if (pendingAction) {
      const fn = pendingAction
      pendingAction = null
      fn()
    }
  }

  function cancelLogin() {
    showLogin.value = false
    pendingAction = null
  }

  return {
    isLoggedIn, isAdminLoggedIn, isAdmin, adminName,
    token, adminToken,
    showLogin, setToken, clearToken,
    setAdminToken, clearAdminToken,
    requireAuth, onLoginSuccess, cancelLogin,
  }
}
