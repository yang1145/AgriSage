<template>
  <header class="top-bar">
    <div class="top-bar__left">
      <span class="top-bar__title">桂收 · 甘蔗专用版</span>
    </div>

    <div class="top-bar__center">
      <span class="top-bar__clock">{{ currentTime }}</span>
    </div>

    <div class="top-bar__right">
      <div class="top-bar__user">
        <span class="top-bar__user-name">{{ userName }}</span>
        <span class="top-bar__user-role hud-badge hud-badge--cyan">{{ userRole }}</span>
      </div>
      <el-dropdown trigger="click" @command="handleCommand">
        <el-icon class="top-bar__dropdown-trigger" :size="16">
          <ArrowDown />
        </el-icon>
        <template #dropdown>
          <el-dropdown-menu>
            <el-dropdown-item command="profile">
              <el-icon><User /></el-icon>
              个人信息
            </el-dropdown-item>
            <el-dropdown-item command="password">
              <el-icon><Lock /></el-icon>
              修改密码
            </el-dropdown-item>
            <el-dropdown-item v-if="isOwner" command="users" divided>
              <el-icon><UserFilled /></el-icon>
              用户管理
            </el-dropdown-item>
            <el-dropdown-item command="logout" divided>
              <el-icon class="logout-icon"><SwitchButton /></el-icon>
              退出登录
            </el-dropdown-item>
          </el-dropdown-menu>
        </template>
      </el-dropdown>
    </div>

    <!-- Bottom glow line -->
    <div class="top-bar__glow-line" />
  </header>
</template>

<script setup>
import { ref, computed, onMounted, onUnmounted } from 'vue'
import { useRouter } from 'vue-router'
import { ElMessage, ElMessageBox } from 'element-plus'
import { useAuthStore } from '@/stores/auth'
import {
  ArrowDown, User, Lock, UserFilled, SwitchButton,
} from '@element-plus/icons-vue'
import dayjs from 'dayjs'

const router = useRouter()
const authStore = useAuthStore()

const currentTime = ref('')
let timer = null

const isOwner = computed(() => authStore.userRole === 'owner')

const userName = computed(() => authStore.user?.name || '未登录')
const userRole = computed(() => {
  const role = authStore.user?.role
  const roleMap = { owner: '户主', family: '家庭成员', coop_admin: '合作社管理员', technician: '农技员' }
  return roleMap[role] || role || ''
})

const updateClock = () => {
  currentTime.value = dayjs().format('HH:mm:ss')
}

const handleLogout = async () => {
  try {
    await ElMessageBox.confirm(
      '确定要退出当前账号吗？退出后需要重新登录。',
      '退出确认',
      {
        confirmButtonText: '确认退出',
        cancelButtonText: '取消',
        type: 'warning',
        confirmButtonClass: 'el-button--danger',
      }
    )
    authStore.logout()
    ElMessage.success('已退出登录')
    router.push('/login')
  } catch {
    // cancelled
  }
}

const handleCommand = (command) => {
  switch (command) {
    case 'logout':
      handleLogout()
      break
    case 'password':
      router.push('/settings')
      break
    case 'users':
      router.push('/users')
      break
    case 'profile':
    default:
      router.push('/settings')
      break
  }
}

onMounted(() => {
  updateClock()
  timer = setInterval(updateClock, 1000)
})

onUnmounted(() => {
  if (timer) clearInterval(timer)
})
</script>

<style lang="scss" scoped>
@use '@/styles/variables' as *;

.top-bar {
  position: relative;
  display: flex;
  align-items: center;
  justify-content: space-between;
  height: $topbar-height;
  padding: 0 $spacing-lg;
  background: $bg-secondary;
  border-bottom: 1px solid $border-color;
  flex-shrink: 0;

  &__left {
    display: flex;
    align-items: center;
  }

  &__title {
    font-family: $font-mono;
    font-size: $font-size-md;
    font-weight: 700;
    color: $accent-cyan;
    text-shadow: 0 0 10px rgba(0, 240, 255, 0.4);
    letter-spacing: 2px;
  }

  &__center {
    display: flex;
    align-items: center;
  }

  &__clock {
    font-family: $font-mono;
    font-size: $font-size-md;
    color: $accent-cyan;
    letter-spacing: 3px;
    text-shadow: 0 0 6px rgba(0, 240, 255, 0.3);
  }

  &__right {
    display: flex;
    align-items: center;
    gap: $spacing-sm;
  }

  &__user {
    display: flex;
    align-items: center;
    gap: $spacing-sm;
  }

  &__user-name {
    font-size: $font-size-sm;
    color: $text-primary;
  }

  &__dropdown-trigger {
    color: $text-muted;
    cursor: pointer;
    transition: color $transition-fast;

    &:hover {
      color: $accent-cyan;
    }
  }

  // Bottom glow line
  &__glow-line {
    position: absolute;
    bottom: 0;
    left: 0;
    right: 0;
    height: 1px;
    background: linear-gradient(
      90deg,
      transparent,
      rgba(0, 240, 255, 0.4) 30%,
      rgba(0, 240, 255, 0.6) 50%,
      rgba(0, 240, 255, 0.4) 70%,
      transparent
    );
  }
}

.logout-icon {
  color: $status-error;
}

// Badge styles (local for this component)
.hud-badge {
  display: inline-flex;
  align-items: center;
  padding: 2px $spacing-sm;
  font-family: $font-mono;
  font-size: $font-size-xs;
  text-transform: uppercase;
  letter-spacing: 1px;
  border-radius: $radius-sm;
  border: 1px solid;

  &--cyan {
    color: $accent-cyan;
    border-color: rgba(0, 240, 255, 0.4);
    background: rgba(0, 240, 255, 0.08);
  }
}

:deep(.el-dropdown-menu__item) {
  display: flex;
  align-items: center;
  gap: $spacing-sm;

  .el-icon {
    font-size: 14px;
  }
}
</style>
