<template>
  <div class="console-stats">
    <div
      v-for="(card, idx) in statCards"
      :key="idx"
      class="console-stat-card"
      :class="`console-stat-card--${card.theme}`"
    >
      <div class="console-stat-card__corner console-stat-card__corner--tl" />
      <div class="console-stat-card__corner console-stat-card__corner--br" />
      <div class="console-stat-card__glow" />
      <div class="console-stat-card__content">
        <div class="console-stat-card__header">
          <el-icon :size="22"><component :is="card.icon" /></el-icon>
          <span class="console-stat-card__trend" v-if="card.trend">{{ card.trend }}</span>
        </div>
        <div class="console-stat-card__value">{{ card.value }}</div>
        <div class="console-stat-card__label">{{ card.label }}</div>
        <div class="console-stat-card__bar">
          <div class="console-stat-card__bar-fill" :style="{ width: card.barWidth + '%' }" />
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { Grid, DataLine, TrendCharts, Location } from '@element-plus/icons-vue'

defineProps({
  statCards: {
    type: Array,
    required: true,
  },
})
</script>

<style lang="scss" scoped>
@use '@/styles/variables' as *;

.console-stats {
  display: grid;
  grid-template-columns: repeat(4, 1fr);
  gap: $spacing-md;
}

.console-stat-card {
  position: relative;
  background: $bg-secondary;
  border: 1px solid $border-color;
  border-radius: $radius-md;
  padding: $spacing-md;
  overflow: hidden;
  transition: all $transition-fast;

  &:hover {
    border-color: rgba(0, 240, 255, 0.2);
    transform: translateY(-2px);
  }

  &__corner {
    position: absolute;
    width: 8px;
    height: 8px;
    pointer-events: none;

    &--tl { top: 0; left: 0; border-top: 1px solid; border-left: 1px solid; }
    &--br { bottom: 0; right: 0; border-bottom: 1px solid; border-right: 1px solid; }
  }

  &__glow {
    position: absolute;
    top: -50%;
    right: -50%;
    width: 100%;
    height: 100%;
    border-radius: 50%;
    opacity: 0.06;
    transition: opacity $transition-fast;
    pointer-events: none;
  }

  &--cyan {
    &:hover { box-shadow: 0 4px 20px rgba(0, 240, 255, 0.08); }
    .console-stat-card__corner { border-color: rgba(0, 240, 255, 0.3); }
    .console-stat-card__glow { background: radial-gradient(circle, $accent-cyan, transparent 70%); }
    .console-stat-card__header { color: $accent-cyan; }
    .console-stat-card__bar-fill { background: linear-gradient(90deg, $accent-cyan, rgba(0, 240, 255, 0.3)); }
  }

  &--green {
    &:hover { box-shadow: 0 4px 20px rgba(57, 255, 20, 0.08); }
    .console-stat-card__corner { border-color: rgba(57, 255, 20, 0.3); }
    .console-stat-card__glow { background: radial-gradient(circle, $accent-green, transparent 70%); }
    .console-stat-card__header { color: $accent-green; }
    .console-stat-card__bar-fill { background: linear-gradient(90deg, $accent-green, rgba(57, 255, 20, 0.3)); }
  }

  &--orange {
    &:hover { box-shadow: 0 4px 20px rgba(255, 107, 53, 0.08); }
    .console-stat-card__corner { border-color: rgba(255, 107, 53, 0.3); }
    .console-stat-card__glow { background: radial-gradient(circle, $accent-orange, transparent 70%); }
    .console-stat-card__header { color: $accent-orange; }
    .console-stat-card__bar-fill { background: linear-gradient(90deg, $accent-orange, rgba(255, 107, 53, 0.3)); }
  }

  &__content {
    position: relative;
    z-index: 1;
  }

  &__header {
    display: flex;
    align-items: center;
    justify-content: space-between;
    margin-bottom: $spacing-sm;
    font-family: $font-mono;
    font-size: $font-size-xs;
  }

  &__trend {
    color: $text-muted;
    letter-spacing: 1px;
  }

  &__value {
    font-family: $font-mono;
    font-size: $font-size-2xl;
    font-weight: 700;
    color: $text-primary;
    line-height: 1;
    margin-bottom: $spacing-xs;
  }

  &__label {
    font-size: $font-size-sm;
    color: $text-muted;
    margin-bottom: $spacing-sm;
  }

  &__bar {
    height: 3px;
    background: rgba(255, 255, 255, 0.05);
    border-radius: 2px;
    overflow: hidden;
  }

  &__bar-fill {
    height: 100%;
    border-radius: 2px;
    transition: width 1s ease;
  }
}

@media (max-width: 1024px) {
  .console-stats { grid-template-columns: repeat(2, 1fr); }
}

@media (max-width: 640px) {
  .console-stats { grid-template-columns: 1fr; }
}
</style>
