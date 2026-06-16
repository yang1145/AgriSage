<template>
  <div class="variety-list-page">
    <!-- Header -->
    <div class="page-header">
      <h1 class="page-title">品种图鉴</h1>
      <div class="page-actions">
        <el-input
          v-model="searchText"
          placeholder="搜索名称/选育单位/适宜区域..."
          class="hud-search"
          :prefix-icon="Search"
          clearable
          @input="onSearch"
        />
        <HudButton type="cyan" icon="Plus" @click="showAddDialog = true">
          添加品种
        </HudButton>
      </div>
    </div>

    <!-- Loading -->
    <div v-if="loading" class="page-loading">
      <el-icon class="is-loading" :size="32"><Loading /></el-icon>
      <span>正在加载品种数据...</span>
    </div>

    <!-- Empty -->
    <div v-else-if="filteredVarieties.length === 0" class="page-empty">
      <el-icon :size="48"><Document /></el-icon>
      <span>{{ searchText ? '未找到匹配的品种' : '暂无品种数据' }}</span>
    </div>

    <!-- Variety Grid -->
    <div v-else class="variety-grid">
      <div
        v-for="v in filteredVarieties"
        :key="v.id"
        class="holo-card"
        :class="{ 'holo-card--flipped': flippedId === v.id }"
        @click="flipCard(v.id)"
      >
        <!-- Front -->
        <div class="holo-card__face holo-card__front">
          <div class="holo-card__corner holo-card__corner--tl" />
          <div class="holo-card__corner holo-card__corner--br" />
          <div class="holo-card__name">{{ v.name }}</div>
          <div class="holo-card__badge" :class="maturityClass(v.maturity_type)">
            {{ maturityLabel(v.maturity_type) }}
          </div>
          <div class="holo-card__stats">
            <div class="holo-card__stat">
              <span class="holo-card__stat-label">平均产量</span>
              <span class="holo-card__stat-value">{{ v.avg_yield ?? '--' }}<small> t/ha</small></span>
            </div>
            <div class="holo-card__stat">
              <span class="holo-card__stat-label">平均糖分</span>
              <span class="holo-card__stat-value">{{ v.avg_sugar ?? '--' }}<small> %</small></span>
            </div>
          </div>
          <div v-if="v.is_custom" class="holo-card__custom-tag">自定义</div>
          <div class="holo-card__flip-hint">点击翻转</div>
        </div>

        <!-- Back -->
        <div class="holo-card__face holo-card__back">
          <div class="holo-card__corner holo-card__corner--tl" />
          <div class="holo-card__corner holo-card__corner--br" />
          <div class="holo-card__back-title">{{ v.name }}</div>
          <div class="holo-card__detail-list">
            <div class="holo-card__detail-item">
              <span class="holo-card__detail-label">育种单位</span>
              <span class="holo-card__detail-value">{{ v.breeding_unit || '--' }}</span>
            </div>
            <div class="holo-card__detail-item">
              <span class="holo-card__detail-label">抗性评级</span>
              <span class="holo-card__detail-value">{{ v.resistance_rating || '--' }}</span>
            </div>
            <div class="holo-card__detail-item">
              <span class="holo-card__detail-label">建议宿根年限</span>
              <span class="holo-card__detail-value">{{ v.suggested_ratoon_years ? v.suggested_ratoon_years + ' 年' : '--' }}</span>
            </div>
            <div class="holo-card__detail-item">
              <span class="holo-card__detail-label">适宜区域</span>
              <span class="holo-card__detail-value">{{ v.suitable_area || '--' }}</span>
            </div>
          </div>
          <div class="holo-card__flip-hint">点击翻转</div>
        </div>
      </div>
    </div>

    <!-- Add Variety Dialog -->
    <el-dialog
      v-model="showAddDialog"
      title="添加自定义品种"
      width="480px"
      class="hud-dialog"
      :close-on-click-modal="false"
    >
      <el-form
        ref="addFormRef"
        :model="addForm"
        :rules="addRules"
        label-width="100px"
        label-position="top"
        class="hud-form"
      >
        <el-form-item label="品种名称" prop="name">
          <el-input v-model="addForm.name" placeholder="请输入品种名称" />
        </el-form-item>
        <el-form-item label="熟期类型" prop="maturity_type">
          <el-select v-model="addForm.maturity_type" placeholder="请选择熟期">
            <el-option label="早熟" value="early" />
            <el-option label="中熟" value="mid" />
            <el-option label="晚熟" value="late" />
          </el-select>
        </el-form-item>
        <el-form-item label="平均产量 (t/ha)" prop="avg_yield">
          <el-input-number v-model="addForm.avg_yield" :min="0" :precision="1" />
        </el-form-item>
        <el-form-item label="平均糖分 (%)" prop="avg_sugar">
          <el-input-number v-model="addForm.avg_sugar" :min="0" :max="30" :precision="1" />
        </el-form-item>
        <el-form-item label="育种单位">
          <el-input v-model="addForm.breeding_unit" placeholder="选填" />
        </el-form-item>
        <el-form-item label="抗性评级">
          <el-input v-model="addForm.resistance_rating" placeholder="选填" />
        </el-form-item>
        <el-form-item label="建议宿根年限 (年)">
          <el-input-number v-model="addForm.suggested_ratoon_years" :min="1" :max="10" />
        </el-form-item>
        <el-form-item label="适宜区域">
          <el-input v-model="addForm.suitable_area" placeholder="选填" />
        </el-form-item>
      </el-form>
      <template #footer>
        <HudButton type="ghost" @click="showAddDialog = false">取消</HudButton>
        <HudButton type="cyan" :disabled="submitting" @click="handleAddVariety">
          {{ submitting ? '提交中...' : '确认添加' }}
        </HudButton>
      </template>
    </el-dialog>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { Search, Loading, Document } from '@element-plus/icons-vue'
import { ElMessage } from 'element-plus'
import { dictionaryApi } from '@/api/dictionary'
import HudButton from '@/components/hud/HudButton.vue'

const varieties = ref([])
const loading = ref(false)
const searchText = ref('')
const flippedId = ref(null)
const showAddDialog = ref(false)
const submitting = ref(false)
const addFormRef = ref(null)
let searchTimer = null

const addForm = ref({
  name: '',
  maturity_type: '',
  avg_yield: null,
  avg_sugar: null,
  breeding_unit: '',
  resistance_rating: '',
  suggested_ratoon_years: null,
  suitable_area: '',
})

const addRules = {
  name: [{ required: true, message: '请输入品种名称', trigger: 'blur' }],
  maturity_type: [{ required: true, message: '请选择熟期类型', trigger: 'change' }],
}

const maturityMap = {
  early: '早熟',
  mid: '中熟',
  late: '晚熟',
}

const maturityLabel = (type) => maturityMap[type] || '--'

const maturityClass = (type) => {
  const map = { early: 'badge--green', mid: 'badge--cyan', late: 'badge--orange' }
  return map[type] || ''
}

const filteredVarieties = computed(() => varieties.value)

const flipCard = (id) => {
  flippedId.value = flippedId.value === id ? null : id
}

const onSearch = () => {
  if (searchTimer) clearTimeout(searchTimer)
  searchTimer = setTimeout(() => {
    fetchVarieties(searchText.value)
  }, 300)
}

const fetchVarieties = async (search = '') => {
  loading.value = true
  try {
    const res = await dictionaryApi.getVarieties(search)
    varieties.value = res.data.varieties || []
  } catch {
    ElMessage.error('获取品种数据失败')
  } finally {
    loading.value = false
  }
}

const handleAddVariety = async () => {
  if (!addFormRef.value) return
  await addFormRef.value.validate()
  submitting.value = true
  try {
    await dictionaryApi.createVariety({ ...addForm.value, is_custom: true })
    ElMessage.success('品种添加成功')
    showAddDialog.value = false
    addForm.value = {
      name: '',
      maturity_type: '',
      avg_yield: null,
      avg_sugar: null,
      breeding_unit: '',
      resistance_rating: '',
      suggested_ratoon_years: null,
      suitable_area: '',
    }
    await fetchVarieties()
  } catch {
    ElMessage.error('添加品种失败')
  } finally {
    submitting.value = false
  }
}

onMounted(fetchVarieties)
</script>

<style lang="scss" scoped>
@use '@/styles/variables' as *;

.variety-list-page {
  min-height: 100%;
}

.page-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  margin-bottom: $spacing-lg;
  flex-wrap: wrap;
  gap: $spacing-md;
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
  align-items: center;
  gap: $spacing-md;
}

.hud-search {
  width: 240px;

  :deep(.el-input__wrapper) {
    background: $bg-card;
    border: 1px solid $border-color;
    box-shadow: none;

    &:hover,
    &.is-focus {
      border-color: rgba(0, 240, 255, 0.4);
      box-shadow: 0 0 6px rgba(0, 240, 255, 0.1);
    }
  }

  :deep(.el-input__inner) {
    color: $text-primary;
    font-family: $font-mono;
    font-size: $font-size-sm;

    &::placeholder {
      color: $text-muted;
    }
  }

  :deep(.el-input__prefix .el-icon) {
    color: $accent-cyan;
  }
}

.page-loading,
.page-empty {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  gap: $spacing-md;
  padding: $spacing-2xl;
  color: $text-muted;
  font-family: $font-mono;
  font-size: $font-size-sm;
}

// Holographic Card Grid
.variety-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(260px, 1fr));
  gap: $spacing-lg;
}

.holo-card {
  perspective: 800px;
  height: 260px;
  cursor: pointer;

  &__face {
    position: absolute;
    inset: 0;
    backface-visibility: hidden;
    border-radius: $radius-md;
    background: $bg-card;
    border: 1px solid $border-color;
    padding: $spacing-lg;
    display: flex;
    flex-direction: column;
    transition: transform 0.6s ease, border-color $transition-glow, box-shadow $transition-glow;
    overflow: hidden;

    // Grid pattern
    &::before {
      content: '';
      position: absolute;
      inset: 0;
      background-image:
        linear-gradient(rgba(0, 240, 255, 0.03) 1px, transparent 1px),
        linear-gradient(90deg, rgba(0, 240, 255, 0.03) 1px, transparent 1px);
      background-size: 16px 16px;
      pointer-events: none;
    }
  }

  &__front {
    transform: rotateY(0deg);
  }

  &__back {
    transform: rotateY(180deg);
  }

  &--flipped .holo-card__front {
    transform: rotateY(-180deg);
  }

  &--flipped .holo-card__back {
    transform: rotateY(0deg);
    border-color: rgba(0, 240, 255, 0.4);
    box-shadow: $shadow-glow-cyan;
  }

  &:hover .holo-card__front {
    border-color: rgba(0, 240, 255, 0.3);
    box-shadow: 0 0 8px rgba(0, 240, 255, 0.15);
  }

  // Corner decorations
  &__corner {
    position: absolute;
    width: 14px;
    height: 14px;
    pointer-events: none;
    z-index: 2;

    &--tl {
      top: 0;
      left: 0;
      border-top: 2px solid $accent-cyan;
      border-left: 2px solid $accent-cyan;
    }

    &--br {
      bottom: 0;
      right: 0;
      border-bottom: 2px solid $accent-cyan;
      border-right: 2px solid $accent-cyan;
    }
  }

  &__name {
    font-family: $font-mono;
    font-size: $font-size-lg;
    font-weight: 700;
    color: $accent-cyan;
    text-shadow: 0 0 10px rgba(0, 240, 255, 0.4);
    margin-bottom: $spacing-sm;
    position: relative;
    z-index: 1;
  }

  &__badge {
    display: inline-block;
    font-family: $font-mono;
    font-size: $font-size-xs;
    padding: 2px 8px;
    border-radius: $radius-sm;
    letter-spacing: 1px;
    margin-bottom: $spacing-md;
    position: relative;
    z-index: 1;
    width: fit-content;

    &.badge--green {
      color: $accent-green;
      border: 1px solid rgba(57, 255, 20, 0.3);
      background: rgba(57, 255, 20, 0.08);
    }

    &.badge--cyan {
      color: $accent-cyan;
      border: 1px solid rgba(0, 240, 255, 0.3);
      background: rgba(0, 240, 255, 0.08);
    }

    &.badge--orange {
      color: $accent-orange;
      border: 1px solid rgba(255, 107, 53, 0.3);
      background: rgba(255, 107, 53, 0.08);
    }
  }

  &__stats {
    display: flex;
    gap: $spacing-lg;
    flex: 1;
    position: relative;
    z-index: 1;
  }

  &__stat {
    display: flex;
    flex-direction: column;
    gap: 4px;
  }

  &__stat-label {
    font-family: $font-mono;
    font-size: $font-size-xs;
    color: $text-muted;
    letter-spacing: 1px;
  }

  &__stat-value {
    font-family: $font-mono;
    font-size: $font-size-md;
    font-weight: 700;
    color: $text-primary;

    small {
      font-size: $font-size-xs;
      color: $text-secondary;
      font-weight: 400;
    }
  }

  &__custom-tag {
    position: absolute;
    top: $spacing-sm;
    right: $spacing-sm;
    font-family: $font-mono;
    font-size: 10px;
    color: $accent-orange;
    border: 1px solid rgba(255, 107, 53, 0.3);
    background: rgba(255, 107, 53, 0.08);
    padding: 1px 6px;
    border-radius: $radius-sm;
    z-index: 2;
  }

  &__flip-hint {
    font-family: $font-mono;
    font-size: 10px;
    color: $text-muted;
    text-align: center;
    margin-top: auto;
    position: relative;
    z-index: 1;
  }

  // Back face styles
  &__back-title {
    font-family: $font-mono;
    font-size: $font-size-base;
    font-weight: 700;
    color: $accent-cyan;
    margin-bottom: $spacing-md;
    position: relative;
    z-index: 1;
  }

  &__detail-list {
    display: flex;
    flex-direction: column;
    gap: $spacing-sm;
    flex: 1;
    position: relative;
    z-index: 1;
  }

  &__detail-item {
    display: flex;
    justify-content: space-between;
    align-items: center;
    padding-bottom: $spacing-xs;
    border-bottom: 1px solid $border-color;
  }

  &__detail-label {
    font-family: $font-mono;
    font-size: $font-size-xs;
    color: $text-muted;
    letter-spacing: 1px;
  }

  &__detail-value {
    font-family: $font-mono;
    font-size: $font-size-sm;
    color: $text-primary;
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

  :deep(.el-input-number) {
    .el-input__wrapper {
      background: $bg-card;
      border: 1px solid $border-color;
    }
  }
}
</style>
