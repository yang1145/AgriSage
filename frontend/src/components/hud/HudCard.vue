<template>
  <div class="hud-card" :class="[`hud-card--${variant}`, { 'hud-card--glowing': glowing }]">
    <div v-if="title" class="hud-card__header">
      <span class="hud-card__title">{{ title }}</span>
      <slot name="header-actions" />
    </div>
    <div class="hud-card__body">
      <slot />
    </div>
    <div v-if="$slots.footer" class="hud-card__footer">
      <slot name="footer" />
    </div>
  </div>
</template>

<script setup>
defineProps({
  title: {
    type: String,
    default: '',
  },
  variant: {
    type: String,
    default: 'default',
    validator: (v) => ['default', 'cyan', 'orange', 'green'].includes(v),
  },
  glowing: {
    type: Boolean,
    default: false,
  },
})
</script>

<style lang="scss" scoped>
@use '@/styles/variables' as *;

.hud-card {
  position: relative;
  background: $bg-card;
  border: 1px solid $border-color;
  border-radius: $radius-md;
  padding: $spacing-md;
  overflow: hidden;
  transition: border-color $transition-glow, box-shadow $transition-glow;

  // Subtle grid background
  &::before {
    content: '';
    position: absolute;
    inset: 0;
    background-image:
      linear-gradient(rgba(0, 240, 255, 0.03) 1px, transparent 1px),
      linear-gradient(90deg, rgba(0, 240, 255, 0.03) 1px, transparent 1px);
    background-size: 20px 20px;
    pointer-events: none;
    z-index: 0;
  }

  // Hexagonal corner decoration - top-left
  &::after {
    content: '';
    position: absolute;
    top: 0;
    left: 0;
    width: 16px;
    height: 16px;
    border-top: 2px solid $accent-cyan;
    border-left: 2px solid $accent-cyan;
    border-radius: $radius-sm 0 0 0;
    pointer-events: none;
    z-index: 1;
  }

  > * {
    position: relative;
    z-index: 1;
  }

  &:hover {
    border-color: rgba(0, 240, 255, 0.3);
    box-shadow: 0 0 8px rgba(0, 240, 255, 0.1);
  }

  &--cyan {
    border-color: rgba(0, 240, 255, 0.3);
    box-shadow: $shadow-glow-cyan;
  }

  &--orange {
    border-color: rgba(255, 107, 53, 0.3);
    box-shadow: $shadow-glow-orange;

    &::after {
      border-top-color: $accent-orange;
      border-left-color: $accent-orange;
    }
  }

  &--green {
    border-color: rgba(57, 255, 20, 0.3);
    box-shadow: $shadow-glow-green;

    &::after {
      border-top-color: $accent-green;
      border-left-color: $accent-green;
    }
  }

  &--glowing {
    animation: breathe 3s ease-in-out infinite;
  }

  &__header {
    display: flex;
    align-items: center;
    justify-content: space-between;
    margin-bottom: $spacing-md;
    padding-bottom: $spacing-sm;
    border-bottom: 1px solid $border-color;
  }

  &__title {
    font-family: $font-mono;
    font-size: $font-size-sm;
    font-weight: 600;
    color: $accent-cyan;
    text-transform: uppercase;
    letter-spacing: 1px;
  }

  &__body {
    color: $text-primary;
  }

  &__footer {
    margin-top: $spacing-md;
    padding-top: $spacing-sm;
    border-top: 1px solid $border-color;
  }
}

@keyframes breathe {
  0%, 100% {
    opacity: 0.85;
  }
  50% {
    opacity: 1;
  }
}
</style>
