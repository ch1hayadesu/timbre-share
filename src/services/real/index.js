/**
 * 真实 API 实现层
 * 
 * 接口签名与 Mock 层完全一致，切换到 USE_MOCK = false 后生效。
 * 
 * 目前为占位实现：所有方法调用真实 HTTP 请求，
 * 后端接口未就绪时会自然抛出网络错误，可在上层统一处理。
 */

import { get, post, put, del } from '../http'

// ============================================================
//  音色 CRUD
// ============================================================

export async function getVoiceList(params = {}) {
  return get('/voices', params)
}

export async function getVoiceDetail(id) {
  return get(`/voices/${id}`)
}

export async function createVoice(data) {
  return post('/voices', data)
}

export async function updateVoice(id, data) {
  return put(`/voices/${id}`, data)
}

export async function deleteVoice(id) {
  return del(`/voices/${id}`)
}

export async function shareVoice(id) {
  return post(`/voices/${id}/share`)
}

// ============================================================
//  音色市场
// ============================================================

export async function getMarketVoiceList(params = {}) {
  return get('/market/voices', params)
}

export async function downloadMarketVoice(marketVoiceId) {
  return post(`/market/voices/${marketVoiceId}/download`)
}

// ============================================================
//  合成记录
// ============================================================

export async function getSynthesisList(params = {}) {
  return get('/synthesis', params)
}

export async function createSynthesis(data) {
  return post('/synthesis', data)
}

// ============================================================
//  TTS 音色选项
// ============================================================

export async function getTTSVoiceOptions() {
  return get('/voices/tts-options')
}

// ============================================================
//  工作台统计
// ============================================================

export async function getDashboardStats() {
  return get('/dashboard/stats')
}

// ============================================================
//  常量映射
// ============================================================

export { statusMap, sourceMap } from '../types'
