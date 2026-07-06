/**
 * 音色共享平台 Mock 数据
 */

export const mockVoices = [
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

export const mockMarketVoices = [
  { id: 101, name: '温柔女声', author: '小**', downloads: 234, date: '2026-07-05' },
  { id: 102, name: '磁性大叔', author: '张**', downloads: 189, date: '2026-07-04' },
  { id: 103, name: '活泼少女', author: '李**', downloads: 156, date: '2026-07-03' },
  { id: 104, name: '御姐音', author: '王**', downloads: 128, date: '2026-07-02' },
  { id: 105, name: '专业播音', author: '陈**', downloads: 312, date: '2026-07-01' },
  { id: 106, name: '正太音', author: '刘**', downloads: 98, date: '2026-06-30' },
]

export const mockSynthesis = [
  { id: 1, text: '大家好，欢迎来到今天的节目...', voice: '温柔女声', params: '语速1.0x 音量80% 音调0', status: 'success', date: '2026-07-05 14:30' },
  { id: 2, text: '今天天气真好，我们一起去...', voice: '沉稳男声', params: '语速1.2x 音量90% 音调+2', status: 'success', date: '2026-07-05 10:15' },
  { id: 3, text: '产品功能介绍：本产品采用...', voice: '知性女声', params: '语速0.8x 音量75% 音调-1', status: 'success', date: '2026-07-04 16:45' },
  { id: 4, text: '温馨提示：请注意天气变化...', voice: '磁性大叔', params: '语速1.0x 音量85% 音调0', status: 'success', date: '2026-07-04 09:20' },
  { id: 5, text: '这是一条测试文本，用于验证...', voice: '活泼少女', params: '语速1.5x 音量70% 音调+3', status: 'failed', date: '2026-07-03 11:00' },
]

export const ttsVoiceOptions = [
  { value: 1, label: '温柔女声' },
  { value: 2, label: '沉稳男声' },
  { value: 3, label: '活泼少女' },
  { value: 4, label: '磁性大叔' },
  { value: 5, label: '知性女声' },
]

export const statusMap = { ready: '就绪', processing: '处理中', failed: '失败', shared: '已分享' }
export const sourceMap = { cloned: '克隆', shared: '下载', preset: '预设' }
