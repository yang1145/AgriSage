<template>
  <div class="console-status-panel">
    <div class="console-status-panel__header">
      <span class="console-status-panel__title">
        <span class="console-status-panel__title-icon">◉</span>
        系统状态
      </span>
      <span class="console-status-panel__subtitle">SYSTEM STATUS</span>
    </div>
    <div class="console-status-list">
      <div v-for="(status, idx) in systemStatuses" :key="idx" class="console-status-item">
        <div class="console-status-item__left">
          <HudStatusLight :status="status.status" />
          <span class="console-status-item__label">{{ status.label }}</span>
        </div>
        <div class="console-status-item__right">
          <span class="console-status-item__value">{{ status.value }}</span>
          <span class="console-status-item__detail">{{ status.detail }}</span>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { computed } from 'vue'
import HudStatusLight from '@/components/hud/HudStatusLight.vue'
import { usePlotStats } from '@/composables/usePlotStats'

const stats = usePlotStats()

const systemStatuses = computed(() => [
  { label: '数据库连接', value: '正常', detail: 'SQLite', status: 'growing' },
  { label: '地图服务', value: '在线', detail: '离线瓦片', status: 'growing' },
  { label: '数据状态', value: stats.value.plotCount > 0 ? '已有数据' : '暂无数据', detail: `${stats.value.plotCount} 地块`, status: stats.value.plotCount > 0 ? 'growing' : 'idle' },
  { label: '系统版本', value: 'v1.0.0', detail: '最新', status: 'idle' },
])
</script>

<style lang="scss" scoped>
@use '@/styles/variables' as *;

.console-status-panel {
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
    background: linear-gradient(90deg, transparent, rgba(255, 107, 53, 0.3), transparent);
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
    color: $accent-orange;
    font-size: $font-size-sm;
  }

  &__subtitle {
    font-family: $font-mono;
    font-size: $font-size-xs;
    color: $text-muted;
    letter-spacing: 1px;
  }
}

.console-status-list {
  display: flex;
  flex-direction: column;
  gap: $spacing-sm;
}

.console-status-item {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: $spacing-sm $spacing-md;
  background: rgba(255, 255, 255, 0.02);
  border: 1px solid rgba(255, 255, 255, 0.04);
  border-radius: $radius-sm;
  transition: all $transition-fast;

  &:hover {
    border-color: rgba(0, 240, 255, 0.1);
    background: rgba(0, 240, 255, 0.02);
  }

  &__left {
    display: flex;
    align-items: center;
    gap: $spacing-sm;
  }

  &__label {
    font-size: $font-size-sm;
    color: $text-secondary;
  }

  &__right {
    display: flex;
    align-items: center;
    gap: $spacing-sm;
  }

  &__value {
    font-family: $font-mono;
    font-size: $font-size-sm;
    color: $accent-cyan;
  }

  &__detail {
    font-family: $font-mono;
    font-size: $font-size-xs;
    color: $text-muted;
  }
}
</style>
