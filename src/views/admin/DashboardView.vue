<template>
  <div class="dashboard-page">
    <div class="page-header">
      <h2 class="page-title">仪表盘</h2>
      <p class="page-desc">实时掌握平台运营状况，数据每5分钟更新</p>
    </div>

    <!-- 概览卡片 -->
    <div class="stat-grid">
      <div class="stat-card">
        <div class="stat-card-icon" style="background:rgba(102,126,234,0.1);color:#667eea;">
          <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M17 21v-2a4 4 0 0 0-4-4H5a4 4 0 0 0-4 4v2"/><circle cx="9" cy="7" r="4"/><path d="M23 21v-2a4 4 0 0 0-3-3.87"/><path d="M16 3.13a4 4 0 0 1 0 7.75"/></svg>
        </div>
        <div class="stat-card-body">
          <div class="stat-card-value">{{ overview.total_users }}</div>
          <div class="stat-card-label">总用户数</div>
        </div>
      </div>
      <div class="stat-card">
        <div class="stat-card-icon" style="background:rgba(16,185,129,0.1);color:#10B981;">
          <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M9 18V5l12-2v13"/><circle cx="6" cy="18" r="3"/><circle cx="18" cy="16" r="3"/></svg>
        </div>
        <div class="stat-card-body">
          <div class="stat-card-value">{{ overview.total_voices }}</div>
          <div class="stat-card-label">总音色数</div>
        </div>
      </div>
      <div class="stat-card">
        <div class="stat-card-icon" style="background:rgba(245,158,11,0.1);color:#F59E0B;">
          <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><polyline points="22 12 18 12 15 21 9 3 6 12 2 12"/></svg>
        </div>
        <div class="stat-card-body">
          <div class="stat-card-value">{{ overview.today_tts_count }}</div>
          <div class="stat-card-label">今日TTS调用量</div>
        </div>
      </div>
      <div class="stat-card">
        <div class="stat-card-icon" style="background:rgba(99,102,241,0.1);color:#6366F1;">
          <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M13 2L3 14h9l-1 8 10-12h-9l1-8z"/></svg>
        </div>
        <div class="stat-card-body">
          <div class="stat-card-value">{{ overview.active_users_7d }}</div>
          <div class="stat-card-label">活跃用户数 (7天)</div>
        </div>
      </div>
    </div>

    <!-- 趋势图 -->
    <div class="charts-row">
      <div class="chart-card">
        <h3 class="chart-title">用户增长趋势</h3>
        <div ref="userChartRef" class="chart-container"></div>
      </div>
      <div class="chart-card">
        <h3 class="chart-title">TTS调用量趋势</h3>
        <div ref="ttsChartRef" class="chart-container"></div>
      </div>
    </div>

    <!-- 排行榜 -->
    <div class="rankings-row">
      <div class="ranking-card">
        <h3 class="chart-title">热门音色 Top 10</h3>
        <div class="ranking-list" v-if="rankings.top_voices && rankings.top_voices.length">
          <div class="ranking-item" v-for="item in rankings.top_voices" :key="item.id">
            <span class="ranking-num" :class="{ top3: item.rank <= 3 }">{{ item.rank }}</span>
            <span class="ranking-name">{{ item.name }}</span>
            <span class="ranking-count">{{ item.count }} 次</span>
          </div>
        </div>
        <div class="empty-state" v-else>暂无数据</div>
      </div>
      <div class="ranking-card">
        <h3 class="chart-title">活跃用户 Top 10</h3>
        <div class="ranking-list" v-if="rankings.top_users && rankings.top_users.length">
          <div class="ranking-item" v-for="item in rankings.top_users" :key="item.id">
            <span class="ranking-num" :class="{ top3: item.rank <= 3 }">{{ item.rank }}</span>
            <span class="ranking-name">{{ item.name }}</span>
            <span class="ranking-count">{{ item.count }} 次</span>
          </div>
        </div>
        <div class="empty-state" v-else>暂无数据</div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, onUnmounted, nextTick } from 'vue'
import * as echarts from 'echarts'
import { getStatsOverview, getStatsTrends, getStatsRankings } from '@/services/adminApi.js'
import { useToast } from '@/composables/useToast'

const { showToast } = useToast()

const overview = ref({ total_users: 0, total_voices: 0, today_tts_count: 0, active_users_7d: 0 })
const rankings = ref({ top_voices: [], top_users: [] })

const userChartRef = ref(null)
const ttsChartRef = ref(null)
let userChart = null
let ttsChart = null
let refreshTimer = null

function initUserChart(data) {
  if (!userChartRef.value) return
  if (userChart) userChart.dispose()
  userChart = echarts.init(userChartRef.value)
  userChart.setOption({
    tooltip: { trigger: 'axis' },
    grid: { left: 50, right: 20, top: 20, bottom: 30 },
    xAxis: { type: 'category', data: data.map(d => d.date.slice(5)), axisLabel: { fontSize: 11, color: '#999' } },
    yAxis: { type: 'value', minInterval: 1, axisLabel: { fontSize: 11, color: '#999' } },
    series: [{
      data: data.map(d => d.count), type: 'line', smooth: true,
      lineStyle: { color: '#667eea', width: 2 },
      itemStyle: { color: '#667eea' },
      areaStyle: { color: new echarts.graphic.LinearGradient(0, 0, 0, 1, [
        { offset: 0, color: 'rgba(102,126,234,0.3)' },
        { offset: 1, color: 'rgba(102,126,234,0.02)' }
      ]) },
      symbolSize: 4,
    }],
  })
}

function initTtsChart(data) {
  if (!ttsChartRef.value) return
  if (ttsChart) ttsChart.dispose()
  ttsChart = echarts.init(ttsChartRef.value)
  ttsChart.setOption({
    tooltip: { trigger: 'axis' },
    grid: { left: 50, right: 20, top: 20, bottom: 30 },
    xAxis: { type: 'category', data: data.map(d => d.date.slice(5)), axisLabel: { fontSize: 11, color: '#999' } },
    yAxis: { type: 'value', minInterval: 1, axisLabel: { fontSize: 11, color: '#999' } },
    series: [{
      data: data.map(d => d.count), type: 'line', smooth: true,
      lineStyle: { color: '#10B981', width: 2 },
      itemStyle: { color: '#10B981' },
      areaStyle: { color: new echarts.graphic.LinearGradient(0, 0, 0, 1, [
        { offset: 0, color: 'rgba(16,185,129,0.3)' },
        { offset: 1, color: 'rgba(16,185,129,0.02)' }
      ]) },
      symbolSize: 4,
    }],
  })
}

async function fetchOverview() {
  try {
    overview.value = await getStatsOverview()
  } catch (e) {
    showToast('error', '加载概览失败: ' + e.message)
  }
}

async function fetchTrends() {
  try {
    const data = await getStatsTrends(30)
    await nextTick()
    initUserChart(data.user_growth)
    initTtsChart(data.tts_usage)
  } catch (e) {
    showToast('error', '加载趋势失败: ' + e.message)
  }
}

async function fetchRankings() {
  try {
    rankings.value = await getStatsRankings()
  } catch (e) {
    showToast('error', '加载排行榜失败: ' + e.message)
  }
}

async function refreshAll() {
  await Promise.all([fetchOverview(), fetchTrends(), fetchRankings()])
}

function handleResize() {
  userChart?.resize()
  ttsChart?.resize()
}

onMounted(() => {
  refreshAll()
  refreshTimer = setInterval(refreshAll, 5 * 60 * 1000)
  window.addEventListener('resize', handleResize)
})

onUnmounted(() => {
  if (refreshTimer) clearInterval(refreshTimer)
  userChart?.dispose()
  ttsChart?.dispose()
  window.removeEventListener('resize', handleResize)
})
</script>

<style scoped>
.dashboard-page { width: 100%; }

.stat-grid {
  display: grid;
  grid-template-columns: repeat(4, 1fr);
  gap: 20px;
  margin-bottom: 24px;
}

.stat-card {
  background: #fff;
  border-radius: 12px;
  padding: 24px;
  display: flex;
  align-items: center;
  gap: 16px;
  box-shadow: 0 1px 3px rgba(0,0,0,0.06);
}

.stat-card-icon {
  width: 48px; height: 48px;
  border-radius: 12px;
  display: flex;
  align-items: center;
  justify-content: center;
  flex-shrink: 0;
}

.stat-card-icon svg { width: 24px; height: 24px; }

.stat-card-value {
  font-size: 28px;
  font-weight: 700;
  color: #1a1a2e;
  line-height: 1.2;
}

.stat-card-label {
  font-size: 13px;
  color: #888;
  margin-top: 2px;
}

.charts-row, .rankings-row {
  display: grid;
  grid-template-columns: repeat(2, 1fr);
  gap: 20px;
  margin-bottom: 24px;
}

.chart-card, .ranking-card {
  background: #fff;
  border-radius: 12px;
  padding: 24px;
  box-shadow: 0 1px 3px rgba(0,0,0,0.06);
}

.chart-title {
  font-size: 16px;
  font-weight: 600;
  color: #1a1a2e;
  margin-bottom: 16px;
}

.chart-container { width: 100%; height: 280px; }

.ranking-list { display: flex; flex-direction: column; gap: 0; }

.ranking-item {
  display: flex;
  align-items: center;
  gap: 12px;
  padding: 10px 0;
  border-bottom: 1px solid #f0f0f0;
}

.ranking-item:last-child { border-bottom: none; }

.ranking-num {
  width: 24px; height: 24px;
  border-radius: 6px;
  background: #f0f0f0;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 12px;
  font-weight: 600;
  color: #888;
  flex-shrink: 0;
}

.ranking-num.top3 {
  background: linear-gradient(135deg, #667eea, #764ba2);
  color: #fff;
}

.ranking-name {
  flex: 1;
  font-size: 14px;
  color: #333;
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
}

.ranking-count {
  font-size: 13px;
  color: #888;
  flex-shrink: 0;
}

.empty-state {
  padding: 40px;
  text-align: center;
  color: #999;
  font-size: 14px;
}

@media (max-width: 1279px) {
  .stat-grid { grid-template-columns: repeat(2, 1fr); }
  .charts-row, .rankings-row { grid-template-columns: 1fr; }
}

@media (max-width: 767px) {
  .stat-grid { grid-template-columns: 1fr; }
  .stat-card { padding: 16px; }
  .stat-card-value { font-size: 24px; }
}
</style>
