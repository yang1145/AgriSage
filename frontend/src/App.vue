<template>
  <AppLayout v-if="showLayout">
    <router-view />
  </AppLayout>
  <router-view v-else />
</template>

<script setup>
import { computed } from 'vue'
import { useRoute } from 'vue-router'
import AppLayout from '@/components/layout/AppLayout.vue'
import { useAuthStore } from '@/stores/auth'

const route = useRoute()
const authStore = useAuthStore()

const showLayout = computed(() => {
  return route.name !== 'Login'
})

// 初始化认证状态（页面刷新时恢复用户信息）
authStore.initAuth()
</script>
