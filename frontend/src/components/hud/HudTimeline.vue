<template>
  <div class="hud-timeline">
    <div
      v-for="(item, index) in items"
      :key="index"
      class="hud-timeline__item"
      :class="{ 'hud-timeline__item--active': item.active }"
    >
      <div class="hud-timeline__node">
        <span class="hud-timeline__dot" />
      </div>
      <div class="hud-timeline__content">
        <div class="hud-timeline__time">{{ item.time }}</div>
        <div class="hud-timeline__label">{{ item.label }}</div>
        <div v-if="item.description" class="hud-timeline__desc">{{ item.description }}</div>
        <slot :name="`item-${index}`" :item="item" />
      </div>
    </div>
  </div>
</template>

<script setup>
defineProps({
  items: {
    type: Array,
    default: () => [],
  },
})
</script>

<style lang="scss" scoped>
@use '@/styles/variables' as *;

.hud-timeline {
  &__item {
    display: flex;
    gap: $spacing-md;
    position: relative;
    padding-bottom: $spacing-lg;

    &:last-child {
      padding-bottom: 0;

      .hud-timeline__node::after {
        display: none;
      }
    }

    &--active {
      .hud-timeline__dot {
        background: $accent-cyan;
        box-shadow: 0 0 8px rgba(0, 240, 255, 0.5);
      }

      .hud-timeline__label {
        color: $accent-cyan;
      }
    }
  }

  &__node {
    position: relative;
    display: flex;
    align-items: flex-start;
    justify-content: center;
    width: 16px;
    flex-shrink: 0;
    padding-top: 4px;

    // Vertical line
    &::after {
      content: '';
      position: absolute;
      top: 16px;
      bottom: -#{$spacing-lg};
      left: 50%;
      transform: translateX(-50%);
      width: 1px;
      background: $border-color;
    }
  }

  &__dot {
    display: block;
    width: 8px;
    height: 8px;
    border-radius: 50%;
    background: $text-muted;
    border: 1px solid $border-color;
    transition: all $transition-base;
  }

  &__content {
    flex: 1;
    min-width: 0;
  }

  &__time {
    font-family: $font-mono;
    font-size: $font-size-xs;
    color: $text-muted;
    letter-spacing: 1px;
    margin-bottom: 2px;
  }

  &__label {
    font-size: $font-size-sm;
    color: $text-primary;
    font-weight: 500;
    transition: color $transition-base;
  }

  &__desc {
    font-size: $font-size-xs;
    color: $text-secondary;
    margin-top: $spacing-xs;
    line-height: 1.5;
  }
}
</style>
