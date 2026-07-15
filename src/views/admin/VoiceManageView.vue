<template>
  <div class="voice-manage-page">
    <div class="page-header">
      <h2 class="page-title">音色管理</h2>
      <p class="page-desc">管理全平台音色内容</p>
    </div>

    <!-- 搜索 & 筛选 -->
    <div class="toolbar">
      <div class="toolbar-left">
        <input type="text" class="search-input" v-model="keyword" placeholder="搜索音色名称" @keyup.enter="handleSearch" />
        <button class="btn btn-primary" @click="handleSearch">搜索</button>
      </div>
      <div class="toolbar-right">
        <div class="filter-tabs">
          <button :class="{ active: statusFilter === 'all' }" @click="statusFilter = 'all'; page = 1; fetchVoices()">全部</button>
          <button :class="{ active: statusFilter === 'active' }" @click="statusFilter = 'active'; page = 1; fetchVoices()">正常</button>
          <button :class="{ active: statusFilter === 'unlisted' }" @click="statusFilter = 'unlisted'; page = 1; fetchVoices()">已下架</button>
        </div>
      </div>
    </div>

    <!-- 表格 -->
    <div class="table-wrapper">
      <table class="data-table">
        <thead>
          <tr>
            <th>音色ID</th>
            <th>名称</th>
            <th>所属用户</th>
            <th>创建时间</th>
            <th>状态</th>
            <th>推荐</th>
            <th>热门</th>
            <th>使用/下载</th>
            <th>操作</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="voice in voices" :key="voice.voice_id">
            <td class="cell-id">{{ voice.voice_id }}</td>
            <td class="cell-name">{{ voice.voice_name }}</td>
            <td>{{ voice.username }}</td>
            <td>{{ formatDate(voice.created_at) }}</td>
            <td>
              <span class="status-badge" :class="voice.admin_status === 'unlisted' ? 'unlisted' : 'active'">
                {{ voice.admin_status === 'unlisted' ? '已下架' : '正常' }}
              </span>
            </td>
            <td>
              <span class="tag" :class="voice.is_recommended ? 'tag-yes' : 'tag-no'">
                {{ voice.is_recommended ? '是' : '否' }}
              </span>
            </td>
            <td>
              <span class="tag" :class="voice.is_popular ? 'tag-yes' : 'tag-no'">
                {{ voice.is_popular ? '是' : '否' }}
              </span>
            </td>
            <td>{{ voice.usage_count }} / {{ voice.download_count }}</td>
            <td class="cell-actions">
              <button v-if="voice.admin_status !== 'unlisted'" class="action-btn warn" @click="confirmToggleStatus(voice)">下架</button>
              <button v-else class="action-btn success" @click="confirmToggleStatus(voice)">上架</button>
              <button class="action-btn danger" @click="confirmDeleteVoice(voice)">删除</button>
              <button v-if="!voice.is_recommended" class="action-btn info" @click="toggleRecommend(voice, true)">推荐</button>
              <button v-else class="action-btn warn" @click="toggleRecommend(voice, false)">取消推荐</button>
              <button v-if="!voice.is_popular" class="action-btn info" @click="togglePopular(voice, true)">热门</button>
              <button v-else class="action-btn warn" @click="togglePopular(voice, false)">取消热门</button>
            </td>
          </tr>
          <tr v-if="loading">
            <td colspan="9" class="loading-cell">加载中...</td>
          </tr>
          <tr v-if="!loading && voices.length === 0">
            <td colspan="9" class="empty-cell">
              <div class="empty-state">暂无音色数据</div>
            </td>
          </tr>
        </tbody>
      </table>
    </div>

    <!-- 分页 -->
    <div class="pagination" v-if="totalPages > 1">
      <button :disabled="page <= 1" @click="page--; fetchVoices()">上一页</button>
      <span class="page-info">第 {{ page }} / {{ totalPages }} 页 (共 {{ total }} 条)</span>
      <button :disabled="page >= totalPages" @click="page++; fetchVoices()">下一页</button>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, computed } from 'vue'
import { getAdminVoices, updateVoiceStatus, deleteAdminVoice, toggleVoiceRecommend, toggleVoicePopular } from '@/services/adminApi.js'
import { useToast } from '@/composables/useToast'
import { useModal } from '@/composables/useModal'

const { showToast } = useToast()
const { showModal } = useModal()

const voices = ref([])
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
  fetchVoices()
}

async function fetchVoices() {
  loading.value = true
  try {
    const data = await getAdminVoices({
      page: page.value,
      page_size: pageSize.value,
      keyword: keyword.value || undefined,
      status: statusFilter.value,
    })
    voices.value = data.items
    total.value = data.pagination.total
  } catch (e) {
    showToast('error', '加载音色列表失败: ' + e.message)
  } finally {
    loading.value = false
  }
}

function confirmToggleStatus(voice) {
  const action = voice.admin_status === 'unlisted' ? '上架' : '下架'
  const newStatus = voice.admin_status === 'unlisted' ? 'active' : 'unlisted'
  showModal(`${action}音色`, `确定要${action}音色 "${voice.voice_name}" 吗？`, async () => {
    try {
      await updateVoiceStatus(voice.voice_id, newStatus)
      showToast('success', `${action}成功`)
      fetchVoices()
    } catch (e) {
      showToast('error', `${action}失败: ` + e.message)
    }
  }, action, voice.admin_status !== 'unlisted')
}

function confirmDeleteVoice(voice) {
  showModal('删除音色', `确定要永久删除音色 "${voice.voice_name}" 吗？此操作不可恢复！`, async () => {
    try {
      await deleteAdminVoice(voice.voice_id)
      showToast('success', '删除成功')
      fetchVoices()
    } catch (e) {
      showToast('error', '删除失败: ' + e.message)
    }
  }, '确认删除', true)
}

async function toggleRecommend(voice, value) {
  try {
    await toggleVoiceRecommend(voice.voice_id, value)
    showToast('success', value ? '已设为推荐' : '已取消推荐')
    fetchVoices()
  } catch (e) {
    showToast('error', '操作失败: ' + e.message)
  }
}

async function togglePopular(voice, value) {
  try {
    await toggleVoicePopular(voice.voice_id, value)
    showToast('success', value ? '已设为热门' : '已取消热门')
    fetchVoices()
  } catch (e) {
    showToast('error', '操作失败: ' + e.message)
  }
}

onMounted(() => {
  fetchVoices()
})
</script>

<style scoped>
.voice-manage-page { width: 100%; }

.toolbar {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 16px;
  margin-bottom: 20px;
  flex-wrap: wrap;
}

.toolbar-left { display: flex; gap: 8px; }

.search-input {
  width: 260px; height: 38px;
  padding: 0 12px;
  border: 1.5px solid #e0e0e0;
  border-radius: 8px;
  font-size: 13px;
  outline: none;
  transition: border-color 0.2s;
}

.search-input:focus { border-color: #667eea; }

.btn {
  height: 38px; padding: 0 18px;
  border: none; border-radius: 8px;
  font-size: 13px; cursor: pointer;
  transition: all 0.2s;
}

.btn-primary { background: #667eea; color: #fff; }
.btn-primary:hover { background: #5a6fd6; }

.filter-tabs {
  display: flex; gap: 4px;
  background: #f0f0f0;
  padding: 3px;
  border-radius: 8px;
}

.filter-tabs button {
  padding: 6px 16px;
  border: none; background: none;
  font-size: 13px; color: #666;
  border-radius: 6px; cursor: pointer;
  transition: all 0.2s;
}

.filter-tabs button.active {
  background: #fff; color: #1a1a2e;
  font-weight: 500;
  box-shadow: 0 1px 3px rgba(0,0,0,0.1);
}

.table-wrapper {
  background: #fff;
  border-radius: 12px;
  overflow-x: auto;
  box-shadow: 0 1px 3px rgba(0,0,0,0.06);
}

.data-table { width: 100%; border-collapse: collapse; min-width: 900px; }

.data-table th {
  padding: 14px 12px;
  text-align: left;
  font-size: 13px; font-weight: 600;
  color: #666; background: #fafafa;
  border-bottom: 1px solid #f0f0f0;
  white-space: nowrap;
}

.data-table td {
  padding: 14px 12px;
  font-size: 13px; color: #333;
  border-bottom: 1px solid #f5f5f5;
}

.data-table tbody tr:hover { background: #fafbfd; }

.cell-id { font-family: monospace; color: #888; }
.cell-name { font-weight: 500; max-width: 120px; overflow: hidden; text-overflow: ellipsis; white-space: nowrap; }

.status-badge {
  display: inline-block;
  padding: 3px 10px;
  border-radius: 12px;
  font-size: 12px; font-weight: 500;
  white-space: nowrap;
}

.status-badge.active { background: #e6f7ee; color: #10B981; }
.status-badge.unlisted { background: #fde8e8; color: #EF4444; }

.tag {
  display: inline-block;
  padding: 2px 8px;
  border-radius: 4px;
  font-size: 12px;
}

.tag-yes { background: #e6f7ee; color: #10B981; }
.tag-no { background: #f0f0f0; color: #999; }

.cell-actions {
  display: flex; gap: 6px; flex-wrap: wrap;
}

.action-btn {
  padding: 3px 8px;
  border: none; border-radius: 5px;
  font-size: 11px; cursor: pointer;
  white-space: nowrap;
  transition: all 0.2s;
}

.action-btn.warn { background: #fef3c7; color: #d97706; }
.action-btn.warn:hover { background: #fde68a; }
.action-btn.success { background: #e6f7ee; color: #10B981; }
.action-btn.success:hover { background: #d1fae5; }
.action-btn.danger { background: #fde8e8; color: #EF4444; }
.action-btn.danger:hover { background: #fecaca; }
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
</style>
