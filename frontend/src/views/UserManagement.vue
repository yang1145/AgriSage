<template>
  <div class="user-management-page">
    <!-- Header -->
    <div class="page-header">
      <h1 class="page-title">用户管理</h1>
      <div class="page-actions">
        <HudButton type="cyan" @click="openAddDialog">
          <el-icon :size="16"><Plus /></el-icon>
          添加用户
        </HudButton>
      </div>
    </div>

    <!-- User Table -->
    <HudPanel title="USER LIST / 用户列表">
      <div class="table-wrapper">
        <el-table
          v-loading="loading"
          :data="users"
          class="hud-table"
          :header-cell-style="headerStyle"
          :cell-style="cellStyle"
        >
          <el-table-column prop="name" label="姓名" min-width="120">
            <template #default="{ row }">
              <span class="user-name">{{ row.name }}</span>
            </template>
          </el-table-column>
          <el-table-column prop="role" label="角色" min-width="140">
            <template #default="{ row }">
              <span class="role-badge" :class="roleBadgeClass(row.role)">{{ roleLabel(row.role) }}</span>
            </template>
          </el-table-column>
          <el-table-column prop="phone" label="联系电话" min-width="140">
            <template #default="{ row }">
              <span class="phone">{{ row.phone || '--' }}</span>
            </template>
          </el-table-column>
          <el-table-column prop="created_at" label="创建时间" min-width="160">
            <template #default="{ row }">
              <span class="time">{{ formatTime(row.created_at) }}</span>
            </template>
          </el-table-column>
          <el-table-column label="操作" width="160" align="center">
            <template #default="{ row }">
              <span class="action-link" @click="editUser(row)">编辑</span>
              <span
                class="action-link action-link--danger"
                :class="{ 'action-link--disabled': row.id === authStore.user?.id }"
                @click="row.id !== authStore.user?.id && deleteUser(row)"
              >
                {{ row.id === authStore.user?.id ? '当前用户' : '删除' }}
              </span>
            </template>
          </el-table-column>
        </el-table>
      </div>
    </HudPanel>

    <!-- User Dialog -->
    <el-dialog
      v-model="showDialog"
      :title="editingUser ? '编辑用户' : '添加用户'"
      width="480px"
      class="hud-dialog"
      :close-on-click-modal="false"
    >
      <el-form
        ref="formRef"
        :model="form"
        :rules="rules"
        label-position="top"
        class="hud-form"
      >
        <el-form-item label="姓名" prop="name">
          <el-input v-model="form.name" placeholder="请输入姓名" />
        </el-form-item>
        <el-form-item label="角色" prop="role">
          <el-select v-model="form.role" placeholder="请选择角色" class="hud-select--full">
            <el-option label="户主" value="owner" />
            <el-option label="家庭成员" value="family" />
            <el-option label="合作社管理员" value="coop_admin" />
            <el-option label="农技员" value="technician" />
          </el-select>
        </el-form-item>
        <el-form-item label="联系电话" prop="phone">
          <el-input v-model="form.phone" placeholder="请输入联系电话" />
        </el-form-item>
        <el-form-item v-if="!editingUser" label="密码" prop="password">
          <el-input v-model="form.password" type="password" show-password placeholder="请输入密码" />
        </el-form-item>
        <el-form-item v-else label="新密码（留空则不修改）" prop="password">
          <el-input v-model="form.password" type="password" show-password placeholder="如需修改请输入新密码" />
        </el-form-item>
      </el-form>
      <template #footer>
        <HudButton type="ghost" @click="closeDialog">取消</HudButton>
        <HudButton type="cyan" :disabled="submitting" @click="handleSubmit">
          {{ submitting ? '提交中...' : '确认' }}
        </HudButton>
      </template>
    </el-dialog>
  </div>
</template>

<script setup>
import { ref, reactive, onMounted } from 'vue'
import { ElMessage, ElMessageBox } from 'element-plus'
import { userApi } from '@/api/user'
import { useAuthStore } from '@/stores/auth'
import HudPanel from '@/components/hud/HudPanel.vue'
import HudButton from '@/components/hud/HudButton.vue'
import { Plus } from '@element-plus/icons-vue'
import dayjs from 'dayjs'

const authStore = useAuthStore()

const users = ref([])
const loading = ref(false)
const showDialog = ref(false)
const editingUser = ref(null)
const submitting = ref(false)
const formRef = ref(null)

const form = reactive({
  name: '',
  role: '',
  phone: '',
  password: '',
})

const rules = {
  name: [{ required: true, message: '请输入姓名', trigger: 'blur' }],
  role: [{ required: true, message: '请选择角色', trigger: 'change' }],
  password: [
    { required: true, message: '请输入密码', trigger: 'blur' },
    { min: 6, message: '密码至少6位', trigger: 'blur' },
  ],
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

const formatTime = (time) => {
  if (!time) return '--'
  return dayjs(time).format('YYYY-MM-DD HH:mm')
}

const fetchUsers = async () => {
  loading.value = true
  try {
    const res = await userApi.getUsers()
    users.value = res.data.users || []
  } catch {
    users.value = []
  } finally {
    loading.value = false
  }
}

const openAddDialog = () => {
  editingUser.value = null
  Object.assign(form, { name: '', role: '', phone: '', password: '' })
  showDialog.value = true
}

const editUser = (user) => {
  editingUser.value = user
  Object.assign(form, {
    name: user.name,
    role: user.role,
    phone: user.phone || '',
    password: '',
  })
  showDialog.value = true
}

const deleteUser = async (user) => {
  try {
    await ElMessageBox.confirm(
      `确定删除用户 "${user.name}" 吗？该操作不可恢复。`,
      '删除确认',
      { confirmButtonText: '确认删除', cancelButtonText: '取消', type: 'warning' }
    )
    await userApi.deleteUser(user.id)
    users.value = users.value.filter((u) => u.id !== user.id)
    ElMessage.success('用户已删除')
  } catch {
    // cancelled or error
  }
}

const closeDialog = () => {
  showDialog.value = false
  editingUser.value = null
  Object.assign(form, { name: '', role: '', phone: '', password: '' })
}

const handleSubmit = async () => {
  if (!formRef.value) return
  await formRef.value.validate()
  submitting.value = true
  try {
    const data = { ...form }
    if (!data.password) delete data.password
    if (editingUser.value) {
      await userApi.updateUser(editingUser.value.id, data)
    } else {
      await userApi.createUser(data)
    }
    ElMessage.success(editingUser.value ? '用户已更新' : '用户已添加')
    closeDialog()
    await fetchUsers()
  } catch {
    ElMessage.error('操作失败')
  } finally {
    submitting.value = false
  }
}

onMounted(() => {
  fetchUsers()
})
</script>

<style lang="scss" scoped>
@use '@/styles/variables' as *;

.user-management-page {
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

.page-actions {
  display: flex;
  gap: $spacing-sm;
}

.table-wrapper {
  overflow-x: auto;
}

.user-name {
  color: $accent-cyan;
  font-weight: 600;
}

.phone,
.time {
  color: $text-secondary;
  font-size: $font-size-sm;
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

  &--disabled {
    color: $text-muted;
    cursor: not-allowed;
    opacity: 0.5;

    &:hover {
      text-shadow: none;
    }
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
