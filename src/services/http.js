/**
 * HTTP 请求客户端
 *
 * 仅在 USE_MOCK = false 时使用，封装 fetch 实现统一错误处理。
 */

import { API_BASE_URL, REQUEST_TIMEOUT } from './config'

function getAuthHeaders() {
  const token = localStorage.getItem('authToken')
  return token ? { 'Authorization': `Bearer ${token}` } : {}
}

async function request(url, options = {}) {
  const controller = new AbortController()
  const timeoutId = setTimeout(() => controller.abort(), REQUEST_TIMEOUT)

  const headers = {
    ...getAuthHeaders(),
    ...options.headers,
  }

  const config = {
    ...options,
    headers,
    signal: controller.signal,
  }

  try {
    const response = await fetch(`${API_BASE_URL}${url}`, config)
    clearTimeout(timeoutId)

    if (!response.ok) {
      throw new Error(`HTTP ${response.status}: ${response.statusText}`)
    }

    const result = await response.json()

    if (result.code !== 0) {
      throw new Error(result.message || '请求失败')
    }

    return result.data
  } catch (err) {
    clearTimeout(timeoutId)
    if (err.name === 'AbortError') {
      throw new Error('请求超时')
    }
    throw err
  }
}

export function get(url, params = {}) {
  const query = new URLSearchParams(params).toString()
  const fullUrl = query ? `${url}?${query}` : url
  return request(fullUrl, { method: 'GET' })
}

export function post(url, data = {}) {
  return request(url, { method: 'POST', headers: { 'Content-Type': 'application/json' }, body: JSON.stringify(data) })
}

export function postForm(url, formData) {
  return request(url, { method: 'POST', body: formData, headers: {} })
}

export function put(url, data = {}) {
  return request(url, { method: 'PUT', body: JSON.stringify(data) })
}

export function del(url) {
  return request(url, { method: 'DELETE' })
}
