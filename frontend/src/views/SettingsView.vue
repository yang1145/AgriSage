<template>
  <div class="settings-page">
    <!-- Header -->
    <div class="page-header">
      <h1 class="page-title">系统设置</h1>
    </div>

    <div class="settings-sections">
      <!-- 个人信息 -->
      <HudPanel title="PROFILE / 个人信息">
        <div class="section-content">
          <el-form
            ref="profileFormRef"
            :model="profileForm"
            :rules="profileRules"
            label-position="top"
            class="hud-form"
          >
            <el-form-item label="姓名" prop="name">
              <el-input v-model="profileForm.name" placeholder="请输入姓名" />
            </el-form-item>
            <el-form-item label="联系电话" prop="phone">
              <el-input v-model="profileForm.phone" placeholder="请输入联系电话" />
            </el-form-item>
          </el-form>
          <div class="form-row form-row--actions">
            <HudButton type="cyan" :disabled="savingProfile" @click="handleSaveProfile">
              {{ savingProfile ? '保存中...' : '保存信息' }}
            </HudButton>
          </div>
        </div>
      </HudPanel>

      <!-- 修改密码 -->
      <HudPanel title="CHANGE PASSWORD / 修改密码">
        <div class="section-content">
          <el-form
            ref="pwdFormRef"
            :model="pwdForm"
            :rules="pwdRules"
            label-position="top"
            class="hud-form"
          >
            <el-form-item label="旧密码" prop="old_password">
              <el-input v-model="pwdForm.old_password" type="password" show-password placeholder="请输入旧密码" />
            </el-form-item>
            <el-form-item label="新密码" prop="new_password">
              <el-input v-model="pwdForm.new_password" type="password" show-password placeholder="请输入新密码" />
            </el-form-item>
            <el-form-item label="确认新密码" prop="confirm_password">
              <el-input v-model="pwdForm.confirm_password" type="password" show-password placeholder="请再次输入新密码" />
            </el-form-item>
          </el-form>
          <div class="form-row form-row--actions">
            <HudButton type="cyan" :disabled="changingPwd" @click="handleChangePassword">
              {{ changingPwd ? '修改中...' : '修改密码' }}
            </HudButton>
          </div>
        </div>
      </HudPanel>

      <!-- 数据概览 -->
      <HudPanel title="DATA OVERVIEW / 数据概览">
        <div class="section-content">
          <div class="stats-grid">
            <div class="stat-box">
              <span class="stat-box__value">{{ sysStats.plot_count || 0 }}</span>
              <span class="stat-box__label">地块</span>
            </div>
            <div class="stat-box">
              <span class="stat-box__value">{{ sysStats.cycle_count || 0 }}</span>
              <span class="stat-box__label">种植周期</span>
            </div>
            <div class="stat-box">
              <span class="stat-box__value">{{ sysStats.variety_count || 0 }}</span>
              <span class="stat-box__label">品种</span>
            </div>
            <div class="stat-box">
              <span class="stat-box__value">{{ sysStats.factory_count || 0 }}</span>
              <span class="stat-box__label">糖厂</span>
            </div>
            <div class="stat-box">
              <span class="stat-box__value">{{ sysStats.db_size_mb || 0 }}</span>
              <span class="stat-box__label">数据库(MB)</span>
            </div>
          </div>
        </div>
      </HudPanel>

      <!-- 预置数据更新 (户主 only) -->
      <HudPanel v-if="isOwner" title="DATA UPDATE / 预置数据更新">
        <div class="section-content">
          <div class="about-grid">
            <div class="about-item">
              <span class="about-label">品种库</span>
              <span class="about-value">{{ sysStats.variety_count || 0 }} 条</span>
            </div>
            <div class="about-item">
              <span class="about-label">糖厂库</span>
              <span class="about-value">{{ sysStats.factory_count || 0 }} 条</span>
            </div>
          </div>
          <div class="form-row form-row--actions">
            <HudButton type="cyan" :disabled="reloadingSeed" @click="handleReloadSeed">
              {{ reloadingSeed ? '更新中...' : '重新加载预置数据' }}
            </HudButton>
          </div>
        </div>
      </HudPanel>

      <!-- 关于系统 -->
      <HudPanel title="ABOUT / 关于系统">
        <div class="section-content">
          <div class="about-grid">
            <div class="about-item">
              <span class="about-label">产品名称</span>
              <span class="about-value about-value--highlight">桂收 · 甘蔗专用版</span>
            </div>
            <div class="about-item">
              <span class="about-label">版本号</span>
              <span class="about-value">1.0.0</span>
            </div>
            <div class="about-item">
              <span class="about-label">技术栈</span>
              <span class="about-value">Vue 3 + Vite + Element Plus + ECharts</span>
            </div>
            <div class="about-item">
              <span class="about-label">后端</span>
              <span class="about-value">Python / Flask + SQLite</span>
            </div>
          </div>
        </div>
      </HudPanel>
    </div>

    <!-- User Dialog 已移至独立 UserManagement 页面 -->
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { ElMessage, ElMessageBox } from 'element-plus'
import { authApi } from '@/api/auth'
import { userApi } from '@/api/user'
import { systemApi } from '@/api/system'
import { useAuthStore } from '@/stores/auth'
import HudPanel from '@/components/hud/HudPanel.vue'
import HudButton from '@/components/hud/HudButton.vue'

const authStore = useAuthStore()

const isOwner = computed(() => authStore.userRole === 'owner')

// --- Profile ---
const profileFormRef = ref(null)
const savingProfile = ref(false)
const profileForm = ref({
  name: '',
  phone: '',
})

const profileRules = {
  name: [{ required: true, message: '请输入姓名', trigger: 'blur' }],
}

const handleSaveProfile = async () => {
  if (!profileFormRef.value) return
  await profileFormRef.value.validate()
  savingProfile.value = true
  try {
    const res = await userApi.updateUser(authStore.user.id, {
      name: profileForm.value.name,
      phone: profileForm.value.phone,
    })
    ElMessage.success('个人信息保存成功')
    authStore.user.name = res.data.user?.name || profileForm.value.name
    authStore.user.phone = res.data.user?.phone || profileForm.value.phone
  } catch {
    ElMessage.error('保存失败')
  } finally {
    savingProfile.value = false
  }
}

// --- System Stats ---
const sysStats = ref({})

const fetchStats = async () => {
  try {
    const res = await systemApi.getStats()
    sysStats.value = res.data
  } catch {
    sysStats.value = {}
  }
}

// --- User Management ---
const users = ref([])
const showUserDialog = ref(false)
const editingUser = ref(null)
const submittingUser = ref(false)
const userFormRef = ref(null)

const userForm = ref({
  name: '',
  role: '',
  phone: '',
  password: '',
})

const userRules = {
  name: [{ required: true, message: '请输入姓名', trigger: 'blur' }],
  role: [{ required: true, message: '请选择角色', trigger: 'change' }],
  password: [{ required: true, message: '请输入密码', trigger: 'blur' }],
}

const roleLabels = {
  owner: '户主',
  family: '家庭成员',
  coop_admin: '合作社管理员',
  technician: '农技员',
}

const roleLabel = (role) => roleLabels[role] || role

const roleBadgeClass = (role) => {
  const map = { owner: 'role-badge--orange', family: 'role-badge--cyan', coop_admin: 'role-badge--green', technician: 'role-badge--cyan' }
  return map[role] || ''
}

const headerStyle = {
  background: '#111820',
  color: '#00f0ff',
  fontFamily: "'Roboto Mono', 'DIN', monospace",
  fontSize: '12px',
  letterSpacing: '1px',
  borderBottom: '1px solid #1a2332',
}

const cellStyle = {
  background: 'transparent',
  color: '#e0e6ed',
  fontFamily: "'Roboto Mono', 'DIN', monospace",
  fontSize: '13px',
  borderBottom: '1px solid #1a2332',
}

const fetchUsers = async () => {
  try {
    const res = await userApi.getUsers()
    users.value = res.data.users || []
  } catch {
    users.value = []
  }
}

const editUser = (user) => {
  editingUser.value = user
  userForm.value = {
    name: user.name,
    role: user.role,
    phone: user.phone || '',
    password: '',
  }
  showUserDialog.value = true
}

const deleteUser = async (user) => {
  try {
    await ElMessageBox.confirm(`确定删除用户 "${user.name}" 吗？`, '删除确认', {
      confirmButtonText: '确认删除',
      cancelButtonText: '取消',
      type: 'warning',
    })
    await userApi.deleteUser(user.id)
    users.value = users.value.filter((u) => u.id !== user.id)
    ElMessage.success('用户已删除')
  } catch {
    // cancelled
  }
}

const closeUserDialog = () => {
  showUserDialog.value = false
  editingUser.value = null
  userForm.value = { name: '', role: '', phone: '', password: '' }
}

const handleSubmitUser = async () => {
  if (!userFormRef.value) return
  await userFormRef.value.validate()
  submittingUser.value = true
  try {
    if (editingUser.value) {
      await userApi.updateUser(editingUser.value.id, userForm.value)
    } else {
      await userApi.createUser(userForm.value)
    }
    ElMessage.success(editingUser.value ? '用户已更新' : '用户已添加')
    closeUserDialog()
    await fetchUsers()
  } catch {
    ElMessage.error('操作失败')
  } finally {
    submittingUser.value = false
  }
}

// --- Data Update ---
const reloadingSeed = ref(false)

const handleReloadSeed = async () => {
  try {
    await ElMessageBox.confirm('确定重新加载预置数据吗？已有数据不会被覆盖。', '预置数据更新', {
      confirmButtonText: '确认更新',
      cancelButtonText: '取消',
      type: 'info',
    })
    reloadingSeed.value = true
    await systemApi.reloadSeed()
    ElMessage.success('预置数据更新成功')
    await fetchStats()
  } catch {
    // cancelled or error
  } finally {
    reloadingSeed.value = false
  }
}

// --- Change Password ---
const pwdFormRef = ref(null)
const changingPwd = ref(false)

const pwdForm = ref({
  old_password: '',
  new_password: '',
  confirm_password: '',
})

const validateConfirmPassword = (rule, value, callback) => {
  if (value !== pwdForm.value.new_password) {
    callback(new Error('两次输入的密码不一致'))
  } else {
    callback()
  }
}

const pwdRules = {
  old_password: [{ required: true, message: '请输入旧密码', trigger: 'blur' }],
  new_password: [
    { required: true, message: '请输入新密码', trigger: 'blur' },
    { min: 6, message: '密码至少6位', trigger: 'blur' },
  ],
  confirm_password: [
    { required: true, message: '请确认新密码', trigger: 'blur' },
    { validator: validateConfirmPassword, trigger: 'blur' },
  ],
}

const handleChangePassword = async () => {
  if (!pwdFormRef.value) return
  await pwdFormRef.value.validate()
  changingPwd.value = true
  try {
    await authApi.changePassword(pwdForm.value.old_password, pwdForm.value.new_password)
    ElMessage.success('密码修改成功')
    pwdForm.value = { old_password: '', new_password: '', confirm_password: '' }
  } catch {
    ElMessage.error('密码修改失败')
  } finally {
    changingPwd.value = false
  }
}

onMounted(() => {
  fetchStats()
  // 初始化个人信息表单
  if (authStore.user) {
    profileForm.value.name = authStore.user.name || ''
    profileForm.value.phone = authStore.user.phone || ''
  }
})
</script>

<style lang="scss" scoped>
@use '@/styles/variables' as *;

.settings-page {
  min-height: 100%;
}

.page-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  margin-bottom: $spacing-lg;
}

.page-title {
  font-family: $font-mono;
  font-size: $font-size-xl;
  font-weight: 700;
  color: $accent-cyan;
  text-shadow: 0 0 12px rgba(0, 240, 255, 0.3);
  letter-spacing: 2px;
  margin: 0;
}

.settings-sections {
  display: flex;
  flex-direction: column;
  gap: $spacing-lg;
  max-width: 720px;
}

.section-content {
  display: flex;
  flex-direction: column;
  gap: $spacing-md;
}

.section-actions {
  display: flex;
  justify-content: flex-end;
}

.user-name {
  color: $accent-cyan;
  font-weight: 600;
}

.role-badge {
  display: inline-block;
  font-family: $font-mono;
  font-size: $font-size-xs;
  padding: 2px 8px;
  border-radius: $radius-sm;
  letter-spacing: 1px;

  &--orange {
    color: $accent-orange;
    border: 1px solid rgba(255, 107, 53, 0.3);
    background: rgba(255, 107, 53, 0.08);
  }

  &--cyan {
    color: $accent-cyan;
    border: 1px solid rgba(0, 240, 255, 0.3);
    background: rgba(0, 240, 255, 0.08);
  }

  &--green {
    color: $accent-green;
    border: 1px solid rgba(57, 255, 20, 0.3);
    background: rgba(57, 255, 20, 0.08);
  }
}

.action-link {
  font-family: $font-mono;
  font-size: $font-size-xs;
  color: $accent-cyan;
  cursor: pointer;
  margin: 0 6px;
  letter-spacing: 1px;
  transition: color $transition-fast;

  &:hover {
    text-shadow: 0 0 6px rgba(0, 240, 255, 0.3);
  }

  &--danger {
    color: $status-error;

    &:hover {
      text-shadow: 0 0 6px rgba(255, 71, 87, 0.3);
    }
  }
}

.form-row {
  display: flex;
  align-items: center;
  gap: $spacing-md;

  &--actions {
    padding-top: $spacing-sm;
  }
}

.hud-form {
  :deep(.el-form-item__label) {
    color: $text-secondary;
    font-family: $font-mono;
    font-size: $font-size-xs;
    letter-spacing: 1px;
  }

  :deep(.el-input__wrapper),
  :deep(.el-select .el-input__wrapper) {
    background: $bg-card;
    border: 1px solid $border-color;
    box-shadow: none;

    &:hover,
    &.is-focus {
      border-color: rgba(0, 240, 255, 0.4);
    }
  }

  :deep(.el-input__inner) {
    color: $text-primary;
  }
}

.hud-select--full {
  width: 100%;

  :deep(.el-input__wrapper) {
    background: $bg-card;
    border: 1px solid $border-color;
    box-shadow: none;

    &:hover,
    &.is-focus {
      border-color: rgba(0, 240, 255, 0.4);
    }
  }

  :deep(.el-input__inner) {
    color: $text-primary;
    font-family: $font-mono;
    font-size: $font-size-sm;
  }
}

// Stats grid
.stats-grid {
  display: grid;
  grid-template-columns: repeat(5, 1fr);
  gap: $spacing-md;
}

.stat-box {
  background: $bg-card;
  border: 1px solid $border-color;
  border-radius: $radius-sm;
  padding: $spacing-md;
  text-align: center;
  transition: all $transition-fast;

  &:hover {
    border-color: rgba(0, 240, 255, 0.2);
  }

  &__value {
    display: block;
    font-family: $font-mono;
    font-size: 24px;
    font-weight: 700;
    color: $accent-cyan;
    line-height: 1;
    margin-bottom: $spacing-xs;
  }

  &__label {
    font-family: $font-mono;
    font-size: $font-size-xs;
    color: $text-muted;
    letter-spacing: 1px;
  }
}

// About section
.about-grid {
  display: grid;
  grid-template-columns: auto 1fr;
  gap: $spacing-sm $spacing-lg;
  align-items: center;
}

.about-label {
  font-family: $font-mono;
  font-size: $font-size-xs;
  color: $text-muted;
  letter-spacing: 1px;
}

.about-value {
  font-family: $font-mono;
  font-size: $font-size-sm;
  color: $text-primary;

  &--highlight {
    color: $accent-cyan;
    font-weight: 600;
  }
}

// Dark table overrides
.hud-table {
  --el-table-bg-color: #{$bg-card};
  --el-table-tr-bg-color: #{$bg-card};
  --el-table-header-bg-color: #{$bg-secondary};
  --el-table-row-hover-bg-color: rgba(0, 240, 255, 0.04);
  --el-table-border-color: #{$border-color};
  --el-table-text-color: #{$text-primary};
  --el-table-header-text-color: #{$accent-cyan};
  --el-table-current-row-bg-color: rgba(0, 240, 255, 0.06);

  :deep(.el-table__inner-wrapper::before) {
    display: none;
  }
}

// Dialog overrides
.hud-dialog {
  :deep(.el-dialog) {
    background: $bg-secondary;
    border: 1px solid $border-color;
    border-radius: $radius-md;
  }

  :deep(.el-dialog__header) {
    border-bottom: 1px solid $border-color;
    padding: $spacing-md $spacing-lg;
  }

  :deep(.el-dialog__title) {
    font-family: $font-mono;
    color: $accent-cyan;
    font-size: $font-size-base;
    letter-spacing: 1px;
  }

  :deep(.el-dialog__body) {
    padding: $spacing-lg;
  }

  :deep(.el-dialog__footer) {
    border-top: 1px solid $border-color;
    padding: $spacing-md $spacing-lg;
    display: flex;
    justify-content: flex-end;
    gap: $spacing-sm;
  }
}
</style>
