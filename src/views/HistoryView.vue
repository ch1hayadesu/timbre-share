<template>
  <div>
    <div class="page-header">
      <h1 class="page-title">浏览历史</h1>
      <p class="page-desc">你查看过的音色记录</p>
    </div>

    <div class="tab-bar">
      <span class="tab" :class="{ active: tab === 'history' }" @click="tab = 'history'">浏览历史</span>
      <span class="tab" :class="{ active: tab === 'favorites' }" @click="tab = 'favorites'">我的收藏</span>
    </div>

    <Card v-if="tab === 'history'">
      <div v-if="historyList.items.length" class="list">
        <div v-for="item in historyList.items" :key="item.id" class="list-item" @click="$router.push('/market')">
          <div class="list-item-name">{{ item.voice_name }}</div>
          <div class="list-item-time">{{ item.created_at }}</div>
        </div>
      </div>
      <EmptyState v-else icon="&#128337;" title="暂无浏览记录" desc="浏览音色市场时会自动记录" />
    </Card>

    <Card v-if="tab === 'favorites'">
      <div v-if="favList.items.length" class="list">
        <div v-for="item in favList.items" :key="item.id" class="list-item">
          <div class="list-item-name">{{ item.voice_name }}</div>
          <div class="list-item-source">{{ item.source }}</div>
          <BaseButton size="sm" type="text" @click.stop="unfav(item)">取消收藏</BaseButton>
        </div>
      </div>
      <EmptyState v-else icon="&#10084;" title="暂无收藏" desc="在音色市场中收藏你喜欢的音色" />
    </Card>

    <div class="pagination">
      <BaseButton size="sm" :disabled="currPage <= 1" @click="currPage--; load()">上一页</BaseButton>
      <span class="page-info">第 {{ currPage }} 页</span>
      <BaseButton size="sm" @click="currPage++; load()">下一页</BaseButton>
    </div>
  </div>
</template>

<script setup>
import { ref, reactive, watch } from 'vue'
import Card from '@/components/Card.vue'
import BaseButton from '@/components/BaseButton.vue'
import EmptyState from '@/components/EmptyState.vue'
import { getHistoryList, getFavoriteList, removeFavorite, recordView } from '@/services'
import { useToast } from '@/composables/useToast'

const { showToast } = useToast()
const tab = ref('history')
const currPage = ref(1)
const historyList = reactive({ items: [], total: 0 })
const favList = reactive({ items: [], total: 0 })

async function load() {
  if (tab.value === 'history') {
    const r = await getHistoryList({ page: currPage.value, pageSize: 20 })
    historyList.items = r.items
    historyList.total = r.total
  } else {
    const r = await getFavoriteList({ page: currPage.value, pageSize: 20 })
    favList.items = r.items
    favList.total = r.total
  }
}

watch(tab, () => { currPage.value = 1; load() })
load()

async function unfav(item) {
  try {
    await removeFavorite(item.voice_id)
    showToast('success', '已取消收藏')
    load()
  } catch (err) {
    showToast('error', err.message)
  }
}
</script>

<style scoped>
.tab-bar { display: flex; gap: 0; margin-bottom: var(--space-4); background: var(--color-bg-section); border-radius: var(--radius-md); overflow: hidden; }
.tab { flex: 1; text-align: center; padding: 10px; cursor: pointer; font-weight: 500; font-size: var(--font-size-sm); color: var(--color-text-secondary); transition: all var(--duration-fast); }
.tab.active { background: white; color: var(--color-primary-6); font-weight: 600; box-shadow: 0 1px 3px rgba(0,0,0,0.08); }
.list { display: flex; flex-direction: column; }
.list-item { display: flex; align-items: center; padding: 12px 0; border-bottom: 1px solid var(--color-border-light); gap: var(--space-3); cursor: pointer; }
.list-item:last-child { border-bottom: none; }
.list-item:hover { background: var(--color-bg-hover); margin: 0 -16px; padding: 12px 16px; border-radius: var(--radius-md); }
.list-item-name { flex: 1; font-weight: 500; font-size: var(--font-size-base); color: var(--color-text-primary); }
.list-item-time { font-size: var(--font-size-xs); color: var(--color-text-disabled); }
.list-item-source { font-size: var(--font-size-xs); color: var(--color-text-secondary); }
</style>
