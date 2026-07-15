<template>
  <div class="user-manage-page">
    <div class="page-header">
      <h2 class="page-title">用户管理</h2>
      <p class="page-desc">管理平台所有用户账号</p>
    </div>

    <!-- 搜索 & 筛选 -->
    <div class="toolbar">
      <div class="toolbar-left">
        <input type="text" class="search-input" v-model="keyword" placeholder="搜索用户名/手机号" @keyup.enter="handleSearch" />
        <button class="btn btn-primary" @click="handleSearch">搜索</button>
      </div>
      <div class="toolbar-right">
        <div class="filter-tabs">
          <button :class="{ active: statusFilter === 'all' }" @click="statusFilter = 'all'; page = 1; fetchUsers()">全部</button>
          <button :class="{ active: statusFilter === 'enabled' }" @click="statusFilter = 'enabled'; page = 1; fetchUsers()">启用</button>
          <button :class="{ active: statusFilter === 'disabled' }" @click="statusFilter = 'disabled'; page = 1; fetchUsers()">禁用</button>
        </div>
      </div>
    </div>

    <!-- 表格 -->
    <div class="table-wrapper">
      <table class="data-table">
        <thead>
          <tr>
            <th>用户ID</th>
            <th>手机号</th>
            <th>注册时间</th>
            <th>状态</th>
            <th>音色数量</th>
            <th>操作</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="user in users" :key="user.user_id">
            <td class="cell-id">{{ user.user_id }}</td>
            <td>{{ user.phone }}</td>
            <td>{{ formatDate(user.created_at) }}</td>
            <td>
              <span class="status-badge" :class="user.is_disabled ? 'disabled' : 'enabled'">
                {{ user.is_disabled ? '已禁用' : '启用' }}
              </span>
            </td>
            <td>{{ user.voice_count }}</td>
            <td class="cell-actions">
              <button v-if="!user.is_disabled" class="action-btn warn" @click="confirmToggleUser(user)">禁用</button>
              <button v-else class="action-btn success" @click="confirmToggleUser(user)">启用</button>
              <button class="action-btn danger" @click="confirmDeleteUser(user)">删除</button>
            </td>
          </tr>
          <tr v-if="loading">
            <td colspan="6" class="loading-cell">加载中...</td>
          </tr>
          <tr v-if="!loading && users.length === 0">
            <td colspan="6" class="empty-cell">
              <div class="empty-state">暂无用户数据</div>
            </td>
          </tr>
        </tbody>
      </table>
    </div>

    <!-- 分页 -->
    <div class="pagination" v-if="totalPages > 1">
      <button :disabled="page <= 1" @click="page--; fetchUsers()">上一页</button>
      <span class="page-info">第 {{ page }} / {{ totalPages }} 页 (共 {{ total }} 条)</span>
      <button :disabled="page >= totalPages" @click="page++; fetchUsers()">下一页</button>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, computed } from 'vue'
import { getAdminUsers, updateUserStatus, deleteAdminUser } from '@/services/adminApi.js'
import { useToast } from '@/composables/useToast'
import { useModal } from '@/composables/useModal'

const { showToast } = useToast()
const { showModal } = useModal()

const users = ref([])
const keyword = ref('')
const statusFilter = ref('all')
const page = ref(1)
const pageSize = ref(20)
const total = ref(0)
const loading = ref(false)

const totalPages = computed(() => Math.max(1, Math.ceil(total.value / pageSize.value)))

function formatDate(d) {
  if (!d) return '-'
  return new Date(d).toLocaleDateString('zh-CN', { year: 'numeric', month: '2-digit', day: '2-digit', hour: '2-digit', minute: '2-digit' })
}

function handleSearch() {
  page.value = 1
  fetchUsers()
}

async function fetchUsers() {
  loading.value = true
  try {
    const data = await getAdminUsers({
      page: page.value,
      page_size: pageSize.value,
      keyword: keyword.value || undefined,
      status: statusFilter.value,
    })
    users.value = data.items
    total.value = data.pagination.total
  } catch (e) {
    showToast('error', '加载用户列表失败: ' + e.message)
  } finally {
    loading.value = false
  }
}

function confirmToggleUser(user) {
  const action = user.is_disabled ? '启用' : '禁用'
  showModal(`${action}用户`, `确定要${action}用户 "${user.phone}" 吗？`, async () => {
    try {
      await updateUserStatus(user.user_id, !user.is_disabled)
      showToast('success', `${action}成功`)
      fetchUsers()
    } catch (e) {
      showToast('error', `${action}失败: ` + e.message)
    }
  }, action, !user.is_disabled)
}

function confirmDeleteUser(user) {
  showModal('删除用户', `确定要永久删除用户 "${user.phone}" 吗？此操作将同时删除该用户的所有音色和关联数据，不可恢复！`, async () => {
    try {
      await deleteAdminUser(user.user_id)
      showToast('success', '删除成功')
      fetchUsers()
    } catch (e) {
      showToast('error', '删除失败: ' + e.message)
    }
  }, '确认删除', true)
}

onMounted(() => {
  fetchUsers()
})
</script>

<style scoped>
.user-manage-page { width: 100%; }

.toolbar {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 16px;
  margin-bottom: 20px;
  flex-wrap: wrap;
}

.toolbar-left {
  display: flex;
  gap: 8px;
}

.search-input {
  width: 260px;
  height: 38px;
  padding: 0 12px;
  border: 1.5px solid #e0e0e0;
  border-radius: 8px;
  font-size: 13px;
  outline: none;
  transition: border-color 0.2s;
}

.search-input:focus { border-color: #667eea; }

.btn {
  height: 38px;
  padding: 0 18px;
  border: none;
  border-radius: 8px;
  font-size: 13px;
  cursor: pointer;
  transition: all 0.2s;
}

.btn-primary {
  background: #667eea;
  color: #fff;
}

.btn-primary:hover { background: #5a6fd6; }

.filter-tabs {
  display: flex;
  gap: 4px;
  background: #f0f0f0;
  padding: 3px;
  border-radius: 8px;
}

.filter-tabs button {
  padding: 6px 16px;
  border: none;
  background: none;
  font-size: 13px;
  color: #666;
  border-radius: 6px;
  cursor: pointer;
  transition: all 0.2s;
}

.filter-tabs button.active {
  background: #fff;
  color: #1a1a2e;
  font-weight: 500;
  box-shadow: 0 1px 3px rgba(0,0,0,0.1);
}

.table-wrapper {
  background: #fff;
  border-radius: 12px;
  overflow: hidden;
  box-shadow: 0 1px 3px rgba(0,0,0,0.06);
}

.data-table { width: 100%; border-collapse: collapse; }

.data-table th {
  padding: 14px 16px;
  text-align: left;
  font-size: 13px;
  font-weight: 600;
  color: #666;
  background: #fafafa;
  border-bottom: 1px solid #f0f0f0;
}

.data-table td {
  padding: 14px 16px;
  font-size: 13px;
  color: #333;
  border-bottom: 1px solid #f5f5f5;
}

.data-table tbody tr:hover { background: #fafbfd; }

.cell-id { font-family: monospace; color: #888; }

.status-badge {
  display: inline-block;
  padding: 3px 10px;
  border-radius: 12px;
  font-size: 12px;
  font-weight: 500;
}

.status-badge.enabled { background: #e6f7ee; color: #10B981; }
.status-badge.disabled { background: #fde8e8; color: #EF4444; }

.cell-actions { display: flex; gap: 8px; }

.action-btn {
  padding: 4px 12px;
  border: none;
  border-radius: 6px;
  font-size: 12px;
  cursor: pointer;
  transition: all 0.2s;
}

.action-btn.warn { background: #fef3c7; color: #d97706; }
.action-btn.warn:hover { background: #fde68a; }
.action-btn.success { background: #e6f7ee; color: #10B981; }
.action-btn.success:hover { background: #d1fae5; }
.action-btn.danger { background: #fde8e8; color: #EF4444; }
.action-btn.danger:hover { background: #fecaca; }

.loading-cell, .empty-cell { text-align: center; padding: 40px !important; color: #999; }
.empty-state { font-size: 14px; color: #999; }

.pagination {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 16px;
  margin-top: 20px;
  padding: 12px 0;
}

.pagination button {
  padding: 8px 16px;
  border: 1.5px solid #e0e0e0;
  background: #fff;
  border-radius: 8px;
  font-size: 13px;
  cursor: pointer;
  color: #333;
  transition: all 0.2s;
}

.pagination button:hover:not(:disabled) { border-color: #667eea; color: #667eea; }
.pagination button:disabled { opacity: 0.4; cursor: not-allowed; }

.page-info { font-size: 13px; color: #888; }
</style>
