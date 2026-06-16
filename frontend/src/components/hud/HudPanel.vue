<template>
  <div class="hud-panel">
    <div class="hud-corner hud-corner--tl" />
    <div class="hud-corner hud-corner--tr" />
    <div class="hud-corner hud-corner--bl" />
    <div class="hud-corner hud-corner--br" />
    <div v-if="title" class="hud-panel__title-bar">
      <span class="hud-panel__title">{{ title }}</span>
    </div>
    <div class="hud-panel__content">
      <slot />
    </div>
  </div>
</template>

<script setup>
defineProps({
  title: {
    type: String,
    default: '',
  },
})
</script>

<style lang="scss" scoped>
@use '@/styles/variables' as *;

.hud-panel {
  position: relative;
  background: $bg-primary;
  border: 1px solid $border-color;
  border-radius: $radius-md;
  overflow: hidden;

  // Grid-line background pattern
  &::before {
    content: '';
    position: absolute;
    inset: 0;
    background:
      repeating-linear-gradient(
        0deg,
        transparent,
        transparent 39px,
        rgba(0, 240, 255, 0.04) 39px,
        rgba(0, 240, 255, 0.04) 40px
      ),
      repeating-linear-gradient(
        90deg,
        transparent,
        transparent 39px,
        rgba(0, 240, 255, 0.04) 39px,
        rgba(0, 240, 255, 0.04) 40px
      );
    pointer-events: none;
    z-index: 0;
  }

  &__title-bar {
    position: relative;
    display: flex;
    align-items: center;
    padding: $spacing-sm $spacing-md;
    background: rgba(0, 240, 255, 0.05);
    border-bottom: 1px solid $border-color;
    z-index: 1;
  }

  &__title {
    font-family: $font-mono;
    font-size: $font-size-sm;
    font-weight: 600;
    color: $accent-cyan;
    text-transform: uppercase;
    letter-spacing: 2px;

    &::before {
      content: '◆ ';
      font-size: 8px;
      vertical-align: middle;
    }
  }

  &__content {
    position: relative;
    padding: $spacing-md;
    z-index: 1;
  }
}

// Corner decorations
.hud-corner {
  position: absolute;
  width: 20px;
  height: 20px;
  pointer-events: none;
  z-index: 2;

  &--tl {
    top: -1px;
    left: -1px;
    border-top: 2px solid $accent-cyan;
    border-left: 2px solid $accent-cyan;
  }

  &--tr {
    top: -1px;
    right: -1px;
    border-top: 2px solid $accent-cyan;
    border-right: 2px solid $accent-cyan;
  }

  &--bl {
    bottom: -1px;
    left: -1px;
    border-bottom: 2px solid $accent-cyan;
    border-left: 2px solid $accent-cyan;
  }

  &--br {
    bottom: -1px;
    right: -1px;
    border-bottom: 2px solid $accent-cyan;
    border-right: 2px solid $accent-cyan;
  }
}
</style>
