import { get, post, postForm, put, del } from '../http'

// ============================================================
//  音色 CRUD
// ============================================================

const STATUS_MAP = { all: undefined, ready: 1, processing: 0, failed: -1, shared: 1 }

export async function getVoiceList(params = {}) {
  const query = {
    page: params.page,
    page_size: params.pageSize,
    keyword: params.keyword,
    source: params.source === 'all' ? undefined : params.source,
    status: STATUS_MAP[params.status],
  }
  Object.keys(query).forEach(k => { if (query[k] === undefined) delete query[k] })
  const result = await get('/voice/list', query)
  if (result && result.items) {
    const p = result.pagination || {}
    return {
      items: result.items.map(normalizeVoice),
      total: p.total || 0,
      page: p.page || 1,
      pageSize: p.pageSize || 10,
    }
  }
  return { items: [], total: 0, page: 1, pageSize: 10 }
}

export async function getVoiceDetail(id) {
  const voice = await get(`/voice/detail/${id}`)
  return voice ? normalizeVoice(voice) : null
}

export async function createVoice(data) {
  return post('/voice/clone', data)
}

export async function updateVoice(id, data) {
  return put(`/voice/update/${id}`, data)
}

export async function deleteVoice(id) {
  return del(`/voice/delete/${id}`)
}

export async function shareVoice(id) {
  return post(`/share/publish/${id}`, {})
}

export async function downloadVoiceModel(voiceId) {
  const token = localStorage.getItem('token')
  const resp = await fetch(`/api/v1/voice/download-model/${voiceId}`, {
    headers: { Authorization: `Bearer ${token}` },
  })
  if (!resp.ok) {
    const errData = await resp.json().catch(() => ({ message: '下载失败' }))
    throw new Error(errData.message || errData.detail || '下载失败')
  }
  const blob = await resp.blob()
  const disposition = resp.headers.get('Content-Disposition') || ''
  const match = disposition.match(/filename="?(.+?)"?$/i)
  const filename = match ? match[1] : `voice_model_${voiceId}.zip`
  const url = URL.createObjectURL(blob)
  const a = document.createElement('a')
  a.href = url
  a.download = filename
  document.body.appendChild(a)
  a.click()
  document.body.removeChild(a)
  URL.revokeObjectURL(url)
}

export async function getCloneHistory(params = {}) {
  const query = { page: params.page || 1, page_size: params.pageSize || 10 }
  const result = await get('/voice/clone-history', query)
  if (result && result.items) {
    const p = result.pagination || {}
    return {
      items: result.items.map(normalizeCloneHistory),
      total: p.total || 0,
      page: p.page || 1,
      pageSize: p.pageSize || 10,
    }
  }
  return { items: [], total: 0, page: 1, pageSize: 10 }
}

export async function downloadCloneHistoryModel(historyId) {
  const token = localStorage.getItem('token')
  const resp = await fetch(`/api/v1/voice/clone-history/download-model/${historyId}`, {
    headers: { Authorization: `Bearer ${token}` },
  })
  if (!resp.ok) {
    const errData = await resp.json().catch(() => ({ message: '下载失败' }))
    throw new Error(errData.message || errData.detail || '下载失败')
  }
  const blob = await resp.blob()
  const disposition = resp.headers.get('Content-Disposition') || ''
  const match = disposition.match(/filename="?(.+?)"?$/i)
  const filename = match ? match[1] : `voice_model_${historyId}.zip`
  const url = URL.createObjectURL(blob)
  const a = document.createElement('a')
  a.href = url
  a.download = filename
  document.body.appendChild(a)
  a.click()
  document.body.removeChild(a)
  URL.revokeObjectURL(url)
}

export async function addCloneHistoryToMyVoices(historyId) {
  return post(`/voice/clone-history/${historyId}/add-to-my-voices`)
}

// ============================================================
//  音色市场
// ============================================================

export async function getMarketVoiceList(params = {}) {
  const query = {
    keyword: params.keyword,
    page: params.page,
    page_size: params.pageSize,
  }
  Object.keys(query).forEach(k => { if (query[k] === undefined) delete query[k] })
  const result = await get('/share/public', query)
  if (result && result.items) {
    const p = result.pagination || {}
    return {
      items: result.items.map(normalizeMarketVoice),
      total: p.total || 0,
      page: p.page || 1,
      pageSize: p.pageSize || 12,
    }
  }
  return { items: [], total: 0, page: 1, pageSize: 12 }
}

export async function downloadMarketVoice(marketVoiceId) {
  return post(`/share/download/${marketVoiceId}`)
}

export function getMarketVoicePreviewUrl(shareId) {
  return `/api/v1/share/preview/${shareId}`
}

// ============================================================
//  TTS 合成
// ============================================================

export async function createSynthesis(data) {
  return post('/tts/synthesize', {
    voice_id: data.voiceId || data.voice_id,
    text: data.text,
    speed: data.speed || 1.0,
    volume: data.volume || 80,
    pitch: data.pitch || 0,
    model: data.model || 'edge-tts',
  })
}

export async function getTTSRecord(recordId) {
  const result = await get(`/tts/record/${recordId}`)
  return result
}

export async function pollTask(taskId) {
  return getTTSRecord(taskId)
}

export async function getSynthesisList(params = {}) {
  const query = {
    page: params.page,
    page_size: params.pageSize,
  }
  Object.keys(query).forEach(k => { if (query[k] === undefined) delete query[k] })
  const result = await get('/tts/history', query)
  if (result && result.items) {
    const p = result.pagination || {}
    return {
      items: result.items.map(normalizeSynthesis),
      total: p.total || 0,
      page: p.page || 1,
      pageSize: p.pageSize || 10,
    }
  }
  return { items: [], total: 0, page: 1, pageSize: 10 }
}

// ============================================================
//  TTS 音色选项
// ============================================================

export async function getTTSVoiceOptions() {
  const [presetsResult, userVoicesResult] = await Promise.all([
    get('/voice/presets'),
    get('/voice/list', { page: 1, page_size: 50, status: 1 }),
  ])
  const presets = (presetsResult?.data || presetsResult || []).map(v => ({
    value: v.voice_id,
    label: v.voice_name,
    category: 'preset',
  }))
  let userVoices = []
  if (userVoicesResult && userVoicesResult.items) {
    userVoices = userVoicesResult.items
      .filter(v => v.source !== 'preset')
      .map(v => ({
        value: v.voice_id,
        label: v.voice_name,
        category: 'user',
      }))
  }
  return [...presets, ...userVoices]
}

// ============================================================
//  工作台统计
// ============================================================

export async function getDashboardStats() {
  const [voiceList, synthList, dubList] = await Promise.all([
    get('/voice/list', { page: 1, page_size: 1 }),
    get('/tts/history', { page: 1, page_size: 1 }),
    get('/script-dub/list', { page: 1, page_size: 1 }),
  ])
  return {
    voiceCount: voiceList?.pagination?.total || 0,
    synthesisCount: synthList?.pagination?.total || 0,
    scriptCount: dubList?.pagination?.total || 0,
    downloadCount: 0,
  }
}

// ============================================================
//  用户认证
// ============================================================

export async function sendCode(phone) {
  return post('/user/send-code', { phone })
}

export async function login(phone, code) {
  const result = await post('/user/login', { phone, code })
  return { token: result.token, user: result.user }
}

export async function getTTSModels() {
  return get('/tts/models')
}

// ============================================================
//  健康检查
// ============================================================

// ============================================================
//  剧本配音
// ============================================================

export async function createScriptDubTask(data) {
  return post('/script-dub/create', data)
}

export async function getScriptDubList(params = {}) {
  const query = { page: params.page, page_size: params.pageSize }
  Object.keys(query).forEach(k => { if (query[k] === undefined) delete query[k] })
  const result = await get('/script-dub/list', query)
  if (result && result.items) {
    const p = result.pagination || {}
    return {
      items: result.items.map(normalizeScriptDub),
      total: p.total || 0,
      page: p.page || 1,
      pageSize: p.pageSize || 10,
    }
  }
  return { items: [], total: 0, page: 1, pageSize: 10 }
}

export async function getScriptDubDetail(taskId) {
  return get(`/script-dub/detail/${taskId}`)
}

export async function getHealth() {
  return get('/health')
}

// ============================================================
//  内部字段映射
// ============================================================

function normalizeMarketVoice(s) {
  return {
    id: s.share_id,
    name: s.voice_name,
    author: '用户',
    downloads: s.download_count || 0,
    date: s.created_at ? s.created_at.split('T')[0] : '',
    share_id: s.share_id,
    voice_id: s.voice_id,
    sample_url: s.sample_url,
    tags: s.tags,
  }
}

function normalizeVoice(v) {
  return {
    id: v.voice_id,
    name: v.voice_name,
    source: v.source,
    status: v.status === 1 ? 'ready' : v.status === 0 ? 'processing' : v.status === -1 ? 'failed' : 'ready',
    mode: v.clone_mode === 1 ? '深度克隆' : '即时克隆',
    date: v.created_at ? v.created_at.split('T')[0] : '',
    downloads: 0,
    voice_id: v.voice_id,
    voice_name: v.voice_name,
    raw_audio_url: v.raw_audio_url,
    sample_url: v.sample_url,
    error_message: v.error_message,
    clone_mode: v.clone_mode,
    tts_model: v.tts_model,
  }
}

function normalizeCloneHistory(h) {
  return {
    id: h.id,               // clone_history 表主键
    historyId: h.id,        // 克隆历史记录ID，用于下载模型
    voiceId: h.voice_id,    // 原音色ID（音色删除后为null）
    name: h.voice_name,
    status: h.status === 1 ? 'ready' : h.status === 0 ? 'processing' : h.status === -1 ? 'failed' : 'ready',
    mode: h.clone_mode === 1 ? '深度克隆' : '即时克隆',
    date: h.created_at ? h.created_at.split('T')[0] : '',
    sample_url: h.sample_url,
    error_message: h.error_message,
    clone_mode: h.clone_mode,
    tts_model: h.tts_model,
  }
}

function normalizeSynthesis(s) {
  return {
    id: s.id || s.record_id,
    text: s.text || s.input_text,
    voice: s.voice_name || '',
    params: `speed=${s.speed || 1.0} volume=${s.volume || 80} pitch=${s.pitch || 0}`,
    status: s.status === 1 ? 'success' : s.status === 0 ? 'processing' : 'failed',
    date: s.created_at || '',
    audio_url: s.audio_url,
    record_id: s.record_id,
    type: 'tts',
  }
}

function normalizeScriptDub(d) {
  return {
    id: d.id || d.task_id,
    scriptName: d.script_name || '未命名剧本',
    roleCount: d.role_count || 0,
    status: d.status === 1 ? 'success' : d.status === 0 ? 'processing' : 'failed',
    date: d.created_at || '',
    outputUrl: d.output_url || '',
    scriptText: d.script_text || '',
    voiceMapping: d.voice_mapping || null,
  }
}

// ============================================================
//  常量映射
// ============================================================

export { statusMap, sourceMap } from '../types'
