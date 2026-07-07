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
  return post(`/share/publish/${id}`)
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
    voice_id: data.voice_id,
    text: data.text,
    speed: data.speed,
    volume: data.volume,
    pitch: data.pitch,
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
  const voices = await get('/voice/presets')
  const ttsVoices = [
    { value: 1, label: '晓晓（女声）' },
    { value: 2, label: '云希（男声）' },
    { value: 3, label: '晓伊（女声）' },
    { value: 4, label: '云健（男声）' },
    { value: 5, label: '云霞（女声）' },
    { value: 6, label: '云扬（男声）' },
    { value: 7, label: '晓北（东北话）' },
  ]
  return ttsVoices
}

// ============================================================
//  工作台统计
// ============================================================

export async function getDashboardStats() {
  try {
    const [voiceList, synthList] = await Promise.all([
      get('/voice/list', { page: 1, page_size: 1 }),
      get('/tts/history', { page: 1, page_size: 1 }),
    ])
    return {
      voiceCount: voiceList?.pagination?.total || 0,
      synthesisCount: synthList?.pagination?.total || 0,
      scriptCount: 0,
      downloadCount: 0,
    }
  } catch {
    return { voiceCount: 0, synthesisCount: 0, scriptCount: 0, downloadCount: 0 }
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
    return { items: result.items, total: p.total || 0, page: p.page || 1, pageSize: p.pageSize || 10 }
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
  }
}

function normalizeSynthesis(s) {
  return {
    id: s.id || s.record_id,
    text: s.text || s.input_text,
    voice: s.voice_name || '',
    params: '',
    status: 'success',
    date: s.created_at || '',
  }
}

// ============================================================
//  常量映射
// ============================================================

export { statusMap, sourceMap } from '../types'
