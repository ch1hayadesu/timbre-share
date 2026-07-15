<template>
  <div class="logs-page">
    <div class="page-header">
      <h2 class="page-title">操作日志</h2>
      <p class="page-desc">管理员操作记录与系统异常日志</p>
    </div>

    <!-- Tab 切换 -->
    <div class="tabs">
      <button :class="{ active: activeTab === 'operations' }" @click="activeTab = 'operations'; page = 1; fetchData()">管理员操作记录</button>
      <button :class="{ active: activeTab === 'errors' }" @click="activeTab = 'errors'; page = 1; fetchData()">系统异常日志</button>
    </div>

    <!-- 操作日志筛选 -->
    <div class="toolbar" v-if="activeTab === 'operations'">
      <div class="toolbar-row">
        <select class="filter-select" v-model="opType" @change="page = 1; fetchData()">
          <option value="">全部操作类型</option>
          <option value="login">登录</option>
          <option value="logout">登出</option>
          <option value="disable_user">禁用用户</option>
          <option value="enable_user">启用用户</option>
          <option value="delete_user">删除用户</option>
          <option value="unlist_voice">下架音色</option>
          <option value="list_voice">上架音色</option>
          <option value="delete_voice">删除音色</option>
          <option value="set_recommend">设置推荐</option>
          <option value="set_popular">设置热门</option>
        </select>
        <input type="text" class="filter-input" v-model="opAdminName" placeholder="操作人" @keyup.enter="page = 1; fetchData()" />
        <input type="date" class="filter-date" v-model="opStartDate" @change="page = 1; fetchData()" />
        <span class="filter-sep">至</span>
        <input type="date" class="filter-date" v-model="opEndDate" @change="page = 1; fetchData()" />
        <button class="btn btn-secondary" @click="opType = ''; opAdminName = ''; opStartDate = ''; opEndDate = ''; page = 1; fetchData()">清除</button>
      </div>
    </div>

    <!-- 错误日志筛选 -->
    <div class="toolbar" v-if="activeTab === 'errors'">
      <div class="toolbar-row">
        <input type="text" class="filter-input" v-model="errorType" placeholder="异常类型" @keyup.enter="page = 1; fetchData()" />
        <input type="date" class="filter-date" v-model="errStartDate" @change="page = 1; fetchData()" />
        <span class="filter-sep">至</span>
        <input type="date" class="filter-date" v-model="errEndDate" @change="page = 1; fetchData()" />
        <button class="btn btn-secondary" @click="errorType = ''; errStartDate = ''; errEndDate = ''; page = 1; fetchData()">清除</button>
      </div>
    </div>

    <!-- 操作日志表格 -->
    <div class="table-wrapper" v-if="activeTab === 'operations'">
      <table class="data-table">
        <thead>
          <tr>
            <th>操作时间</th>
            <th>操作人</th>
            <th>操作类型</th>
            <th>操作对象</th>
            <th>操作结果</th>
            <th>IP地址</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="log in items" :key="log.id">
            <td>{{ formatDate(log.created_at) }}</td>
            <td>{{ log.admin_name }}</td>
            <td><span class="op-type-tag">{{ getOpTypeLabel(log.operation_type) }}</span></td>
            <td>{{ log.target_name || `#${log.target_id}` }}</td>
            <td>
              <span class="result-badge" :class="log.result === 'success' ? 'success' : 'fail'">
                {{ log.result === 'success' ? '成功' : '失败' }}
              </span>
            </td>
            <td class="cell-mono">{{ log.ip_address || '-' }}</td>
          </tr>
          <tr v-if="loading">
            <td colspan="6" class="loading-cell">加载中...</td>
          </tr>
          <tr v-if="!loading && items.length === 0">
            <td colspan="6" class="empty-cell">
              <div class="empty-state">暂无操作记录</div>
            </td>
          </tr>
        </tbody>
      </table>
    </div>

    <!-- 错误日志表格 -->
    <div class="table-wrapper" v-if="activeTab === 'errors'">
      <table class="data-table">
        <thead>
          <tr>
            <th>时间</th>
            <th>异常类型</th>
            <th>异常信息</th>
            <th>请求路径</th>
            <th>操作</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="log in items" :key="log.id">
            <td>{{ formatDate(log.created_at) }}</td>
            <td><span class="error-type-tag">{{ log.error_type }}</span></td>
            <td class="cell-message">{{ truncate(log.error_message, 80) }}</td>
            <td class="cell-mono">{{ log.request_method }} {{ log.request_path }}</td>
            <td>
              <button class="action-btn info" @click="showDetail = log">查看详情</button>
            </td>
          </tr>
          <tr v-if="loading">
            <td colspan="5" class="loading-cell">加载中...</td>
          </tr>
          <tr v-if="!loading && items.length === 0">
            <td colspan="5" class="empty-cell">
              <div class="empty-state">暂无异常日志</div>
            </td>
          </tr>
        </tbody>
      </table>
    </div>

    <!-- 分页 -->
    <div class="pagination" v-if="totalPages > 1">
      <button :disabled="page <= 1" @click="page--; fetchData()">上一页</button>
      <span class="page-info">第 {{ page }} / {{ totalPages }} 页 (共 {{ total }} 条)</span>
      <button :disabled="page >= totalPages" @click="page++; fetchData()">下一页</button>
    </div>

    <!-- 错误详情弹窗 -->
    <Teleport to="body">
      <div v-if="showDetail" class="detail-modal-mask" @click.self="showDetail = null">
        <div class="detail-modal">
          <div class="detail-header">
            <h3>异常详情</h3>
            <button class="detail-close" @click="showDetail = null">✕</button>
          </div>
          <div class="detail-body">
            <div class="detail-row"><label>异常类型:</label> {{ showDetail.error_type }}</div>
            <div class="detail-row"><label>异常信息:</label> {{ showDetail.error_message }}</div>
            <div class="detail-row"><label>请求路径:</label> {{ showDetail.request_method }} {{ showDetail.request_path }}</div>
            <div class="detail-row"><label>发生时间:</label> {{ formatDate(showDetail.created_at) }}</div>
            <div class="detail-row" v-if="showDetail.traceback">
              <label>堆栈跟踪:</label>
              <pre class="traceback-block">{{ showDetail.traceback }}</pre>
            </div>
          </div>
        </div>
      </div>
    </Teleport>
  </div>
</template>

<script setup>
import { ref, onMounted, computed } from 'vue'
import { getOperationLogs, getErrorLogs } from '@/services/adminApi.js'
import { useToast } from '@/composables/useToast'

const { showToast } = useToast()

const activeTab = ref('operations')

// 操作日志筛选
const opType = ref('')
const opAdminName = ref('')
const opStartDate = ref('')
const opEndDate = ref('')

// 错误日志筛选
const errorType = ref('')
const errStartDate = ref('')
const errEndDate = ref('')

const items = ref([])
const page = ref(1)
const pageSize = ref(20)
const total = ref(0)
const loading = ref(false)
const showDetail = ref(null)

const totalPages = computed(() => Math.max(1, Math.ceil(total.value / pageSize.value)))

const opTypeLabels = {
  login: '登录', logout: '登出',
  disable_user: '禁用用户', enable_user: '启用用户', delete_user: '删除用户',
  unlist_voice: '下架音色', list_voice: '上架音色', delete_voice: '删除音色',
  set_recommend: '设置推荐', set_popular: '设置热门',
}

function getOpTypeLabel(type) {
  return opTypeLabels[type] || type
}

function formatDate(d) {
  if (!d) return '-'
  return new Date(d).toLocaleDateString('zh-CN', { year: 'numeric', month: '2-digit', day: '2-digit', hour: '2-digit', minute: '2-digit', second: '2-digit' })
}

function truncate(str, len) {
  if (!str) return '-'
  return str.length > len ? str.slice(0, len) + '...' : str
}

async function fetchData() {
  loading.value = true
  try {
    if (activeTab.value === 'operations') {
      const data = await getOperationLogs({
        page: page.value,
        page_size: pageSize.value,
        operation_type: opType.value || undefined,
        admin_name: opAdminName.value || undefined,
        start_date: opStartDate.value || undefined,
        end_date: opEndDate.value || undefined,
      })
      items.value = data.items
      total.value = data.pagination.total
    } else {
      const data = await getErrorLogs({
        page: page.value,
        page_size: pageSize.value,
        error_type: errorType.value || undefined,
        start_date: errStartDate.value || undefined,
        end_date: errEndDate.value || undefined,
      })
      items.value = data.items
      total.value = data.pagination.total
    }
  } catch (e) {
    showToast('error', '加载日志失败: ' + e.message)
  } finally {
    loading.value = false
  }
}

onMounted(() => {
  fetchData()
})
</script>

<style scoped>
.logs-page { width: 100%; }

.tabs {
  display: flex;
  gap: 0;
  margin-bottom: 16px;
  border-bottom: 2px solid #f0f0f0;
}

.tabs button {
  padding: 10px 24px;
  border: none;
  background: none;
  font-size: 14px;
  color: #888;
  cursor: pointer;
  transition: all 0.2s;
  border-bottom: 2px solid transparent;
  margin-bottom: -2px;
}

.tabs button:hover { color: #333; }
.tabs button.active { color: #667eea; border-bottom-color: #667eea; font-weight: 500; }

.toolbar { margin-bottom: 16px; }

.toolbar-row {
  display: flex;
  align-items: center;
  gap: 10px;
  flex-wrap: wrap;
}

.filter-select, .filter-input, .filter-date {
  height: 36px;
  padding: 0 10px;
  border: 1.5px solid #e0e0e0;
  border-radius: 8px;
  font-size: 13px;
  outline: none;
  background: #fff;
  transition: border-color 0.2s;
}

.filter-select { min-width: 140px; }
.filter-input { width: 160px; }
.filter-date { width: 150px; }

.filter-select:focus, .filter-input:focus, .filter-date:focus { border-color: #667eea; }

.filter-sep { color: #999; font-size: 13px; }

.btn {
  height: 36px; padding: 0 16px;
  border: none; border-radius: 8px;
  font-size: 13px; cursor: pointer;
  transition: all 0.2s;
}

.btn-secondary { background: #f0f0f0; color: #666; }
.btn-secondary:hover { background: #e0e0e0; }

.table-wrapper {
  background: #fff;
  border-radius: 12px;
  overflow: hidden;
  box-shadow: 0 1px 3px rgba(0,0,0,0.06);
}

.data-table { width: 100%; border-collapse: collapse; }

.data-table th {
  padding: 14px 16px; text-align: left;
  font-size: 13px; font-weight: 600; color: #666;
  background: #fafafa; border-bottom: 1px solid #f0f0f0;
}

.data-table td {
  padding: 14px 16px;
  font-size: 13px; color: #333;
  border-bottom: 1px solid #f5f5f5;
}

.data-table tbody tr:hover { background: #fafbfd; }

.cell-mono { font-family: monospace; font-size: 12px !important; color: #888; }
.cell-message { max-width: 250px; overflow: hidden; text-overflow: ellipsis; white-space: nowrap; }

.op-type-tag {
  display: inline-block;
  padding: 2px 8px;
  background: #ede9fe;
  color: #7C3AED;
  border-radius: 4px;
  font-size: 12px;
  white-space: nowrap;
}

.error-type-tag {
  display: inline-block;
  padding: 2px 8px;
  background: #fde8e8;
  color: #EF4444;
  border-radius: 4px;
  font-size: 12px;
  white-space: nowrap;
}

.result-badge {
  display: inline-block;
  padding: 2px 8px;
  border-radius: 4px;
  font-size: 12px;
  font-weight: 500;
}

.result-badge.success { background: #e6f7ee; color: #10B981; }
.result-badge.fail { background: #fde8e8; color: #EF4444; }

.action-btn {
  padding: 4px 10px;
  border: none; border-radius: 5px;
  font-size: 12px; cursor: pointer;
  transition: all 0.2s;
}

.action-btn.info { background: #ede9fe; color: #7C3AED; }
.action-btn.info:hover { background: #ddd6fe; }

.loading-cell, .empty-cell { text-align: center; padding: 40px !important; color: #999; }
.empty-state { font-size: 14px; color: #999; }

.pagination {
  display: flex; align-items: center; justify-content: center;
  gap: 16px; margin-top: 20px; padding: 12px 0;
}

.pagination button {
  padding: 8px 16px;
  border: 1.5px solid #e0e0e0;
  background: #fff; border-radius: 8px;
  font-size: 13px; cursor: pointer; color: #333;
  transition: all 0.2s;
}

.pagination button:hover:not(:disabled) { border-color: #667eea; color: #667eea; }
.pagination button:disabled { opacity: 0.4; cursor: not-allowed; }

.page-info { font-size: 13px; color: #888; }

/* Detail Modal */
.detail-modal-mask {
  position: fixed; inset: 0;
  background: rgba(0,0,0,0.5);
  display: flex; align-items: center; justify-content: center;
  z-index: 10000;
}

.detail-modal {
  background: #fff;
  border-radius: 16px;
  width: 700px;
  max-width: 90vw;
  max-height: 80vh;
  overflow-y: auto;
  box-shadow: 0 20px 60px rgba(0,0,0,0.15);
}

.detail-header {
  display: flex; align-items: center; justify-content: space-between;
  padding: 20px 24px;
  border-bottom: 1px solid #f0f0f0;
}

.detail-header h3 { font-size: 18px; font-weight: 600; color: #1a1a2e; }

.detail-close {
  width: 32px; height: 32px;
  border: none; background: #f0f0f0;
  border-radius: 50%;
  font-size: 14px; cursor: pointer;
  display: flex; align-items: center; justify-content: center;
  color: #666;
}

.detail-close:hover { background: #e0e0e0; }

.detail-body { padding: 24px; }

.detail-row {
  margin-bottom: 16px;
  font-size: 14px;
  color: #333;
  word-break: break-all;
}

.detail-row label {
  display: block;
  font-size: 12px;
  font-weight: 600;
  color: #888;
  margin-bottom: 4px;
  text-transform: uppercase;
}

.traceback-block {
  background: #1a1a2e;
  color: #e0e0e0;
  padding: 16px;
  border-radius: 8px;
  font-size: 12px;
  line-height: 1.6;
  overflow-x: auto;
  max-height: 300px;
  overflow-y: auto;
  margin-top: 8px;
  white-space: pre-wrap;
}
</style>
