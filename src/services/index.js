/**
 * Service Layer 统一入口
 * 
 * 通过 config.js 中的 USE_MOCK 开关一键切换数据源：
 *   USE_MOCK = true  → 使用 mock/ 模块（内存模拟数据）
 *   USE_MOCK = false → 使用 real/ 模块（真实 HTTP API）
 * 
 * 业务组件只需 import 此文件的方法即可，无需关心底层实现。
 * 切换数据源时只需修改 config.js 中的一行代码。
 */

import { USE_MOCK } from './config'
import * as mockService from './mock'
import * as realService from './real'

const service = USE_MOCK ? mockService : realService

// 音色 CRUD
export const getVoiceList       = service.getVoiceList
export const getVoiceDetail     = service.getVoiceDetail
export const createVoice        = service.createVoice
export const updateVoice        = service.updateVoice
export const deleteVoice        = service.deleteVoice
export const shareVoice         = service.shareVoice

// 音色市场
export const getMarketVoiceList = service.getMarketVoiceList
export const downloadMarketVoice = service.downloadMarketVoice

// 合成记录
export const getSynthesisList   = service.getSynthesisList
export const createSynthesis    = service.createSynthesis

// TTS 音色选项
export const getTTSVoiceOptions = service.getTTSVoiceOptions

// 工作台统计
export const getDashboardStats  = service.getDashboardStats

// 常量映射
export { statusMap, sourceMap } from './types'

// 重新导出类型便于外部使用
export { USE_MOCK } from './config'
