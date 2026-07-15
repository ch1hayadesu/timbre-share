/**
 * 运维管理后台 API 服务
 *
 * 注意：所有路径都使用相对路径（不带 /api/v1 前缀），
 * 因为 http.js 中的 adminPost/adminGet 等函数会自动添加 API_BASE_URL。
 */
import { adminGet, adminPost, adminPut, adminDel } from './http.js'

// ========== Auth ==========

export const adminLogin = (username, password) =>
  adminPost('/admin/login', { username, password })

export const adminLogout = () =>
  adminPost('/admin/logout')

// ========== Users ==========

export const getAdminUsers = (params = {}) =>
  adminGet('/admin/users', params)

export const updateUserStatus = (userId, isDisabled) =>
  adminPut(`/admin/users/${userId}/status`, { is_disabled: isDisabled })

export const deleteAdminUser = (userId) =>
  adminDel(`/admin/users/${userId}`)

// ========== Voices ==========

export const getAdminVoices = (params = {}) =>
  adminGet('/admin/voices', params)

export const updateVoiceStatus = (voiceId, adminStatus) =>
  adminPut(`/admin/voices/${voiceId}/status`, { admin_status: adminStatus })

export const deleteAdminVoice = (voiceId) =>
  adminDel(`/admin/voices/${voiceId}`)

export const toggleVoiceRecommend = (voiceId, isRecommended) =>
  adminPut(`/admin/voices/${voiceId}/recommend`, { is_recommended: isRecommended })

export const toggleVoicePopular = (voiceId, isPopular) =>
  adminPut(`/admin/voices/${voiceId}/popular`, { is_popular: isPopular })

// ========== Stats ==========

export const getStatsOverview = () =>
  adminGet('/admin/stats/overview')

export const getStatsTrends = (days = 30) =>
  adminGet('/admin/stats/trends', { days })

export const getStatsRankings = () =>
  adminGet('/admin/stats/rankings')

// ========== Logs ==========

export const getOperationLogs = (params = {}) =>
  adminGet('/admin/logs/operations', params)

export const getErrorLogs = (params = {}) =>
  adminGet('/admin/logs/errors', params)
