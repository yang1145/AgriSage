<template>
  <div class="console-shortcuts-panel">
    <div class="console-shortcuts-panel__header">
      <span class="console-shortcuts-panel__title">
        <span class="console-shortcuts-panel__title-icon">▣</span>
        快捷入口
      </span>
      <span class="console-shortcuts-panel__subtitle">QUICK ACCESS</span>
    </div>
    <div class="console-shortcuts">
      <div
        v-for="item in shortcuts"
        :key="item.path"
        class="console-shortcut"
        @click="router.push(item.path)"
      >
        <div class="console-shortcut__bg" />
        <div class="console-shortcut__corner console-shortcut__corner--tl" />
        <div class="console-shortcut__corner console-shortcut__corner--br" />
        <div class="console-shortcut__icon" :class="item.iconClass">
          <el-icon :size="24"><component :is="item.icon" /></el-icon>
        </div>
        <div class="console-shortcut__info">
          <div class="console-shortcut__label">{{ item.label }}</div>
          <div class="console-shortcut__desc">{{ item.desc }}</div>
        </div>
        <div class="console-shortcut__arrow">›</div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { useRouter } from 'vue-router'
import {
  MapLocation, Monitor, Plus, Document, Collection, Setting,
} from '@element-plus/icons-vue'

const router = useRouter()

const shortcuts = [
  { label: '地块管理', desc: '查看与管理所有地块', icon: MapLocation, iconClass: 'console-shortcut__icon--cyan', path: '/plots' },
  { label: '数据大屏', desc: '全局可视化总览', icon: Monitor, iconClass: 'console-shortcut__icon--cyan', path: '/panel' },
  { label: '新建地块', desc: '录入新地块信息', icon: Plus, iconClass: 'console-shortcut__icon--green', path: '/plots/create' },
  { label: '农事记录', desc: '施肥灌溉采收记录', icon: Document, iconClass: 'console-shortcut__icon--cyan', path: '/farming' },
  { label: '品种图鉴', desc: '甘蔗品种信息库', icon: Collection, iconClass: 'console-shortcut__icon--orange', path: '/dictionary/varieties' },
  { label: '系统设置', desc: '账号与系统配置', icon: Setting, iconClass: 'console-shortcut__icon--cyan', path: '/settings' },
]
</script>

<style lang="scss" scoped>
@use '@/styles/variables' as *;

.console-shortcuts-panel {
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

.console-shortcuts {
  display: grid;
  grid-template-columns: repeat(2, 1fr);
  gap: $spacing-sm;
}

.console-shortcut {
  position: relative;
  display: flex;
  align-items: center;
  gap: $spacing-sm;
  padding: $spacing-md;
  background: rgba(255, 255, 255, 0.02);
  border: 1px solid rgba(255, 255, 255, 0.05);
  border-radius: $radius-sm;
  cursor: pointer;
  transition: all $transition-fast;
  overflow: hidden;

  &:hover {
    border-color: rgba(0, 240, 255, 0.2);
    background: rgba(0, 240, 255, 0.03);
    transform: translateX(4px);

    .console-shortcut__arrow {
      color: $accent-cyan;
      transform: translateX(4px);
    }
  }

  &__bg {
    position: absolute;
    inset: 0;
    background-image:
      linear-gradient(rgba(0, 240, 255, 0.02) 1px, transparent 1px),
      linear-gradient(90deg, rgba(0, 240, 255, 0.02) 1px, transparent 1px);
    background-size: 12px 12px;
    pointer-events: none;
  }

  &__corner {
    position: absolute;
    width: 6px;
    height: 6px;
    pointer-events: none;

    &--tl { top: 0; left: 0; border-top: 1px solid rgba(0, 240, 255, 0.2); border-left: 1px solid rgba(0, 240, 255, 0.2); }
    &--br { bottom: 0; right: 0; border-bottom: 1px solid rgba(0, 240, 255, 0.2); border-right: 1px solid rgba(0, 240, 255, 0.2); }
  }

  &__icon {
    width: 40px;
    height: 40px;
    border-radius: $radius-sm;
    display: flex;
    align-items: center;
    justify-content: center;
    flex-shrink: 0;
    background: rgba(0, 240, 255, 0.06);
    border: 1px solid rgba(0, 240, 255, 0.12);
    color: $accent-cyan;
    transition: all $transition-fast;

    &--green {
      background: rgba(57, 255, 20, 0.06);
      border-color: rgba(57, 255, 20, 0.12);
      color: $accent-green;
    }

    &--orange {
      background: rgba(255, 107, 53, 0.06);
      border-color: rgba(255, 107, 53, 0.12);
      color: $accent-orange;
    }
  }

  &:hover .console-shortcut__icon {
    box-shadow: 0 0 8px rgba(0, 240, 255, 0.15);
  }

  &__info {
    flex: 1;
    min-width: 0;
  }

  &__label {
    font-size: $font-size-sm;
    font-weight: 600;
    color: $text-primary;
    margin-bottom: 2px;
  }

  &__desc {
    font-size: $font-size-xs;
    color: $text-muted;
  }

  &__arrow {
    font-size: 18px;
    color: $text-muted;
    transition: all $transition-fast;
  }
}

@media (max-width: 1024px) {
  .console-shortcuts { grid-template-columns: repeat(2, 1fr); }
}

@media (max-width: 640px) {
  .console-shortcuts { grid-template-columns: 1fr; }
}
</style>
