<template>
  <div class="console-hero">
    <div class="console-hero__corner console-hero__corner--tl" />
    <div class="console-hero__corner console-hero__corner--tr" />
    <div class="console-hero__corner console-hero__corner--bl" />
    <div class="console-hero__corner console-hero__corner--br" />
    <div class="console-hero__line-top" />
    <div class="console-hero__line-bottom" />

    <div class="console-hero__content">
      <div class="console-hero__left">
        <div class="console-hero__badge">
          <span class="console-hero__badge-dot" />
          <span class="console-hero__badge-text">SYSTEM ONLINE</span>
        </div>
        <h1 class="console-hero__title">
          <span class="console-hero__greeting">欢迎回来</span>
          <span class="console-hero__name">{{ authStore.user?.name || '用户' }}</span>
        </h1>
        <p class="console-hero__subtitle">
          <span class="console-hero__subtitle-prefix">//</span>
          桂收 · 甘蔗专用版智能管理系统
          <span class="console-hero__divider">|</span>
          当前角色: {{ roleLabel }}
        </p>
      </div>
      <div class="console-hero__right">
        <div class="console-clock">
          <div class="console-clock__time">{{ clockTime }}</div>
          <div class="console-clock__date">{{ clockDate }}</div>
          <div class="console-clock__week">{{ clockWeek }}</div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { computed } from 'vue'
import { useAuthStore } from '@/stores/auth'
import { useClock } from '@/composables/useClock'

const authStore = useAuthStore()
const { clockTime, clockDate, clockWeek } = useClock()

const roleMap = { owner: '户主', family: '家庭成员', coop_admin: '合作社管理员', technician: '农技员' }
const roleLabel = computed(() => roleMap[authStore.user?.role] || authStore.user?.role || '')
</script>

<style lang="scss" scoped>
@use '@/styles/variables' as *;

.console-hero {
  position: relative;
  background: linear-gradient(135deg, rgba(0, 240, 255, 0.04) 0%, transparent 50%, rgba(57, 255, 20, 0.02) 100%);
  border: 1px solid $border-color;
  border-radius: $radius-md;
  padding: $spacing-xl;
  overflow: hidden;

  &::before {
    content: '';
    position: absolute;
    top: 0;
    left: 0;
    right: 0;
    height: 1px;
    background: linear-gradient(90deg, transparent, rgba(0, 240, 255, 0.4) 30%, rgba(0, 240, 255, 0.6) 50%, rgba(0, 240, 255, 0.4) 70%, transparent);
  }

  &__corner {
    position: absolute;
    width: 16px;
    height: 16px;
    pointer-events: none;

    &--tl { top: -1px; left: -1px; border-top: 2px solid $accent-cyan; border-left: 2px solid $accent-cyan; }
    &--tr { top: -1px; right: -1px; border-top: 2px solid $accent-cyan; border-right: 2px solid $accent-cyan; }
    &--bl { bottom: -1px; left: -1px; border-bottom: 2px solid $accent-cyan; border-left: 2px solid $accent-cyan; }
    &--br { bottom: -1px; right: -1px; border-bottom: 2px solid $accent-cyan; border-right: 2px solid $accent-cyan; }
  }

  &__line-top,
  &__line-bottom {
    position: absolute;
    left: 0;
    right: 0;
    height: 1px;
    background: linear-gradient(90deg, transparent 0%, rgba(0, 240, 255, 0.15) 20%, rgba(0, 240, 255, 0.15) 80%, transparent 100%);
  }
  &__line-top { top: 8px; }
  &__line-bottom { bottom: 8px; }

  &__content {
    position: relative;
    display: flex;
    justify-content: space-between;
    align-items: center;
    flex-wrap: wrap;
    gap: $spacing-lg;
  }

  &__badge {
    display: inline-flex;
    align-items: center;
    gap: 6px;
    margin-bottom: $spacing-sm;
    font-family: $font-mono;
    font-size: $font-size-xs;
    letter-spacing: 2px;
  }

  &__badge-dot {
    width: 6px;
    height: 6px;
    border-radius: 50%;
    background: $accent-green;
    box-shadow: 0 0 6px $accent-green;
    animation: pulse-dot 2s ease-in-out infinite;
  }

  &__badge-text {
    color: $accent-green;
    text-shadow: 0 0 6px rgba(57, 255, 20, 0.3);
  }

  &__title {
    display: flex;
    align-items: baseline;
    gap: $spacing-sm;
    margin: 0 0 $spacing-xs 0;
    font-size: $font-size-2xl;
    font-weight: 700;
  }

  &__greeting {
    color: $text-primary;
  }

  &__name {
    color: $accent-cyan;
    text-shadow: 0 0 12px rgba(0, 240, 255, 0.4);
  }

  &__subtitle {
    margin: 0;
    font-family: $font-mono;
    font-size: $font-size-sm;
    color: $text-muted;
    letter-spacing: 1px;
  }

  &__subtitle-prefix {
    color: $accent-cyan;
    margin-right: $spacing-xs;
  }

  &__divider {
    margin: 0 $spacing-sm;
    color: rgba(255, 255, 255, 0.1);
  }
}

.console-clock {
  text-align: right;
  font-family: $font-mono;

  &__time {
    font-size: $font-size-2xl;
    font-weight: 700;
    color: $accent-cyan;
    text-shadow: 0 0 12px rgba(0, 240, 255, 0.3);
    letter-spacing: 2px;
    line-height: 1;
  }

  &__date {
    font-size: $font-size-sm;
    color: $text-secondary;
    margin-top: $spacing-xs;
    letter-spacing: 1px;
  }

  &__week {
    font-size: $font-size-xs;
    color: $text-muted;
    margin-top: 2px;
  }
}

@keyframes pulse-dot {
  0%, 100% { opacity: 1; box-shadow: 0 0 6px $accent-green; }
  50% { opacity: 0.5; box-shadow: 0 0 2px $accent-green; }
}

@media (max-width: 640px) {
  .console-hero__content { flex-direction: column; align-items: flex-start; }
  .console-clock { text-align: left; }
}
</style>
