const KEYS = {
  voiceCount: 'stat_voiceCount',
  synthesisCount: 'stat_synthesisCount',
  scriptCount: 'stat_scriptCount',
  downloadCount: 'stat_downloadCount',
}
const DEFAULTS = { voiceCount: 3, synthesisCount: 12, scriptCount: 5, downloadCount: 2 }

function get(key, fallback) {
  const val = localStorage.getItem(key)
  return val !== null ? parseInt(val, 10) : fallback
}
function set(key, val) {
  localStorage.setItem(key, String(val))
}

export function getStats() {
  return {
    voiceCount: get(KEYS.voiceCount, DEFAULTS.voiceCount),
    synthesisCount: get(KEYS.synthesisCount, DEFAULTS.synthesisCount),
    scriptCount: get(KEYS.scriptCount, DEFAULTS.scriptCount),
    downloadCount: get(KEYS.downloadCount, DEFAULTS.downloadCount),
  }
}

export function incrementVoiceCount() { set(KEYS.voiceCount, get(KEYS.voiceCount, DEFAULTS.voiceCount) + 1) }
export function incrementSynthesisCount() { set(KEYS.synthesisCount, get(KEYS.synthesisCount, DEFAULTS.synthesisCount) + 1) }
export function incrementScriptCount() { set(KEYS.scriptCount, get(KEYS.scriptCount, DEFAULTS.scriptCount) + 1) }
export function incrementDownloadCount() { set(KEYS.downloadCount, get(KEYS.downloadCount, DEFAULTS.downloadCount) + 1) }
