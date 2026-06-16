import { createRouter, createWebHistory } from 'vue-router'

const routes = [
  {
    path: '/login',
    name: 'Login',
    component: () => import('@/views/LoginView.vue'),
    meta: { requiresAuth: false },
  },
  {
    path: '/',
    name: 'Console',
    component: () => import('@/views/ConsoleView.vue'),
    meta: { requiresAuth: true },
  },
  {
    path: '/plots',
    name: 'PlotOverview',
    component: () => import('@/views/plot/PlotOverview.vue'),
    meta: { requiresAuth: true },
  },
  {
    path: '/panel',
    name: 'Dashboard',
    component: () => import('@/views/DashboardView.vue'),
    meta: { requiresAuth: true },
  },
  {
    path: '/plots/create',
    name: 'PlotCreate',
    component: () => import('@/views/plot/PlotCreate.vue'),
    meta: { requiresAuth: true },
  },
  {
    path: '/plots/:id',
    name: 'PlotDetail',
    component: () => import('@/views/plot/PlotDetail.vue'),
    meta: { requiresAuth: true },
  },
  {
    path: '/plots/:id/images',
    name: 'PlotImages',
    component: () => import('@/views/plot/PlotImages.vue'),
    meta: { requiresAuth: true },
  },
  {
    path: '/plots/:id/cycle/create',
    name: 'CycleCreate',
    component: () => import('@/views/CycleCreate.vue'),
    meta: { requiresAuth: true },
  },
  {
    path: '/cycles/:id',
    name: 'CycleDetail',
    component: () => import('@/views/CycleDetail.vue'),
    meta: { requiresAuth: true },
  },
  {
    path: '/farming',
    name: 'FarmingRecord',
    component: () => import('@/views/FarmingRecord.vue'),
    meta: { requiresAuth: true },
  },
  {
    path: '/farming/create',
    name: 'FarmingForm',
    component: () => import('@/views/FarmingForm.vue'),
    meta: { requiresAuth: true },
  },
  {
    path: '/dictionary/varieties',
    name: 'VarietyList',
    component: () => import('@/views/VarietyList.vue'),
    meta: { requiresAuth: true },
  },
  {
    path: '/dictionary/factories',
    name: 'FactoryList',
    component: () => import('@/views/FactoryList.vue'),
    meta: { requiresAuth: true },
  },
  {
    path: '/dictionary/weather',
    name: 'WeatherData',
    component: () => import('@/views/WeatherData.vue'),
    meta: { requiresAuth: true },
  },
  {
    path: '/export',
    name: 'ExportView',
    component: () => import('@/views/ExportView.vue'),
    meta: { requiresAuth: true },
  },
  {
    path: '/settings',
    name: 'SettingsView',
    component: () => import('@/views/SettingsView.vue'),
    meta: { requiresAuth: true },
  },
  {
    path: '/users',
    name: 'UserManagement',
    component: () => import('@/views/UserManagement.vue'),
    meta: { requiresAuth: true, requiresOwner: true },
  },
]

const router = createRouter({
  history: createWebHistory(),
  routes,
})

router.beforeEach((to, from, next) => {
  const token = localStorage.getItem('token')
  if (to.meta.requiresAuth !== false && !token) {
    next({ name: 'Login', query: { redirect: to.fullPath } })
  } else if (to.name === 'Login' && token) {
    next({ name: 'Console' })
  } else if (to.meta.requiresOwner) {
    // 需要户主权限，等待角色信息加载
    // 如果角色尚未确定（正在初始化），允许访问，组件内会处理
    const role = localStorage.getItem('userRole')
    if (role && role !== 'owner') {
      // 角色已确定且不是户主，重定向
      next({ name: 'Console' })
    } else {
      // 角色尚未确定或为户主，允许访问
      next()
    }
  } else {
    next()
  }
})

export default router
