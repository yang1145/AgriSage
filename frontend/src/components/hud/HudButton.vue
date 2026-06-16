<template>
  <button
    class="hud-button"
    :class="[`hud-button--${type}`, `hud-button--${size}`]"
    :disabled="disabled"
    @click="$emit('click', $event)"
  >
    <span class="hud-button__scanline" />
    <span class="hud-button__content">
      <el-icon v-if="icon" class="hud-button__icon"><component :is="icon" /></el-icon>
      <slot />
    </span>
  </button>
</template>

<script setup>
defineProps({
  type: {
    type: String,
    default: 'cyan',
    validator: (v) => ['cyan', 'orange', 'green', 'ghost'].includes(v),
  },
  size: {
    type: String,
    default: 'default',
    validator: (v) => ['small', 'default', 'large'].includes(v),
  },
  icon: {
    type: String,
    default: '',
  },
  disabled: {
    type: Boolean,
    default: false,
  },
})

defineEmits(['click'])
</script>

<style lang="scss" scoped>
@use '@/styles/variables' as *;

.hud-button {
  position: relative;
  display: inline-flex;
  align-items: center;
  justify-content: center;
  border: 1px solid;
  border-radius: $radius-sm;
  font-family: $font-mono;
  font-weight: 600;
  letter-spacing: 1px;
  cursor: pointer;
  overflow: hidden;
  transition: all $transition-base;
  background: transparent;
  outline: none;

  // Sizes
  &--small {
    height: 28px;
    padding: 0 $spacing-sm;
    font-size: $font-size-xs;
  }

  &--default {
    height: 36px;
    padding: 0 $spacing-md;
    font-size: $font-size-sm;
  }

  &--large {
    height: 44px;
    padding: 0 $spacing-lg;
    font-size: $font-size-base;
  }

  // Scanline effect
  &__scanline {
    position: absolute;
    top: 0;
    left: -100%;
    width: 100%;
    height: 100%;
    background: linear-gradient(
      90deg,
      transparent,
      rgba(255, 255, 255, 0.15),
      transparent
    );
    transition: left 0.4s ease;
    pointer-events: none;
  }

  &:hover .hud-button__scanline {
    left: 100%;
  }

  &:active .hud-button__scanline {
    left: 100%;
    background: linear-gradient(
      90deg,
      transparent,
      rgba(255, 255, 255, 0.25),
      transparent
    );
  }

  &__content {
    display: inline-flex;
    align-items: center;
    gap: $spacing-xs;
    position: relative;
    z-index: 1;
  }

  &__icon {
    font-size: 1em;
  }

  // Type variants
  &--cyan {
    color: $accent-cyan;
    border-color: rgba(0, 240, 255, 0.4);
    background: rgba(0, 240, 255, 0.08);

    &:hover {
      background: rgba(0, 240, 255, 0.15);
      border-color: $accent-cyan;
      box-shadow: 0 0 12px rgba(0, 240, 255, 0.2);
    }

    &:active {
      background: rgba(0, 240, 255, 0.2);
    }
  }

  &--orange {
    color: $accent-orange;
    border-color: rgba(255, 107, 53, 0.4);
    background: rgba(255, 107, 53, 0.08);

    &:hover {
      background: rgba(255, 107, 53, 0.15);
      border-color: $accent-orange;
      box-shadow: 0 0 12px rgba(255, 107, 53, 0.2);
    }

    &:active {
      background: rgba(255, 107, 53, 0.2);
    }
  }

  &--green {
    color: $accent-green;
    border-color: rgba(57, 255, 20, 0.4);
    background: rgba(57, 255, 20, 0.08);

    &:hover {
      background: rgba(57, 255, 20, 0.15);
      border-color: $accent-green;
      box-shadow: 0 0 12px rgba(57, 255, 20, 0.2);
    }

    &:active {
      background: rgba(57, 255, 20, 0.2);
    }
  }

  &--ghost {
    color: $text-secondary;
    border-color: $border-color;
    background: transparent;

    &:hover {
      color: $accent-cyan;
      border-color: rgba(0, 240, 255, 0.3);
      background: rgba(0, 240, 255, 0.05);
    }

    &:active {
      background: rgba(0, 240, 255, 0.08);
    }
  }

  // Disabled
  &:disabled {
    opacity: 0.4;
    cursor: not-allowed;
    pointer-events: none;
  }
}
</style>
