/**
 * Service Layer 配置
 * 
 * USE_MOCK = true  → 使用 Mock 模拟数据（开发阶段）
 * USE_MOCK = false → 调用真实后端 API
 * 
 * 切换到真实 API 时只需修改此文件，无需改动任何业务组件代码。
 */

export const USE_MOCK = false

/** 真实 API 基础地址 */
export const API_BASE_URL = '/api/v1'

/** 请求超时时间 (ms) */
export const REQUEST_TIMEOUT = 15000

/**
 * 模拟网络延迟范围 (ms)，仅在 USE_MOCK = true 时生效
 * [最小值, 最大值]，设为 [0, 0] 则无延迟
 */
export const MOCK_DELAY = [200, 600]
