<template>
  <nav class="side-nav" :class="{ 'side-nav--collapsed': collapsed }">
    <!-- Logo area -->
    <div class="side-nav__logo">
      <span class="side-nav__logo-icon">◈</span>
      <span v-if="!collapsed" class="side-nav__logo-text">AgriSage</span>
    </div>

    <!-- Toggle button -->
    <div class="side-nav__toggle" @click="$emit('toggle')">
      <el-icon :size="16">
        <component :is="collapsed ? 'DArrowRight' : 'DArrowLeft'" />
      </el-icon>
    </div>

    <!-- Navigation items -->
    <div class="side-nav__menu">
      <router-link
        v-for="item in visibleNavItems"
        :key="item.path"
        :to="item.path"
        class="side-nav__item"
        :class="{ 'side-nav__item--active': isActive(item.path) }"
      >
        <el-icon :size="18" class="side-nav__item-icon">
          <component :is="item.icon" />
        </el-icon>
        <span v-if="!collapsed" class="side-nav__item-label">{{ item.label }}</span>
      </router-link>
    </div>

    <!-- Bottom decoration -->
    <div class="side-nav__bottom">
      <div class="side-nav__bottom-line" />
    </div>
  </nav>
</template>

<script setup>
import { computed } from 'vue'
import { useRoute } from 'vue-router'
import { useAuthStore } from '@/stores/auth'

defineProps({
  collapsed: {
    type: Boolean,
    default: false,
  },
})

defineEmits(['toggle'])

const route = useRoute()
const authStore = useAuthStore()

const isOwner = computed(() => authStore.userRole === 'owner')

const navItems = [
  { label: '控制台', icon: 'HomeFilled', path: '/' },
  { label: '地块管理', icon: 'MapLocation', path: '/plots' },
  { label: '数据大屏', icon: 'Monitor', path: '/panel' },
  { label: '农事记录', icon: 'Document', path: '/farming' },
  { label: '品种图鉴', icon: 'Collection', path: '/dictionary/varieties' },
  { label: '糖厂通讯录', icon: 'Phone', path: '/dictionary/factories' },
  { label: '气象数据', icon: 'Cloudy', path: '/dictionary/weather' },
  { label: '数据导出', icon: 'Download', path: '/export' },
  { label: '用户管理', icon: 'UserFilled', path: '/users', ownerOnly: true },
  { label: '系统设置', icon: 'Setting', path: '/settings' },
]

const visibleNavItems = computed(() =>
  navItems.filter((item) => !item.ownerOnly || isOwner.value)
)

const isActive = (path) => {
  if (path === '/plots') return route.path === '/plots' || route.path.startsWith('/plots/')
  if (path === '/') return route.path === '/'
  return route.path.startsWith(path)
}
</script>

<style lang="scss" scoped>
@use '@/styles/variables' as *;

.side-nav {
  position: fixed;
  top: 0;
  left: 0;
  width: $sidebar-width;
  height: 100vh;
  background: $bg-primary;
  border-right: 1px solid $border-color;
  display: flex;
  flex-direction: column;
  transition: width $transition-base;
  z-index: $z-fixed;
  overflow: hidden;

  &--collapsed {
    width: $sidebar-collapsed-width;

    .side-nav__logo {
      justify-content: center;
      padding: $spacing-md $spacing-xs;
    }

    .side-nav__toggle {
      justify-content: center;
    }

    .side-nav__item {
      justify-content: center;
      padding: $spacing-sm;
    }
  }

  // Logo
  &__logo {
    display: flex;
    align-items: center;
    gap: $spacing-sm;
    padding: $spacing-md $spacing-md;
    border-bottom: 1px solid $border-color;
    min-height: $topbar-height;
  }

  &__logo-icon {
    font-size: 20px;
    color: $accent-cyan;
    text-shadow: 0 0 8px rgba(0, 240, 255, 0.5);
    flex-shrink: 0;
  }

  &__logo-text {
    font-family: $font-mono;
    font-size: $font-size-md;
    font-weight: 700;
    color: $accent-cyan;
    letter-spacing: 2px;
    white-space: nowrap;
  }

  // Toggle button
  &__toggle {
    display: flex;
    align-items: center;
    justify-content: flex-end;
    padding: $spacing-xs $spacing-md;
    color: $text-muted;
    cursor: pointer;
    border-bottom: 1px solid $border-color;
    transition: color $transition-fast;

    &:hover {
      color: $accent-cyan;
    }
  }

  // Menu
  &__menu {
    flex: 1;
    overflow-y: auto;
    padding: $spacing-sm 0;
  }

  &__item {
    display: flex;
    align-items: center;
    gap: $spacing-sm;
    padding: $spacing-sm $spacing-md;
    margin: 2px $spacing-sm;
    color: $text-secondary;
    text-decoration: none;
    border-radius: $radius-sm;
    border-left: 2px solid transparent;
    transition: all $transition-fast;
    position: relative;

    &:hover {
      color: $text-primary;
      background: rgba(0, 240, 255, 0.05);
    }

    &--active {
      color: $accent-cyan;
      background: rgba(0, 240, 255, 0.08);
      border-left-color: $accent-cyan;
      box-shadow: 0 0 8px rgba(0, 240, 255, 0.1);

      .side-nav__item-icon {
        filter: drop-shadow(0 0 4px rgba(0, 240, 255, 0.5));
      }
    }
  }

  &__item-icon {
    flex-shrink: 0;
  }

  &__item-label {
    font-size: $font-size-sm;
    white-space: nowrap;
    letter-spacing: 0.5px;
  }

  // Bottom decoration
  &__bottom {
    padding: $spacing-sm $spacing-md;
  }

  &__bottom-line {
    height: 1px;
    background: linear-gradient(
      90deg,
      transparent,
      rgba(0, 240, 255, 0.2),
      transparent
    );
  }
}
</style>
