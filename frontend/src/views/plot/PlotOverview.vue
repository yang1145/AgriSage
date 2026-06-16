<template>
  <div class="plot-overview">
    <!-- 左侧数据面板 -->
    <aside class="plot-overview__sidebar">
      <!-- 地块统计 -->
      <HudPanel title="地块统计" class="plot-overview__panel">
        <div v-if="loading" class="plot-overview__loading">
          <el-icon class="is-loading" :size="24"><Loading /></el-icon>
          <span>数据加载中...</span>
        </div>
        <template v-else-if="stats">
          <div class="plot-overview__stat-row">
            <div class="plot-overview__stat-item">
              <span class="plot-overview__stat-value">{{ stats.total_area?.toFixed(1) || '0' }}</span>
              <span class="plot-overview__stat-unit">亩</span>
            </div>
            <div class="plot-overview__stat-item">
              <span class="plot-overview__stat-value">{{ stats.plot_count || 0 }}</span>
              <span class="plot-overview__stat-unit">地块</span>
            </div>
          </div>
          <div class="plot-overview__status-breakdown">
            <div class="plot-overview__status-item">
              <HudStatusLight status="idle" />
              <span class="plot-overview__status-label">闲置</span>
              <span class="plot-overview__status-count">{{ stats.status_distribution?.idle || 0 }}</span>
            </div>
            <div class="plot-overview__status-item">
              <HudStatusLight status="growing" />
              <span class="plot-overview__status-label">种植中</span>
              <span class="plot-overview__status-count">{{ stats.status_distribution?.growing || 0 }}</span>
            </div>
            <div class="plot-overview__status-item">
              <HudStatusLight status="harvested" />
              <span class="plot-overview__status-label">已收割</span>
              <span class="plot-overview__status-count">{{ stats.status_distribution?.harvested || 0 }}</span>
            </div>
          </div>
        </template>
      </HudPanel>

      <!-- 快捷操作 -->
      <HudPanel title="快捷操作" class="plot-overview__panel">
        <HudButton type="cyan" @click="router.push('/plots/create')">
          + 新建地块
        </HudButton>
      </HudPanel>

      <!-- 搜索筛选 -->
      <HudPanel title="搜索筛选" class="plot-overview__panel">
        <el-input
          v-model="searchName"
          placeholder="搜索地块名称..."
          size="small"
          clearable
          @input="onSearch"
        />
        <div style="margin-top: 8px; display: flex; gap: 8px; flex-wrap: wrap;">
          <el-select v-model="searchStatus" placeholder="状态" size="small" clearable style="width: 100px;" @change="onSearch">
            <el-option label="全部" value="" />
            <el-option label="闲置" value="闲置" />
            <el-option label="种植中" value="种植中" />
            <el-option label="已收割" value="已收割" />
          </el-select>
          <el-input-number v-model="searchMinArea" placeholder="最小面积" size="small" :min="0" :precision="1" style="width: 100px;" @change="onSearch" />
          <el-input-number v-model="searchMaxArea" placeholder="最大面积" size="small" :min="0" :precision="1" style="width: 100px;" @change="onSearch" />
        </div>
      </HudPanel>

      <!-- 地块列表 -->
      <HudPanel title="地块列表" class="plot-overview__panel plot-overview__list-panel">
        <div v-if="loading" class="plot-overview__loading">
          <el-icon class="is-loading" :size="20"><Loading /></el-icon>
        </div>
        <div v-else-if="plots.length === 0" class="plot-overview__empty">
          <span>暂无地块数据</span>
        </div>
        <div v-else class="plot-overview__list">
          <div
            v-for="plot in plots"
            :key="plot.id"
            class="plot-overview__list-item"
            @click="router.push(`/plots/${plot.id}`)"
          >
            <HudStatusLight :status="plot.status || 'idle'" />
            <div class="plot-overview__list-info">
              <span class="plot-overview__list-name">{{ plot.name }}</span>
              <span class="plot-overview__list-meta">
                {{ plot.area?.toFixed(1) || '0' }} 亩
                <template v-if="plot.current_variety"> · {{ plot.current_variety }}</template>
              </span>
            </div>
          </div>
        </div>
      </HudPanel>
    </aside>

    <!-- 右侧地图区域 -->
    <div class="plot-overview__map-area">
      <PlotMap
        :plots="plots"
        :center="mapCenter"
        :zoom="mapZoom"
        @select="onPlotSelect"
      />
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { usePlotStore } from '@/stores/plot'
import { storeToRefs } from 'pinia'
import HudPanel from '@/components/hud/HudPanel.vue'
import HudButton from '@/components/hud/HudButton.vue'
import HudStatusLight from '@/components/hud/HudStatusLight.vue'
import PlotMap from '@/components/map/PlotMap.vue'

const router = useRouter()
const plotStore = usePlotStore()
const { plots, stats } = storeToRefs(plotStore)

const loading = ref(true)
const mapCenter = ref([22.8, 108.3])
const mapZoom = ref(11)
const searchName = ref('')
const searchStatus = ref('')
const searchMinArea = ref(null)
const searchMaxArea = ref(null)
let searchTimer = null

const onPlotSelect = (plotId) => {
  router.push(`/plots/${plotId}`)
}

const onSearch = () => {
  if (searchTimer) clearTimeout(searchTimer)
  searchTimer = setTimeout(async () => {
    loading.value = true
    try {
      const params = {}
      if (searchName.value) params.name = searchName.value
      if (searchStatus.value) params.status = searchStatus.value
      if (searchMinArea.value !== null && searchMinArea.value !== undefined) params.min_area = searchMinArea.value
      if (searchMaxArea.value !== null && searchMaxArea.value !== undefined) params.max_area = searchMaxArea.value
      await plotStore.fetchPlots(params)
      await plotStore.fetchStats()
    } finally {
      loading.value = false
    }
  }, 300)
}

onMounted(async () => {
  loading.value = true
  try {
    await Promise.all([
      plotStore.fetchPlots(),
      plotStore.fetchStats(),
    ])
  } catch (e) {
    console.error('加载地块数据失败:', e)
  } finally {
    loading.value = false
  }
})
</script>

<style lang="scss" scoped>
@use '@/styles/variables' as *;

.plot-overview {
  display: flex;
  height: calc(100vh - #{$topbar-height} - #{$spacing-lg * 2});
  gap: $spacing-md;

  &__sidebar {
    width: 300px;
    flex-shrink: 0;
    display: flex;
    flex-direction: column;
    gap: $spacing-md;
    overflow-y: auto;
    padding-right: $spacing-xs;

    &::-webkit-scrollbar {
      width: 4px;
    }

    &::-webkit-scrollbar-thumb {
      background: rgba(0, 240, 255, 0.2);
      border-radius: 2px;
    }

    &::-webkit-scrollbar-track {
      background: transparent;
    }
  }

  &__map-area {
    flex: 1;
    min-width: 0;
    position: relative;
  }

  &__panel {
    flex-shrink: 0;
  }

  &__list-panel {
    flex: 1;
    min-height: 0;

    .hud-panel__content {
      display: flex;
      flex-direction: column;
      min-height: 0;
      overflow: hidden;
    }
  }

  &__loading {
    display: flex;
    align-items: center;
    justify-content: center;
    gap: $spacing-sm;
    padding: $spacing-lg;
    color: $text-muted;
    font-size: $font-size-sm;
  }

  &__empty {
    display: flex;
    align-items: center;
    justify-content: center;
    padding: $spacing-xl;
    color: $text-muted;
    font-size: $font-size-sm;
  }

  &__stat-row {
    display: flex;
    gap: $spacing-lg;
    margin-bottom: $spacing-md;
  }

  &__stat-item {
    display: flex;
    align-items: baseline;
    gap: $spacing-xs;
  }

  &__stat-value {
    font-family: $font-mono;
    font-size: $font-size-2xl;
    font-weight: 700;
    color: $accent-cyan;
    text-shadow: 0 0 8px rgba(0, 240, 255, 0.3);
  }

  &__stat-unit {
    font-family: $font-mono;
    font-size: $font-size-sm;
    color: $text-secondary;
    letter-spacing: 1px;
  }

  &__status-breakdown {
    display: flex;
    flex-direction: column;
    gap: $spacing-sm;
  }

  &__status-item {
    display: flex;
    align-items: center;
    gap: $spacing-sm;
  }

  &__status-label {
    font-size: $font-size-sm;
    color: $text-secondary;
    flex: 1;
  }

  &__status-count {
    font-family: $font-mono;
    font-size: $font-size-sm;
    color: $text-primary;
    font-weight: 600;
  }

  &__list {
    display: flex;
    flex-direction: column;
    gap: 2px;
    overflow-y: auto;
    flex: 1;
    min-height: 0;

    &::-webkit-scrollbar {
      width: 3px;
    }

    &::-webkit-scrollbar-thumb {
      background: rgba(0, 240, 255, 0.15);
      border-radius: 2px;
    }

    &::-webkit-scrollbar-track {
      background: transparent;
    }
  }

  &__list-item {
    display: flex;
    align-items: center;
    gap: $spacing-sm;
    padding: $spacing-sm $spacing-sm;
    border-radius: $radius-sm;
    cursor: pointer;
    transition: background $transition-fast;

    &:hover {
      background: rgba(0, 240, 255, 0.06);
    }
  }

  &__list-info {
    flex: 1;
    min-width: 0;
    display: flex;
    flex-direction: column;
    gap: 2px;
  }

  &__list-name {
    font-size: $font-size-sm;
    color: $text-primary;
    font-weight: 500;
    white-space: nowrap;
    overflow: hidden;
    text-overflow: ellipsis;
  }

  &__list-meta {
    font-family: $font-mono;
    font-size: $font-size-xs;
    color: $text-muted;
  }
}
</style>
