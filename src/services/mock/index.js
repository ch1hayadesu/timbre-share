/**
 * Mock 数据存储（模块级单例，模拟后端数据库）
 * 
 * 所有修改操作直接修改此内存数据，刷新页面后恢复初始状态。
 */
import { MOCK_DELAY } from '../config'

// ---- 初始数据 ----

const initialVoices = [
  { id: 1, name: '温柔女声', source: 'cloned', status: 'ready', mode: '即时克隆', date: '2026-07-05', downloads: 0 },
  { id: 2, name: '沉稳男声', source: 'cloned', status: 'ready', mode: '深度克隆', date: '2026-07-04', downloads: 0 },
  { id: 3, name: '活泼少女', source: 'shared', status: 'ready', mode: '下载', date: '2026-07-03', downloads: 0 },
  { id: 4, name: '磁性大叔', source: 'cloned', status: 'shared', mode: '即时克隆', date: '2026-07-02', downloads: 23 },
  { id: 5, name: '知性女声', source: 'preset', status: 'ready', mode: '系统预设', date: '2026-07-01', downloads: 0 },
  { id: 6, name: '清亮少年', source: 'cloned', status: 'processing', mode: '深度克隆', date: '2026-07-06', downloads: 0 },
  { id: 7, name: '甜美萝莉', source: 'shared', status: 'ready', mode: '下载', date: '2026-06-28', downloads: 0 },
  { id: 8, name: '沧桑老者', source: 'cloned', status: 'failed', mode: '深度克隆', date: '2026-06-25', downloads: 0 },
  { id: 9, name: '专业播音', source: 'preset', status: 'ready', mode: '系统预设', date: '2026-06-20', downloads: 0 },
  { id: 10, name: '邻家男孩', source: 'cloned', status: 'ready', mode: '即时克隆', date: '2026-07-04', downloads: 0 },
  { id: 11, name: '御姐音', source: 'shared', status: 'ready', mode: '下载', date: '2026-07-01', downloads: 0 },
  { id: 12, name: '正太音', source: 'cloned', status: 'shared', mode: '深度克隆', date: '2026-06-30', downloads: 15 },
]

const initialMarketVoices = [
  { id: 101, name: '温柔女声', author: '小**', downloads: 234, date: '2026-07-05' },
  { id: 102, name: '磁性大叔', author: '张**', downloads: 189, date: '2026-07-04' },
  { id: 103, name: '活泼少女', author: '李**', downloads: 156, date: '2026-07-03' },
  { id: 104, name: '御姐音', author: '王**', downloads: 128, date: '2026-07-02' },
  { id: 105, name: '专业播音', author: '陈**', downloads: 312, date: '2026-07-01' },
  { id: 106, name: '正太音', author: '刘**', downloads: 98, date: '2026-06-30' },
]

const initialSynthesis = [
  { id: 1, text: '大家好，欢迎来到今天的节目...', voice: '温柔女声', params: '语速1.0x 音量80% 音调0', status: 'success', date: '2026-07-05 14:30' },
  { id: 2, text: '今天天气真好，我们一起去...', voice: '沉稳男声', params: '语速1.2x 音量90% 音调+2', status: 'success', date: '2026-07-05 10:15' },
  { id: 3, text: '产品功能介绍：本产品采用...', voice: '知性女声', params: '语速0.8x 音量75% 音调-1', status: 'success', date: '2026-07-04 16:45' },
  { id: 4, text: '温馨提示：请注意天气变化...', voice: '磁性大叔', params: '语速1.0x 音量85% 音调0', status: 'success', date: '2026-07-04 09:20' },
  { id: 5, text: '这是一条测试文本，用于验证...', voice: '活泼少女', params: '语速1.5x 音量70% 音调+3', status: 'failed', date: '2026-07-03 11:00' },
]

const initialTTSVoiceOptions = [
  { value: 1, label: '温柔女声' },
  { value: 2, label: '沉稳男声' },
  { value: 3, label: '活泼少女' },
  { value: 4, label: '磁性大叔' },
  { value: 5, label: '知性女声' },
]

// ---- 运行时的可变数据（深拷贝初始值） ----

let voices = JSON.parse(JSON.stringify(initialVoices))
let marketVoices = JSON.parse(JSON.stringify(initialMarketVoices))
let synthesisRecords = JSON.parse(JSON.stringify(initialSynthesis))
let ttsVoiceOptions = JSON.parse(JSON.stringify(initialTTSVoiceOptions))

let voiceIdCounter = voices.length
let marketIdCounter = marketVoices.length
let synthesisIdCounter = synthesisRecords.length

// ---- 工具函数 ----

/** 模拟网络延迟 */
function delay() {
  const [min, max] = MOCK_DELAY
  const ms = Math.floor(Math.random() * (max - min + 1)) + min
  return new Promise(resolve => setTimeout(resolve, ms))
}

/** 格式化日期 */
function today() {
  return new Date().toISOString().split('T')[0]
}

/** 格式化日期时间 */
function now() {
  const d = new Date()
  const pad = n => String(n).padStart(2, '0')
  return `${d.getFullYear()}-${pad(d.getMonth() + 1)}-${pad(d.getDate())} ${pad(d.getHours())}:${pad(d.getMinutes())}`
}

/** 深拷贝 */
function clone(data) {
  return JSON.parse(JSON.stringify(data))
}

// ---- 重置函数（用于测试） ----
export function resetMockData() {
  voices = clone(initialVoices)
  marketVoices = clone(initialMarketVoices)
  synthesisRecords = clone(initialSynthesis)
  ttsVoiceOptions = clone(initialTTSVoiceOptions)
  voiceIdCounter = voices.length
  marketIdCounter = marketVoices.length
  synthesisIdCounter = synthesisRecords.length
}

// ============================================================
//  音色 CRUD (My Voices)
// ============================================================

/**
 * 获取我的音色列表
 * @param {object} params
 * @param {string} [params.keyword] - 搜索关键词
 * @param {string} [params.source]  - 来源筛选 (cloned|shared|preset)
 * @param {string} [params.status]  - 状态筛选 (ready|processing|failed|shared)
 * @param {number} [params.page=1]
 * @param {number} [params.pageSize=10]
 * @returns {Promise<{items: Voice[], total: number, page: number, pageSize: number}>}
 */
export async function getVoiceList(params = {}) {
  await delay()
  const { keyword = '', source = '', status = '', page = 1, pageSize = 10 } = params

  let filtered = clone(voices)

  if (keyword) {
    filtered = filtered.filter(v => v.name.includes(keyword))
  }
  if (source) {
    filtered = filtered.filter(v => v.source === source)
  }
  if (status) {
    filtered = filtered.filter(v => v.status === status)
  }

  const total = filtered.length
  const start = (page - 1) * pageSize
  const items = filtered.slice(start, start + pageSize)

  return { items, total, page, pageSize }
}

/**
 * 获取单个音色详情
 * @param {number} id
 * @returns {Promise<Voice|null>}
 */
export async function getVoiceDetail(id) {
  await delay()
  const voice = voices.find(v => v.id === id)
  return voice ? clone(voice) : null
}

/**
 * 创建新音色（克隆结果保存）
 * @param {object} data
 * @param {string} data.name   - 音色名称
 * @param {string} data.source - 来源 (cloned|shared|preset)
 * @param {string} data.mode   - 模式
 * @returns {Promise<Voice>}
 */
export async function createVoice(data) {
  await delay()
  const voice = {
    id: ++voiceIdCounter,
    name: data.name,
    source: data.source || 'cloned',
    status: 'ready',
    mode: data.mode || '即时克隆',
    date: today(),
    downloads: 0,
  }
  voices.unshift(voice)
  return clone(voice)
}

/**
 * 更新音色信息
 * @param {number} id
 * @param {object}  data - 要更新的字段
 * @returns {Promise<Voice|null>}
 */
export async function updateVoice(id, data) {
  await delay()
  const voice = voices.find(v => v.id === id)
  if (!voice) return null
  Object.assign(voice, data)
  return clone(voice)
}

/**
 * 删除音色
 * @param {number} id
 * @returns {Promise<boolean>}
 */
export async function deleteVoice(id) {
  await delay()
  const idx = voices.findIndex(v => v.id === id)
  if (idx === -1) return false
  voices.splice(idx, 1)
  return true
}

/**
 * 分享音色到平台
 * @param {number} id
 * @returns {Promise<Voice|null>}
 */
export async function shareVoice(id) {
  await delay()
  const voice = voices.find(v => v.id === id)
  if (!voice) return null
  voice.status = 'shared'
  return clone(voice)
}

// ============================================================
//  音色市场 (Market)
// ============================================================

/**
 * 获取音色市场列表
 * @param {object} params
 * @param {string} [params.keyword] - 搜索关键词
 * @param {'newest'|'popular'} [params.sort='newest']
 * @param {number} [params.page=1]
 * @param {number} [params.pageSize=12]
 * @returns {Promise<{items: MarketVoice[], total: number, page: number, pageSize: number}>}
 */
export async function getMarketVoiceList(params = {}) {
  await delay()
  const { keyword = '', sort = 'newest', page = 1, pageSize = 12 } = params

  let filtered = clone(marketVoices)

  if (keyword) {
    filtered = filtered.filter(v => v.name.includes(keyword))
  }

  if (sort === 'popular') {
    filtered.sort((a, b) => b.downloads - a.downloads)
  }

  const total = filtered.length
  const start = (page - 1) * pageSize
  const items = filtered.slice(start, start + pageSize)

  return { items, total, page, pageSize }
}

/**
 * 从市场下载音色到我的语音库
 * @param {number} marketVoiceId
 * @returns {Promise<Voice>}
 */
export async function downloadMarketVoice(marketVoiceId) {
  await delay()
  const marketVoice = marketVoices.find(v => v.id === marketVoiceId)
  if (!marketVoice) throw new Error('音色不存在')

  // 增加下载计数
  marketVoice.downloads++

  // 添加到我的音色
  const voice = {
    id: ++voiceIdCounter,
    name: marketVoice.name,
    source: 'shared',
    status: 'ready',
    mode: '下载',
    date: today(),
    downloads: 0,
  }
  voices.push(voice)
  return clone(voice)
}

// ============================================================
//  合成记录 (Synthesis)
// ============================================================

/**
 * 获取合成记录列表
 * @param {object} params
 * @param {number} [params.page=1]
 * @param {number} [params.pageSize=10]
 * @returns {Promise<{items: SynthesisRecord[], total: number, page: number, pageSize: number}>}
 */
export async function getSynthesisList(params = {}) {
  await delay()
  const { page = 1, pageSize = 10 } = params

  const records = clone(synthesisRecords)
  const total = records.length
  const start = (page - 1) * pageSize
  const items = records.slice(start, start + pageSize)

  return { items, total, page, pageSize }
}

/**
 * 创建合成记录
 * @param {object} data
 * @param {string} data.text   - 合成文本
 * @param {string} data.voice  - 使用音色
 * @param {string} data.params - 合成参数
 * @param {string} data.status - 状态 (success|failed)
 * @returns {Promise<SynthesisRecord>}
 */
export async function createSynthesis(data) {
  await delay()
  const record = {
    id: ++synthesisIdCounter,
    text: data.text,
    voice: data.voice,
    params: data.params,
    status: data.status || 'success',
    date: now(),
  }
  synthesisRecords.unshift(record)
  return clone(record)
}

// ============================================================
//  TTS 音色选项
// ============================================================

/**
 * 获取可用的 TTS 音色选项
 * @returns {Promise<TTSVoiceOption[]>}
 */
export async function getTTSVoiceOptions() {
  await delay()
  return clone(ttsVoiceOptions)
}

// ============================================================
//  工作台统计
// ============================================================

/**
 * 获取工作台统计数据
 * @returns {Promise<{voiceCount: number, synthesisCount: number, scriptCount: number, downloadCount: number}>}
 */
export async function getDashboardStats() {
  await delay()
  return {
    voiceCount: voices.length,
    synthesisCount: synthesisRecords.filter(r => r.status === 'success').length,
    scriptCount: 8,
    downloadCount: voices.filter(v => v.source === 'shared').length,
  }
}

// ============================================================
//  常量映射
// ============================================================

export { statusMap, sourceMap } from '../types'
