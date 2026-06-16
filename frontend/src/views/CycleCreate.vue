<template>
  <div class="cycle-create-page">
    <div class="page-wrapper">
      <h1 class="page-title">创建种植周期</h1>

      <HudPanel title="周期信息">
        <el-form
          ref="formRef"
          :model="form"
          :rules="rules"
          label-position="top"
          class="hud-form"
          v-loading="loading"
        >
          <el-form-item label="植期类型" prop="cycle_type">
            <el-select v-model="form.cycle_type" placeholder="选择植期类型" style="width: 100%">
              <el-option label="新植蔗" value="新植蔗" />
              <el-option label="宿根1年" value="宿根1年" />
              <el-option label="宿根2年" value="宿根2年" />
              <el-option label="宿根3年+" value="宿根3年+" />
            </el-select>
          </el-form-item>

          <el-form-item label="品种选择" prop="variety_id">
            <el-select
              v-model="form.variety_id"
              filterable
              remote
              :remote-method="searchVarieties"
              :loading="varietySearching"
              placeholder="搜索品种"
              style="width: 100%"
              @change="onVarietyChange"
            >
              <el-option
                v-for="v in varietyOptions"
                :key="v.id"
                :label="v.name"
                :value="v.id"
              />
            </el-select>
            <div v-if="selectedVariety" class="variety-card">
              <div class="variety-card__name">{{ selectedVariety.name }}</div>
              <div class="variety-card__attrs">
                <span class="variety-card__attr">
                  <span class="variety-card__label">产量潜力</span>
                  <span class="variety-card__value">{{ selectedVariety.avg_yield || '-' }}</span>
                </span>
                <span class="variety-card__attr">
                  <span class="variety-card__label">糖分</span>
                  <span class="variety-card__value">{{ selectedVariety.avg_sugar || '-' }}</span>
                </span>
                <span class="variety-card__attr">
                  <span class="variety-card__label">抗逆性</span>
                  <span class="variety-card__value">{{ selectedVariety.resistance_rating || '-' }}</span>
                </span>
              </div>
            </div>
          </el-form-item>

          <el-form-item label="种植日期" prop="plant_date">
            <el-date-picker
              v-model="form.plant_date"
              type="date"
              placeholder="选择种植日期"
              style="width: 100%"
              value-format="YYYY-MM-DD"
            />
          </el-form-item>

          <el-form-item label="种苗来源" prop="seed_source">
            <el-select v-model="form.seed_source" placeholder="选择种苗来源" style="width: 100%">
              <el-option label="自留" value="自留" />
              <el-option label="糖厂供种" value="糖厂供种" />
              <el-option label="市场购买" value="市场购买" />
            </el-select>
          </el-form-item>

          <el-form-item label="下种量 (芽/亩)" prop="seed_amount">
            <el-input-number
              v-model="form.seed_amount"
              :min="0"
              :step="100"
              controls-position="right"
              style="width: 100%"
            />
          </el-form-item>

          <el-form-item label="行距 (cm)" prop="row_spacing">
            <el-input-number
              v-model="form.row_spacing"
              :min="0"
              :step="10"
              controls-position="right"
              style="width: 100%"
            />
          </el-form-item>

          <el-form-item label="盖膜情况">
            <el-switch v-model="form.mulch" active-text="已盖膜" inactive-text="未盖膜" />
          </el-form-item>

          <div class="form-actions">
            <HudButton type="cyan" :disabled="loading" @click="handleSubmit">创建</HudButton>
            <HudButton type="ghost" @click="handleCancel">取消</HudButton>
          </div>
        </el-form>
      </HudPanel>
    </div>
  </div>
</template>

<script setup>
import { ref, reactive, watch } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { ElMessage } from 'element-plus'
import { plantingApi } from '@/api/planting'
import { dictionaryApi } from '@/api/dictionary'
import HudPanel from '@/components/hud/HudPanel.vue'
import HudButton from '@/components/hud/HudButton.vue'

const route = useRoute()
const router = useRouter()

const plotId = route.params.id
const formRef = ref(null)
const loading = ref(false)
const varietySearching = ref(false)
const varietyOptions = ref([])
const selectedVariety = ref(null)

const form = reactive({
  cycle_type: '',
  variety_id: null,
  plant_date: '',
  seed_source: '',
  seed_amount: 4000,
  row_spacing: 120,
  mulch: false,
})

const rules = {
  cycle_type: [{ required: true, message: '请选择植期类型', trigger: 'change' }],
  variety_id: [{ required: true, message: '请选择品种', trigger: 'change' }],
  plant_date: [{ required: true, message: '请选择种植日期', trigger: 'change' }],
  seed_source: [{ required: true, message: '请选择种苗来源', trigger: 'change' }],
}

// 宿根类型自动填充上一周期品种
watch(() => form.cycle_type, async (val) => {
  if (val && val !== '新植蔗') {
    try {
      const res = await plantingApi.getCycles(plotId)
      const cycles = res.data.cycles || []
      if (cycles.length > 0) {
        const lastCycle = cycles[cycles.length - 1]
        if (lastCycle.variety_id) {
          form.variety_id = lastCycle.variety_id
          const vRes = await dictionaryApi.getVariety(lastCycle.variety_id)
          selectedVariety.value = vRes.data.variety || vRes.data
          varietyOptions.value = [selectedVariety.value]
        }
      }
    } catch {
      // 静默处理
    }
  }
})

const searchVarieties = async (query) => {
  if (!query) return
  varietySearching.value = true
  try {
    const res = await dictionaryApi.getVarieties(query)
    varietyOptions.value = res.data.varieties || []
  } catch {
    varietyOptions.value = []
  } finally {
    varietySearching.value = false
  }
}

const onVarietyChange = async (val) => {
  if (!val) {
    selectedVariety.value = null
    return
  }
  try {
    const res = await dictionaryApi.getVariety(val)
    selectedVariety.value = res.data.variety || res.data
  } catch {
    selectedVariety.value = null
  }
}

const handleSubmit = async () => {
  const valid = await formRef.value.validate().catch(() => false)
  if (!valid) return

  loading.value = true
  try {
    const res = await plantingApi.createCycle(plotId, { ...form })
    ElMessage.success('种植周期创建成功')
    router.push({ name: 'CycleDetail', params: { id: res.data.id } })
  } catch {
    // 错误已由拦截器处理
  } finally {
    loading.value = false
  }
}

const handleCancel = () => {
  router.back()
}
</script>

<style lang="scss" scoped>
@use '@/styles/variables' as *;

.cycle-create-page {
  min-height: 100%;
}

.page-wrapper {
  max-width: 700px;
  margin: 0 auto;
}

.page-title {
  font-family: $font-mono;
  font-size: $font-size-xl;
  font-weight: 700;
  color: $accent-cyan;
  text-shadow: 0 0 20px rgba(0, 240, 255, 0.4);
  margin-bottom: $spacing-lg;
  letter-spacing: 2px;
}

.hud-form {
  :deep(.el-form-item__label) {
    color: $text-secondary;
    font-family: $font-mono;
    font-size: $font-size-sm;
    letter-spacing: 1px;
  }

  :deep(.el-input__wrapper),
  :deep(.el-select__wrapper) {
    background: $bg-secondary;
    border-color: $border-color;
    box-shadow: none;
  }

  :deep(.el-input__inner),
  :deep(.el-select__placeholder) {
    color: $text-primary;
  }

  :deep(.el-input-number) {
    .el-input__wrapper {
      background: $bg-secondary;
    }
  }
}

.variety-card {
  margin-top: $spacing-sm;
  padding: $spacing-md;
  background: rgba(0, 240, 255, 0.04);
  border: 1px solid rgba(0, 240, 255, 0.15);
  border-radius: $radius-md;

  &__name {
    font-family: $font-mono;
    font-size: $font-size-base;
    color: $accent-cyan;
    margin-bottom: $spacing-sm;
    font-weight: 600;
  }

  &__attrs {
    display: flex;
    gap: $spacing-lg;
  }

  &__attr {
    display: flex;
    flex-direction: column;
    gap: 2px;
  }

  &__label {
    font-size: $font-size-xs;
    color: $text-muted;
    font-family: $font-mono;
  }

  &__value {
    font-size: $font-size-sm;
    color: $text-primary;
    font-weight: 500;
  }
}

.form-actions {
  display: flex;
  gap: $spacing-md;
  margin-top: $spacing-lg;
  padding-top: $spacing-md;
  border-top: 1px solid $border-color;
}
</style>
