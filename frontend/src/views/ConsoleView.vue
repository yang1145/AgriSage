<template>
  <div class="console-view">
    <div class="console-bg-grid" />
    <div class="console-scanline" />

    <ConsoleHero class="console-hero" />

    <ConsoleStats class="console-stats" :stat-cards="statCards" />

    <div class="console-mid">
      <ConsoleChart />
      <ConsoleShortcuts />
    </div>

    <div class="console-bottom">
      <ConsoleStatus />
      <ConsoleGuide />
    </div>
  </div>
</template>

<script setup>
import { computed } from 'vue'
import { providePlotStats } from '@/composables/usePlotStats'
import ConsoleHero from '@/components/console/ConsoleHero.vue'
import ConsoleStats from '@/components/console/ConsoleStats.vue'
import ConsoleChart from '@/components/console/ConsoleChart.vue'
import ConsoleShortcuts from '@/components/console/ConsoleShortcuts.vue'
import ConsoleStatus from '@/components/console/ConsoleStatus.vue'
import ConsoleGuide from '@/components/console/ConsoleGuide.vue'

const stats = providePlotStats()

const statCards = computed(() => [
  {
    icon: 'Grid',
    value: stats.value.plotCount,
    label: '地块总数',
    theme: 'cyan',
    trend: '+新增',
    barWidth: Math.min(100, stats.value.plotCount * 10),
  },
  {
    icon: 'DataLine',
    value: stats.value.totalArea?.toFixed(1) || '0.0',
    label: '总面积（亩）',
    theme: 'green',
    trend: null,
    barWidth: Math.min(100, (stats.value.totalArea || 0) * 2),
  },
  {
    icon: 'TrendCharts',
    value: stats.value.growingCount,
    label: '种植中',
    theme: 'cyan',
    trend: '活跃',
    barWidth: stats.value.plotCount > 0 ? (stats.value.growingCount / stats.value.plotCount) * 100 : 0,
  },
  {
    icon: 'Location',
    value: stats.value.harvestedCount,
    label: '已收割',
    theme: 'orange',
    trend: '完成',
    barWidth: stats.value.plotCount > 0 ? (stats.value.harvestedCount / stats.value.plotCount) * 100 : 0,
  },
])
</script>

<style lang="scss" scoped>
@use '@/styles/variables' as *;

.console-view {
  position: relative;
  padding: $spacing-lg;
  max-width: 1400px;
  margin: 0 auto;
  overflow: hidden;
}

.console-bg-grid {
  position: fixed;
  inset: 0;
  pointer-events: none;
  z-index: 0;
  opacity: 0.3;
  background-image:
    linear-gradient(rgba(0, 240, 255, 0.03) 1px, transparent 1px),
    linear-gradient(90deg, rgba(0, 240, 255, 0.03) 1px, transparent 1px);
  background-size: 40px 40px;
  mask-image: radial-gradient(ellipse at center, black 40%, transparent 80%);
}

.console-scanline {
  position: fixed;
  inset: 0;
  pointer-events: none;
  z-index: 9999;
  background: repeating-linear-gradient(
    0deg,
    transparent,
    transparent 2px,
    rgba(0, 240, 255, 0.015) 2px,
    rgba(0, 240, 255, 0.015) 4px
  );
}

.console-hero {
  margin-bottom: $spacing-xl;
}

.console-stats {
  margin-bottom: $spacing-xl;
}

.console-mid {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: $spacing-xl;
  margin-bottom: $spacing-xl;
}

.console-bottom {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: $spacing-xl;
}

@media (max-width: 1024px) {
  .console-mid { grid-template-columns: 1fr; }
  .console-bottom { grid-template-columns: 1fr; }
}
</style>
