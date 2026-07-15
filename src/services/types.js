/**
 * Service Layer 类型定义
 * 
 * 所有 Service 方法的入参/出参类型在此统一定义，
 * Mock 实现和 Real 实现共用同一套接口签名。
 */

/**
 * @typedef {Object} Voice
 * @property {number}   id        - 音色 ID
 * @property {string}   name      - 音色名称
 * @property {'cloned'|'shared'|'preset'} source - 来源
 * @property {'ready'|'processing'|'failed'|'shared'} status - 状态
 * @property {string}   mode      - 模式（即时克隆 / 深度克隆 / 下载 / 系统预设）
 * @property {string}   date      - 创建日期 YYYY-MM-DD
 * @property {number}   downloads - 下载次数
 */

/**
 * @typedef {Object} MarketVoice
 * @property {number}  id        - 音色 ID
 * @property {string}  name      - 音色名称
 * @property {string}  author    - 分享者
 * @property {number}  downloads - 下载次数
 * @property {string}  date      - 发布日期 YYYY-MM-DD
 */

/**
 * @typedef {Object} SynthesisRecord
 * @property {number}  id     - 记录 ID
 * @property {string}  text   - 文本内容
 * @property {string}  voice  - 使用音色名称
 * @property {string}  params - 合成参数描述
 * @property {'success'|'failed'} status - 状态
 * @property {string}  date   - 合成时间 YYYY-MM-DD HH:mm
 * @property {'tts'|'script_dub'} type - 合成类型
 * @property {string}  audio_url - 音频文件 URL
 */

/**
 * @typedef {Object} ScriptDubRecord
 * @property {number}  id          - 记录 ID
 * @property {string}  scriptName  - 剧本名称
 * @property {number}  roleCount   - 角色数量
 * @property {'success'|'processing'|'failed'} status - 状态
 * @property {string}  date        - 配音时间 YYYY-MM-DD HH:mm
 * @property {string}  outputUrl   - 输出音频地址
 */

/**
 * @typedef {Object} TTSVoiceOption
 * @property {number} value - 音色 ID
 * @property {string} label - 音色名称
 */

/**
 * @typedef {Object} PaginatedResult
 * @template T
 * @property {T[]}    items      - 数据列表
 * @property {number} total      - 总数
 * @property {number} page       - 当前页码
 * @property {number} pageSize   - 每页条数
 */

/**
 * @typedef {Object} ApiResponse
 * @template T
 * @property {number}  code    - 业务状态码 (0=成功)
 * @property {string}  message - 提示信息
 * @property {T}       data    - 响应数据
 */

// ---- 常量映射（Mock 和 Real 共用） ----

export const statusMap = { ready: '就绪', processing: '处理中', failed: '失败', shared: '已分享' }
export const sourceMap = { cloned: '克隆', shared: '下载', preset: '预设' }
