<template>
  <div class="console-chart-panel">
    <div class="console-chart-panel__header">
      <span class="console-chart-panel__title">
        <span class="console-chart-panel__title-icon">◈</span>
        地块状态分布
      </span>
      <span class="console-chart-panel__subtitle">STATUS DISTRIBUTION</span>
    </div>
    <div ref="chartRef" class="console-chart" />
  </div>
</template>

<script setup>
import { ref, onMounted, onUnmounted, nextTick, watch } from 'vue'
import { usePlotStats } from '@/composables/usePlotStats'
import * as echarts from 'echarts'

const chartRef = ref(null)
const stats = usePlotStats()

let chartInstance = null

const baseOption = {
  backgroundColor: 'transparent',
  tooltip: {
    trigger: 'item',
    backgroundColor: 'rgba(10, 15, 20, 0.9)',
    borderColor: '#1a2332',
    textStyle: { color: '#e0e6ed', fontFamily: "'Roboto Mono', monospace" },
    formatter: '{b}: {c} ({d}%)',
  },
  legend: {
    orient: 'vertical',
    right: 10,
    top: 'center',
    textStyle: { color: '#8b9bb4', fontFamily: "'Roboto Mono', monospace", fontSize: 12 },
    itemWidth: 10,
    itemHeight: 10,
    itemGap: 16,
  },
  series: [
    {
      name: '地块状态',
      type: 'pie',
      radius: ['45%', '70%'],
      center: ['35%', '50%'],
      avoidLabelOverlap: false,
      itemStyle: {
        borderRadius: 4,
        borderColor: '#0a0f14',
        borderWidth: 2,
      },
      label: { show: false },
      emphasis: {
        label: {
          show: true,
          fontSize: 14,
          fontWeight: 'bold',
          color: '#e0e6ed',
          fontFamily: "'Roboto Mono', monospace",
        },
        itemStyle: {
          shadowBlur: 10,
          shadowOffsetX: 0,
          shadowColor: 'rgba(0, 240, 255, 0.3)',
        },
      },
      labelLine: { show: false },
      data: [],
    },
  ],
}

const initChart = async () => {
  await nextTick()
  if (!chartRef.value || !stats.value) return
  chartInstance = echarts.init(chartRef.value, 'dark', { renderer: 'canvas' })
  updateChart()
}

const updateChart = () => {
  if (!chartInstance) return
  chartInstance.setOption({
    ...baseOption,
    series: [{
      ...baseOption.series[0],
      data: [
        { value: stats.value.growingCount, name: '种植中', itemStyle: { color: '#39ff14' } },
        { value: stats.value.harvestedCount, name: '已收割', itemStyle: { color: '#ff6b35' } },
        { value: stats.value.idleCount, name: '闲置', itemStyle: { color: '#4a5568' } },
      ],
    }],
  })
}

// 数据变化时更新图表
watch(() => stats.value, () => {
  if (chartInstance) {
    updateChart()
  } else if (chartRef.value) {
    initChart()
  }
}, { deep: true })

onMounted(async () => {
  // 等待 stats 数据加载完成后再初始化图表
  await nextTick()
  // 如果数据还没加载，等一下再初始化
  const tryInit = () => {
    if (chartRef.value && stats.value) {
      initChart()
    } else {
      setTimeout(tryInit, 100)
    }
  }
  tryInit()

  window.addEventListener('resize', handleResize)
})

const handleResize = () => {
  if (chartInstance) chartInstance.resize()
}

onUnmounted(() => {
  window.removeEventListener('resize', handleResize)
  if (chartInstance) {
    chartInstance.dispose()
    chartInstance = null
  }
})
</script>

<style lang="scss" scoped>
@use '@/styles/variables' as *;

.console-chart-panel {
  background: $bg-secondary;
  border: 1px solid $border-color;
  border-radius: $radius-md;
  padding: $spacing-lg;
  position: relative;
  overflow: hidden;

  &::before {
    content: '';
    position: absolute;
    top: 0;
    left: 0;
    right: 0;
    height: 1px;
    background: linear-gradient(90deg, transparent, rgba(0, 240, 255, 0.3), transparent);
  }

  &__header {
    display: flex;
    align-items: center;
    justify-content: space-between;
    margin-bottom: $spacing-md;
  }

  &__title {
    display: flex;
    align-items: center;
    gap: $spacing-sm;
    font-size: $font-size-md;
    font-weight: 600;
    color: $text-primary;
  }

  &__title-icon {
    color: $accent-cyan;
    font-size: $font-size-sm;
  }

  &__subtitle {
    font-family: $font-mono;
    font-size: $font-size-xs;
    color: $text-muted;
    letter-spacing: 1px;
  }
}

.console-chart {
  width: 100%;
  height: 240px;
}
</style>
