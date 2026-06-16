<template>
  <span class="hud-status-light" :class="[`hud-status-light--${status}`]" :title="statusText" />
</template>

<script setup>
import { computed } from 'vue'

const props = defineProps({
  status: {
    type: String,
    default: 'idle',
    validator: (v) => ['idle', 'growing', 'harvested'].includes(v),
  },
})

const statusTextMap = {
  idle: '空闲',
  growing: '生长中',
  harvested: '已收割',
}

const statusText = computed(() => statusTextMap[props.status] || props.status)
</script>

<style lang="scss" scoped>
@use '@/styles/variables' as *;

.hud-status-light {
  display: inline-block;
  width: 10px;
  height: 10px;
  border-radius: 50%;
  vertical-align: middle;

  &--idle {
    background: $status-idle;
    animation: pulse-gray 2.5s ease-in-out infinite;
  }

  &--growing {
    background: $status-growing;
    box-shadow: 0 0 6px rgba(57, 255, 20, 0.5);
    animation: breathe 2s ease-in-out infinite;
  }

  &--harvested {
    background: $status-harvested;
    box-shadow: 0 0 6px rgba(255, 107, 53, 0.5);
  }
}

@keyframes breathe {
  0%, 100% {
    opacity: 0.5;
    box-shadow: 0 0 4px rgba(57, 255, 20, 0.3);
  }
  50% {
    opacity: 1;
    box-shadow: 0 0 10px rgba(57, 255, 20, 0.6);
  }
}

@keyframes pulse-gray {
  0%, 100% {
    box-shadow: 0 0 2px rgba(74, 85, 104, 0.2);
  }
  50% {
    box-shadow: 0 0 6px rgba(74, 85, 104, 0.4);
  }
}
</style>
