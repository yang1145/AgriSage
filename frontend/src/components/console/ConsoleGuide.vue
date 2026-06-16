<template>
  <div class="console-guide-panel">
    <div class="console-guide-panel__header">
      <span class="console-guide-panel__title">
        <span class="console-guide-panel__title-icon">◐</span>
        操作指南
      </span>
      <span class="console-guide-panel__subtitle">OPERATION GUIDE</span>
    </div>
    <div class="console-guide-list">
      <div
        v-for="(guide, idx) in guides"
        :key="idx"
        class="console-guide-item"
        @click="guide.path ? router.push(guide.path) : null"
        :class="{ 'console-guide-item--clickable': guide.path }"
      >
        <span class="console-guide-item__num">{{ String(idx + 1).padStart(2, '0') }}</span>
        <div class="console-guide-item__content">
          <div class="console-guide-item__title">{{ guide.title }}</div>
          <div class="console-guide-item__desc">{{ guide.desc }}</div>
        </div>
        <div v-if="guide.path" class="console-guide-item__arrow">›</div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { useRouter } from 'vue-router'

const router = useRouter()

const guides = [
  { title: '新建地块', desc: '点击「新建地块」开始录入您的甘蔗种植地块信息', path: '/plots/create' },
  { title: '规划种植周期', desc: '在「地块管理」中可查看所有地块并规划种植周期', path: '/plots' },
  { title: '查看数据大屏', desc: '全局可视化总览与统计分析', path: '/panel' },
  { title: '记录农事操作', desc: '支持施肥、灌溉、病虫害、采收四类操作', path: '/farming' },
]
</script>

<style lang="scss" scoped>
@use '@/styles/variables' as *;

.console-guide-panel {
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
    background: linear-gradient(90deg, transparent, rgba(57, 255, 20, 0.3), transparent);
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
    color: $accent-green;
    font-size: $font-size-sm;
  }

  &__subtitle {
    font-family: $font-mono;
    font-size: $font-size-xs;
    color: $text-muted;
    letter-spacing: 1px;
  }
}

.console-guide-list {
  display: flex;
  flex-direction: column;
  gap: $spacing-sm;
}

.console-guide-item {
  display: flex;
  align-items: flex-start;
  gap: $spacing-sm;
  padding: $spacing-sm $spacing-md;
  background: rgba(255, 255, 255, 0.02);
  border: 1px solid rgba(255, 255, 255, 0.04);
  border-radius: $radius-sm;
  transition: all $transition-fast;

  &--clickable {
    cursor: pointer;

    &:hover {
      border-color: rgba(0, 240, 255, 0.15);
      background: rgba(0, 240, 255, 0.03);

      .console-guide-item__arrow {
        color: $accent-cyan;
        transform: translateX(4px);
      }
    }
  }

  &__num {
    font-family: $font-mono;
    font-size: $font-size-xs;
    color: $accent-cyan;
    opacity: 0.5;
    min-width: 20px;
    padding-top: 2px;
  }

  &__content {
    flex: 1;
    min-width: 0;
  }

  &__title {
    font-size: $font-size-sm;
    font-weight: 600;
    color: $text-primary;
    margin-bottom: 2px;
  }

  &__desc {
    font-size: $font-size-xs;
    color: $text-muted;
    line-height: 1.5;
  }

  &__arrow {
    font-size: 16px;
    color: $text-muted;
    transition: all $transition-fast;
    padding-top: 2px;
  }
}
</style>
