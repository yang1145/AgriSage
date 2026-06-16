<template>
  <div class="dashboard">
    <!-- Top bar -->
    <div class="dashboard__topbar">
      <div class="dashboard__topbar-left">
        <span class="dashboard__topbar-title">桂收 · 数据总览</span>
      </div>
      <div class="dashboard__topbar-right">
        <span class="dashboard__clock">{{ currentTime }}</span>
      </div>
    </div>

    <!-- 3-column layout -->
    <div class="dashboard__body">
      <!-- LEFT COLUMN -->
      <div class="dashboard__col dashboard__col--left">
        <!-- 地块概况 -->
        <HudCard title="地块概况" variant="cyan" class="dash-card">
          <div class="stat-row">
            <div class="stat-item">
              <div class="hud-data-label">总面积</div>
              <div class="hud-data-value hud-data-value--sm">{{ stats.totalArea || 0 }} <small>亩</small></div>
            </div>
            <div class="stat-item">
              <div class="hud-data-label">地块数</div>
              <div class="hud-data-value hud-data-value--sm">{{ stats.plotCount || 0 }} <small>块</small></div>
            </div>
          </div>
          <div class="status-row">
            <div class="status-item">
              <HudStatusLight status="idle" />
              <span class="status-label">闲置</span>
              <span class="status-count">{{ stats.idleCount || 0 }}</span>
            </div>
            <div class="status-item">
              <HudStatusLight status="growing" />
              <span class="status-label">种植中</span>
              <span class="status-count">{{ stats.growingCount || 0 }}</span>
            </div>
            <div class="status-item">
              <HudStatusLight status="harvested" />
              <span class="status-label">已收割</span>
              <span class="status-count">{{ stats.harvestedCount || 0 }}</span>
            </div>
          </div>
        </HudCard>

        <!-- 品种分布 -->
        <HudCard title="品种分布" variant="green" class="dash-card">
          <div ref="varietyChartRef" class="chart-container" />
        </HudCard>

        <!-- 产量趋势 -->
        <HudCard title="产量趋势" class="dash-card">
          <div ref="yieldChartRef" class="chart-container" />
        </HudCard>
      </div>

      <!-- CENTER COLUMN -->
      <div class="dashboard__col dashboard__col--center">
        <!-- Top stat cards -->
        <div class="center-stats">
          <div class="center-stat-card">
            <div class="hud-data-label">总种植面积</div>
            <div class="hud-data-value hud-data-value--lg">{{ stats.growingArea || 0 }}<small>亩</small></div>
          </div>
          <div class="center-stat-card">
            <div class="hud-data-label">活跃地块数</div>
            <div class="hud-data-value hud-data-value--lg hud-data-value--green">{{ stats.growingCount || 0 }}<small>块</small></div>
          </div>
          <div class="center-stat-card">
            <div class="hud-data-label">本季产量</div>
            <div class="hud-data-value hud-data-value--lg hud-data-value--orange">{{ stats.seasonYield || 0 }}<small>吨</small></div>
          </div>
        </div>

        <!-- Map -->
        <div class="center-map">
          <PlotMap :plots="plotStore.plots" @select="onPlotSelect" />
        </div>

        <!-- Recent activities -->
        <HudCard title="近期农事记录" variant="cyan" class="dash-card dash-card--activities">
          <div class="activity-list">
            <div v-if="recentActivities.length === 0" class="activity-empty">暂无农事记录</div>
            <div
              v-for="(act, idx) in recentActivities"
              :key="idx"
              class="activity-item"
            >
              <div class="activity-item__type">
                <span class="hud-badge" :class="activityBadgeClass(act.type)">{{ activityTypeLabel(act.type) }}</span>
              </div>
              <div class="activity-item__info">
                <span class="activity-item__plot">{{ act.plotName || '-' }}</span>
                <span class="activity-item__date">{{ act.date || '-' }}</span>
              </div>
              <div class="activity-item__desc">{{ act.description || '-' }}</div>
            </div>
          </div>
        </HudCard>
      </div>

      <!-- RIGHT COLUMN -->
      <div class="dashboard__col dashboard__col--right">
        <!-- 近期农事 Timeline -->
        <HudCard title="近期农事" variant="cyan" class="dash-card">
          <HudTimeline :items="timelineItems" />
        </HudCard>

        <!-- 采收统计 -->
        <HudCard title="采收统计" variant="orange" class="dash-card">
          <div ref="harvestChartRef" class="chart-container" />
        </HudCard>

        <!-- 预警信息 -->
        <HudCard title="预警信息" variant="orange" class="dash-card">
          <div v-if="alerts.length === 0" class="alert-empty">
            <HudStatusLight status="growing" />
            <span>暂无预警</span>
          </div>
          <div v-else class="alert-list">
            <div v-for="(alert, idx) in alerts" :key="idx" class="alert-item">
              <span class="alert-item__severity">⚠</span>
              <div class="alert-item__content">
                <div class="alert-item__title">{{ alert.title }}</div>
                <div class="alert-item__detail">{{ alert.detail }}</div>
              </div>
            </div>
          </div>
        </HudCard>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted, onUnmounted, nextTick } from 'vue'
import { useRouter } from 'vue-router'
import * as echarts from 'echarts'
import { usePlotStore } from '@/stores/plot'
import { plotApi } from '@/api/plot'
import { plantingApi } from '@/api/planting'
import HudCard from '@/components/hud/HudCard.vue'
import HudStatusLight from '@/components/hud/HudStatusLight.vue'
import HudTimeline from '@/components/hud/HudTimeline.vue'
import PlotMap from '@/components/map/PlotMap.vue'

const router = useRouter()
const plotStore = usePlotStore()

// --- Clock ---
const currentTime = ref('')
let clockTimer = null

const updateClock = () => {
  const now = new Date()
  const week = ['星期日', '星期一', '星期二', '星期三', '星期四', '星期五', '星期六']
  const pad = (n) => String(n).padStart(2, '0')
  currentTime.value = `${now.getFullYear()}-${pad(now.getMonth() + 1)}-${pad(now.getDate())} ${pad(now.getHours())}:${pad(now.getMinutes())}:${pad(now.getSeconds())} ${week[now.getDay()]}`
}

// --- Stats ---
const stats = ref({
  totalArea: 0,
  plotCount: 0,
  idleCount: 0,
  growingCount: 0,
  harvestedCount: 0,
  growingArea: 0,
  seasonYield: 0,
  varietyDistribution: [],
  yieldTrend: [],
  harvestStats: [],
})

const recentActivities = ref([])
const alerts = ref([])

// --- Chart refs ---
const varietyChartRef = ref(null)
const yieldChartRef = ref(null)
const harvestChartRef = ref(null)
let varietyChart = null
let yieldChart = null
let harvestChart = null

// --- Timeline ---
const timelineItems = computed(() =>
  recentActivities.value.slice(0, 8).map((act) => ({
    time: act.date || '',
    label: `${activityTypeLabel(act.type)} - ${act.plotName || ''}`,
    description: act.description || '',
    active: act.type === 'pest_disease',
  }))
)

// --- Activity helpers ---
const activityTypeLabel = (type) => {
  const map = {
    fertilization: '施肥',
    irrigation: '灌溉',
    pest_disease: '病虫害',
    harvest: '采收',
  }
  return map[type] || type || '农事'
}

const activityBadgeClass = (type) => {
  const map = {
    fertilization: 'hud-badge--green',
    irrigation: 'hud-badge--cyan',
    pest_disease: 'hud-badge--orange',
    harvest: 'hud-badge--orange',
  }
  return map[type] || 'hud-badge--gray'
}

// --- Plot select ---
const onPlotSelect = (plotId) => {
  router.push(`/plots/${plotId}`)
}

// --- Chart theme colors ---
const chartColors = ['#00f0ff', '#39ff14', '#ff6b35', '#4a5568', '#8b9bb4']

// --- Init charts ---
const initVarietyChart = () => {
  if (!varietyChartRef.value) return
  varietyChart = echarts.init(varietyChartRef.value)
  const data = stats.value.varietyDistribution.length
    ? stats.value.varietyDistribution
    : [
        { name: '桂糖42号', value: 35 },
        { name: '桂糖44号', value: 25 },
        { name: '新台糖22号', value: 20 },
        { name: '粤糖93-159', value: 12 },
        { name: '其他', value: 8 },
      ]
  varietyChart.setOption({
    tooltip: {
      trigger: 'item',
      backgroundColor: 'rgba(13,17,23,0.9)',
      borderColor: '#1a2332',
      textStyle: { color: '#e0e6ed', fontSize: 12 },
    },
    color: chartColors,
    series: [{
      type: 'pie',
      radius: ['40%', '70%'],
      center: ['50%', '50%'],
      avoidLabelOverlap: true,
      itemStyle: {
        borderColor: '#0a0f14',
        borderWidth: 2,
        borderRadius: 4,
      },
      label: {
        color: '#8b9bb4',
        fontSize: 11,
        formatter: '{b}\n{d}%',
      },
      labelLine: {
        lineStyle: { color: '#1a2332' },
      },
      emphasis: {
        label: { color: '#00f0ff', fontSize: 13 },
        itemStyle: {
          shadowBlur: 10,
          shadowColor: 'rgba(0,240,255,0.3)',
        },
      },
      data,
    }],
  })
}

const initYieldChart = () => {
  if (!yieldChartRef.value) return
  yieldChart = echarts.init(yieldChartRef.value)
  const months = ['1月', '2月', '3月', '4月', '5月', '6月', '7月', '8月', '9月', '10月', '11月', '12月']
  const data = stats.value.yieldTrend.length
    ? stats.value.yieldTrend
    : [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
  yieldChart.setOption({
    tooltip: {
      trigger: 'axis',
      backgroundColor: 'rgba(13,17,23,0.9)',
      borderColor: '#1a2332',
      textStyle: { color: '#e0e6ed', fontSize: 12 },
    },
    grid: { top: 20, right: 16, bottom: 24, left: 40 },
    xAxis: {
      type: 'category',
      data: months,
      axisLine: { lineStyle: { color: '#1a2332' } },
      axisLabel: { color: '#4a5568', fontSize: 10 },
      axisTick: { show: false },
    },
    yAxis: {
      type: 'value',
      splitLine: { lineStyle: { color: '#1a2332' } },
      axisLabel: { color: '#4a5568', fontSize: 10 },
      axisLine: { show: false },
    },
    series: [{
      type: 'line',
      data,
      smooth: true,
      symbol: 'circle',
      symbolSize: 6,
      lineStyle: { color: '#00f0ff', width: 2 },
      itemStyle: { color: '#00f0ff', borderColor: '#0a0f14', borderWidth: 2 },
      areaStyle: {
        color: new echarts.graphic.LinearGradient(0, 0, 0, 1, [
          { offset: 0, color: 'rgba(0,240,255,0.25)' },
          { offset: 1, color: 'rgba(0,240,255,0.02)' },
        ]),
      },
    }],
  })
}

const initHarvestChart = () => {
  if (!harvestChartRef.value) return
  harvestChart = echarts.init(harvestChartRef.value)
  const categories = stats.value.harvestStats.length
    ? stats.value.harvestStats.map((s) => s.name)
    : ['1月', '2月', '3月', '4月', '5月', '6月']
  const data = stats.value.harvestStats.length
    ? stats.value.harvestStats.map((s) => s.value)
    : [0, 0, 0, 0, 0, 0]
  harvestChart.setOption({
    tooltip: {
      trigger: 'axis',
      backgroundColor: 'rgba(13,17,23,0.9)',
      borderColor: '#1a2332',
      textStyle: { color: '#e0e6ed', fontSize: 12 },
    },
    grid: { top: 20, right: 16, bottom: 24, left: 40 },
    xAxis: {
      type: 'category',
      data: categories,
      axisLine: { lineStyle: { color: '#1a2332' } },
      axisLabel: { color: '#4a5568', fontSize: 10 },
      axisTick: { show: false },
    },
    yAxis: {
      type: 'value',
      splitLine: { lineStyle: { color: '#1a2332' } },
      axisLabel: { color: '#4a5568', fontSize: 10 },
      axisLine: { show: false },
    },
    series: [{
      type: 'bar',
      data,
      barWidth: '50%',
      itemStyle: {
        color: new echarts.graphic.LinearGradient(0, 0, 0, 1, [
          { offset: 0, color: '#ff6b35' },
          { offset: 1, color: 'rgba(255,107,53,0.2)' },
        ]),
        borderRadius: [2, 2, 0, 0],
      },
      emphasis: {
        itemStyle: {
          shadowBlur: 10,
          shadowColor: 'rgba(255,107,53,0.4)',
        },
      },
    }],
  })
}

// --- Resize handler ---
const handleResize = () => {
  varietyChart?.resize()
  yieldChart?.resize()
  harvestChart?.resize()
}

// --- Fetch data ---
const fetchDashboardData = async () => {
  try {
    // Fetch plots and stats in parallel
    await Promise.all([
      plotStore.fetchPlots(),
      plotStore.fetchStats(),
    ])

    const s = plotStore.stats || {}
    const sd = s.status_distribution || {}
    stats.value = {
      totalArea: s.total_area || 0,
      plotCount: s.plot_count || 0,
      idleCount: sd.idle || 0,
      growingCount: sd.growing || 0,
      harvestedCount: sd.harvested || 0,
      growingArea: s.growing_area || 0,
      seasonYield: s.season_yield || 0,
      varietyDistribution: s.variety_distribution || [],
      yieldTrend: s.yield_trend || [],
      harvestStats: s.harvest_stats || [],
    }

    // Build recent activities from plots with active cycles
    const activities = []
    for (const plot of plotStore.plots) {
      if (plot.latest_activity) {
        activities.push({
          type: plot.latest_activity.type,
          plotName: plot.name,
          date: plot.latest_activity.date,
          description: plot.latest_activity.description,
        })
      }
    }
    recentActivities.value = activities.slice(0, 20)

    // Build alerts from pest/disease records
    const alertItems = []
    for (const plot of plotStore.plots) {
      if (plot.alerts && plot.alerts.length) {
        for (const a of plot.alerts) {
          if (a.severity === '重') {
            alertItems.push({
              title: `${plot.name} - ${a.type || '病虫害预警'}`,
              detail: a.description || '',
            })
          }
        }
      }
    }
    alerts.value = alertItems.slice(0, 10)
  } catch {
    // Use default empty data, charts will show placeholder
  }
}

// --- Lifecycle ---
onMounted(async () => {
  updateClock()
  clockTimer = setInterval(updateClock, 1000)

  await fetchDashboardData()

  await nextTick()
  initVarietyChart()
  initYieldChart()
  initHarvestChart()

  window.addEventListener('resize', handleResize)
})

onUnmounted(() => {
  clearInterval(clockTimer)
  varietyChart?.dispose()
  yieldChart?.dispose()
  harvestChart?.dispose()
  window.removeEventListener('resize', handleResize)
})
</script>

<style lang="scss" scoped>
@use '@/styles/variables' as *;

.dashboard {
  width: 100%;
  height: 100%;
  display: flex;
  flex-direction: column;
  background: $bg-primary;
  color: $text-primary;
  overflow: hidden;
}

// --- Top Bar ---
.dashboard__topbar {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: $spacing-md $spacing-lg;
  background: rgba(0, 240, 255, 0.03);
  border-bottom: 1px solid $border-color;
  flex-shrink: 0;
}

.dashboard__topbar-title {
  font-family: $font-mono;
  font-size: $font-size-lg;
  font-weight: 700;
  color: $accent-cyan;
  letter-spacing: 3px;
  text-shadow: 0 0 8px rgba(0, 240, 255, 0.3);
}

.dashboard__clock {
  font-family: $font-mono;
  font-size: $font-size-sm;
  color: $text-secondary;
  letter-spacing: 1px;
}

// --- Body (3 columns) ---
.dashboard__body {
  flex: 1;
  display: flex;
  gap: $spacing-md;
  padding: $spacing-md;
  overflow: hidden;
  min-height: 0;
}

.dashboard__col {
  display: flex;
  flex-direction: column;
  gap: $spacing-md;
  overflow-y: auto;
  min-height: 0;

  &--left {
    width: 25%;
    flex-shrink: 0;
  }

  &--center {
    flex: 1;
    min-width: 0;
  }

  &--right {
    width: 25%;
    flex-shrink: 0;
  }
}

// --- Card ---
.dash-card {
  flex-shrink: 0;
}

.dash-card--activities {
  flex: 1;
  min-height: 0;

  :deep(.hud-card__body) {
    overflow-y: auto;
    max-height: 200px;
  }
}

// --- Stat Row (left column) ---
.stat-row {
  display: flex;
  gap: $spacing-lg;
  margin-bottom: $spacing-md;
}

.stat-item {
  flex: 1;

  small {
    font-size: $font-size-xs;
    color: $text-muted;
    margin-left: 2px;
  }
}

.status-row {
  display: flex;
  gap: $spacing-lg;
}

.status-item {
  display: flex;
  align-items: center;
  gap: $spacing-xs;
}

.status-label {
  font-size: $font-size-sm;
  color: $text-secondary;
}

.status-count {
  font-family: $font-mono;
  font-size: $font-size-sm;
  font-weight: 600;
  color: $text-primary;
}

// --- Chart Container ---
.chart-container {
  width: 100%;
  height: 180px;
}

// --- Center Stats ---
.center-stats {
  display: flex;
  gap: $spacing-md;
  flex-shrink: 0;
}

.center-stat-card {
  flex: 1;
  background: $bg-card;
  border: 1px solid $border-color;
  border-radius: $radius-md;
  padding: $spacing-md $spacing-lg;
  position: relative;
  overflow: hidden;

  // Corner decoration
  &::after {
    content: '';
    position: absolute;
    top: 0;
    left: 0;
    width: 16px;
    height: 16px;
    border-top: 2px solid $accent-cyan;
    border-left: 2px solid $accent-cyan;
    pointer-events: none;
  }

  small {
    font-size: $font-size-sm;
    color: $text-muted;
    margin-left: 4px;
    font-weight: 400;
  }
}

// --- Center Map ---
.center-map {
  flex: 1;
  min-height: 300px;
  border-radius: $radius-md;
  overflow: hidden;
  border: 1px solid $border-color;
}

// --- Activity List ---
.activity-list {
  display: flex;
  flex-direction: column;
  gap: $spacing-sm;
}

.activity-empty {
  text-align: center;
  color: $text-muted;
  font-size: $font-size-sm;
  padding: $spacing-lg 0;
}

.activity-item {
  display: flex;
  align-items: center;
  gap: $spacing-sm;
  padding: $spacing-xs 0;
  border-bottom: 1px solid rgba($border-color, 0.5);

  &:last-child {
    border-bottom: none;
  }

  &__info {
    display: flex;
    flex-direction: column;
    min-width: 0;
  }

  &__plot {
    font-size: $font-size-sm;
    color: $text-primary;
    white-space: nowrap;
    overflow: hidden;
    text-overflow: ellipsis;
  }

  &__date {
    font-family: $font-mono;
    font-size: $font-size-xs;
    color: $text-muted;
  }

  &__desc {
    font-size: $font-size-xs;
    color: $text-secondary;
    white-space: nowrap;
    overflow: hidden;
    text-overflow: ellipsis;
    flex: 1;
    min-width: 0;
  }
}

// --- Alert List ---
.alert-empty {
  display: flex;
  align-items: center;
  gap: $spacing-sm;
  color: $accent-green;
  font-size: $font-size-sm;
  padding: $spacing-md 0;
}

.alert-list {
  display: flex;
  flex-direction: column;
  gap: $spacing-sm;
}

.alert-item {
  display: flex;
  gap: $spacing-sm;
  padding: $spacing-xs 0;
  border-bottom: 1px solid rgba($border-color, 0.5);

  &:last-child {
    border-bottom: none;
  }

  &__severity {
    color: $accent-orange;
    font-size: $font-size-md;
    flex-shrink: 0;
  }

  &__content {
    flex: 1;
    min-width: 0;
  }

  &__title {
    font-size: $font-size-sm;
    color: $accent-orange;
    font-weight: 500;
  }

  &__detail {
    font-size: $font-size-xs;
    color: $text-secondary;
    margin-top: 2px;
  }
}

// --- HUD Badge (local) ---
.hud-badge {
  display: inline-flex;
  align-items: center;
  padding: 2px $spacing-sm;
  font-family: $font-mono;
  font-size: $font-size-xs;
  letter-spacing: 1px;
  border-radius: $radius-sm;
  border: 1px solid;
  white-space: nowrap;

  &--cyan {
    color: $accent-cyan;
    border-color: rgba(0, 240, 255, 0.4);
    background: rgba(0, 240, 255, 0.08);
  }

  &--orange {
    color: $accent-orange;
    border-color: rgba(255, 107, 53, 0.4);
    background: rgba(255, 107, 53, 0.08);
  }

  &--green {
    color: $accent-green;
    border-color: rgba(57, 255, 20, 0.4);
    background: rgba(57, 255, 20, 0.08);
  }

  &--gray {
    color: $text-muted;
    border-color: rgba(74, 85, 104, 0.4);
    background: rgba(74, 85, 104, 0.08);
  }
}

// --- HUD Data helpers (local) ---
.hud-data-label {
  font-family: $font-mono;
  font-size: $font-size-xs;
  color: $text-muted;
  text-transform: uppercase;
  letter-spacing: 1.5px;
  margin-bottom: $spacing-xs;
}

.hud-data-value {
  font-family: $font-mono;
  font-size: $font-size-xl;
  font-weight: 700;
  color: $accent-cyan;
  text-shadow: 0 0 10px rgba(0, 240, 255, 0.5);

  &--green {
    color: $accent-green;
    text-shadow: 0 0 10px rgba(57, 255, 20, 0.5);
  }

  &--orange {
    color: $accent-orange;
    text-shadow: 0 0 10px rgba(255, 107, 53, 0.5);
  }

  &--sm {
    font-size: $font-size-md;
  }

  &--lg {
    font-size: $font-size-2xl;
  }
}
</style>
