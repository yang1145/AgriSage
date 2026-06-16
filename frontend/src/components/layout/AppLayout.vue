<template>
  <div class="app-layout" :class="{ 'app-layout--collapsed': collapsed }">
    <SideNav :collapsed="collapsed" @toggle="toggleSidebar" />
    <div class="app-layout__main">
      <TopBar />
      <div class="app-layout__content">
        <router-view />
      </div>
    </div>
    <!-- Scanline overlay -->
    <div class="app-layout__scanline" />
  </div>
</template>

<script setup>
import { computed } from 'vue'
import { useAppStore } from '@/stores/app'
import SideNav from './SideNav.vue'
import TopBar from './TopBar.vue'

const appStore = useAppStore()
const collapsed = computed(() => appStore.sidebarCollapsed)

const toggleSidebar = () => {
  appStore.toggleSidebar()
}
</script>

<style lang="scss" scoped>
@use '@/styles/variables' as *;

.app-layout {
  display: flex;
  width: 100%;
  height: 100vh;
  background: $bg-primary;
  color: $text-primary;
  overflow: hidden;

  &__main {
    flex: 1;
    display: flex;
    flex-direction: column;
    min-width: 0;
    margin-left: $sidebar-width;
    transition: margin-left $transition-base;
  }

  &--collapsed &__main {
    margin-left: $sidebar-collapsed-width;
  }

  &__content {
    flex: 1;
    overflow-y: auto;
    padding: $spacing-lg;
    background: $bg-primary;

    // Subtle grid background
    background-image:
      linear-gradient(rgba(0, 240, 255, 0.015) 1px, transparent 1px),
      linear-gradient(90deg, rgba(0, 240, 255, 0.015) 1px, transparent 1px);
    background-size: 40px 40px;
  }

  &__scanline {
    position: fixed;
    inset: 0;
    pointer-events: none;
    z-index: $z-scanline;
    background: repeating-linear-gradient(
      0deg,
      transparent,
      transparent 2px,
      rgba(0, 0, 0, 0.02) 2px,
      rgba(0, 0, 0, 0.02) 4px
    );
  }
}
</style>
