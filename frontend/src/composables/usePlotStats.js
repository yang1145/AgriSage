import { ref, computed, provide, inject, onMounted, onUnmounted } from 'vue'
import { plotApi } from '@/api/plot'
import * as echarts from 'echarts'

const PLOT_STATS_KEY = Symbol('plotStats')

export function providePlotStats() {
  const stats = ref({
    plotCount: 0,
    totalArea: 0,
    growingCount: 0,
    harvestedCount: 0,
    idleCount: 0,
  })

  provide(PLOT_STATS_KEY, stats)

  let chartInstance = null

  const loadStats = async () => {
    try {
      const res = await plotApi.getPlotStats()
      if (res.data) {
        stats.value = {
          plotCount: res.data.plot_count || 0,
          totalArea: res.data.total_area || 0,
          growingCount: res.data.status_distribution?.growing || 0,
          harvestedCount: res.data.status_distribution?.harvested || 0,
          idleCount: res.data.status_distribution?.idle || 0,
        }
      }
    } catch {
      // ignore
    }
  }

  const initChart = (chartRef) => {
    if (!chartRef) return
    chartInstance = echarts.init(chartRef, 'dark', { renderer: 'canvas' })
    const option = {
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
          data: [
            { value: stats.value.growingCount, name: '种植中', itemStyle: { color: '#39ff14' } },
            { value: stats.value.harvestedCount, name: '已收割', itemStyle: { color: '#ff6b35' } },
            { value: stats.value.idleCount, name: '闲置', itemStyle: { color: '#4a5568' } },
          ],
        },
      ],
    }
    chartInstance.setOption(option)
  }

  const updateChart = () => {
    if (!chartInstance) return
    chartInstance.setOption({
      series: [{
        data: [
          { value: stats.value.growingCount, name: '种植中', itemStyle: { color: '#39ff14' } },
          { value: stats.value.harvestedCount, name: '已收割', itemStyle: { color: '#ff6b35' } },
          { value: stats.value.idleCount, name: '闲置', itemStyle: { color: '#4a5568' } },
        ],
      }],
    })
  }

  const handleResize = () => {
    if (chartInstance) chartInstance.resize()
  }

  onMounted(() => {
    loadStats()
    window.addEventListener('resize', handleResize)
  })

  onUnmounted(() => {
    if (chartInstance) {
      chartInstance.dispose()
      chartInstance = null
    }
    window.removeEventListener('resize', handleResize)
  })

  return stats
}

export function usePlotStats() {
  const stats = inject(PLOT_STATS_KEY)
  if (!stats) {
    throw new Error('usePlotStats must be used within a component that provides plotStats')
  }
  return stats
}
