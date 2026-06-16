<template>
  <div class="farming-form-page">
    <div class="page-wrapper">
      <h1 class="page-title">{{ pageTitle }}</h1>

      <HudPanel :title="pageTitle">
        <el-form
          ref="formRef"
          :model="form"
          :rules="currentRules"
          label-position="top"
          class="hud-form"
          v-loading="loading"
        >
          <!-- ========== 施肥表单 ========== -->
          <template v-if="recordType === 'fertilization'">
            <el-form-item label="日期" prop="date">
              <el-date-picker
                v-model="form.date"
                type="date"
                placeholder="选择日期"
                style="width: 100%"
                value-format="YYYY-MM-DD"
              />
            </el-form-item>
            <el-form-item label="肥料类型" prop="fertilizer_type">
              <el-select v-model="form.fertilizer_type" placeholder="选择肥料类型" style="width: 100%">
                <el-option label="尿素" value="尿素" />
                <el-option label="复合肥" value="复合肥" />
                <el-option label="磷肥" value="磷肥" />
                <el-option label="钾肥" value="钾肥" />
                <el-option label="有机肥" value="有机肥" />
                <el-option label="叶面肥" value="叶面肥" />
                <el-option label="其他" value="其他" />
              </el-select>
            </el-form-item>
            <el-form-item label="具体名称" prop="fertilizer_name">
              <el-input v-model="form.fertilizer_name" placeholder="输入具体肥料名称" />
            </el-form-item>
            <div class="npk-row">
              <el-form-item label="N%" prop="n_content">
                <el-input v-model="form.n_content" placeholder="0" />
              </el-form-item>
              <el-form-item label="P%" prop="p_content">
                <el-input v-model="form.p_content" placeholder="0" />
              </el-form-item>
              <el-form-item label="K%" prop="k_content">
                <el-input v-model="form.k_content" placeholder="0" />
              </el-form-item>
            </div>
            <el-form-item label="施用量 (公斤/亩)" prop="amount">
              <el-input-number v-model="form.amount" :min="0" :step="5" controls-position="right" style="width: 100%" />
            </el-form-item>
            <el-form-item label="施用方式" prop="method">
              <el-select v-model="form.method" placeholder="选择施用方式" style="width: 100%">
                <el-option label="沟施" value="沟施" />
                <el-option label="撒施" value="撒施" />
                <el-option label="穴施" value="穴施" />
                <el-option label="冲施" value="冲施" />
                <el-option label="叶面喷施" value="叶面喷施" />
              </el-select>
            </el-form-item>
            <el-form-item label="关联地块" prop="plot_ids">
              <el-select v-model="form.plot_ids" multiple placeholder="选择地块（可多选）" style="width: 100%">
                <el-option v-for="p in plotOptions" :key="p.id" :label="p.name" :value="p.id" />
              </el-select>
            </el-form-item>
          </template>

          <!-- ========== 灌溉表单 ========== -->
          <template v-if="recordType === 'irrigation'">
            <el-form-item label="日期" prop="date">
              <el-date-picker
                v-model="form.date"
                type="date"
                placeholder="选择日期"
                style="width: 100%"
                value-format="YYYY-MM-DD"
              />
            </el-form-item>
            <el-form-item label="灌溉方式" prop="irrigation_method">
              <el-select v-model="form.irrigation_method" placeholder="选择灌溉方式" style="width: 100%">
                <el-option label="漫灌" value="漫灌" />
                <el-option label="沟灌" value="沟灌" />
                <el-option label="滴灌" value="滴灌" />
                <el-option label="喷灌" value="喷灌" />
                <el-option label="雨养" value="雨养" />
              </el-select>
            </el-form-item>
            <el-form-item label="水量 (立方米/亩)" prop="water_amount">
              <el-input-number
                v-model="form.water_amount"
                :min="0"
                :disabled="form.irrigation_method === '雨养'"
                controls-position="right"
                style="width: 100%"
              />
            </el-form-item>
            <el-form-item label="水源类型" prop="water_source">
              <el-select v-model="form.water_source" placeholder="选择水源类型" style="width: 100%">
                <el-option label="河水" value="河水" />
                <el-option label="井水" value="井水" />
                <el-option label="水库" value="水库" />
                <el-option label="雨水" value="雨水" />
                <el-option label="其他" value="其他" />
              </el-select>
            </el-form-item>
          </template>

          <!-- ========== 病虫害表单 ========== -->
          <template v-if="recordType === 'pest_disease'">
            <el-form-item label="发现日期" prop="discovery_date">
              <el-date-picker
                v-model="form.discovery_date"
                type="date"
                placeholder="选择发现日期"
                style="width: 100%"
                value-format="YYYY-MM-DD"
              />
            </el-form-item>
            <el-form-item label="病虫害类型" prop="pest_type">
              <el-select v-model="form.pest_type" placeholder="选择病虫害类型" style="width: 100%">
                <el-option label="二点螟" value="二点螟" />
                <el-option label="条螟" value="条螟" />
                <el-option label="绵蚜" value="绵蚜" />
                <el-option label="蓟马" value="蓟马" />
                <el-option label="黑穗病" value="黑穗病" />
                <el-option label="梢腐病" value="梢腐病" />
                <el-option label="锈病" value="锈病" />
                <el-option label="其他" value="其他" />
              </el-select>
            </el-form-item>
            <el-form-item label="危害部位" prop="affected_part">
              <el-input v-model="form.affected_part" placeholder="输入危害部位" />
            </el-form-item>
            <el-form-item label="危害程度" prop="severity">
              <el-select v-model="form.severity" placeholder="选择危害程度" style="width: 100%">
                <el-option label="轻" value="轻" />
                <el-option label="中" value="中" />
                <el-option label="重" value="重" />
              </el-select>
            </el-form-item>
            <el-form-item label="防治日期" prop="treatment_date">
              <el-date-picker
                v-model="form.treatment_date"
                type="date"
                placeholder="选择防治日期"
                style="width: 100%"
                value-format="YYYY-MM-DD"
              />
            </el-form-item>
            <el-form-item label="农药名称" prop="pesticide_name">
              <el-input v-model="form.pesticide_name" placeholder="输入农药名称" />
            </el-form-item>
            <el-form-item label="用量" prop="pesticide_dosage">
              <el-input v-model="form.pesticide_dosage" placeholder="输入用量" />
            </el-form-item>
            <el-form-item label="防治效果" prop="treatment_effect">
              <el-select v-model="form.treatment_effect" placeholder="选择防治效果" style="width: 100%">
                <el-option label="待观察" value="待观察" />
                <el-option label="有效" value="有效" />
                <el-option label="无效" value="无效" />
              </el-select>
            </el-form-item>
          </template>

          <!-- ========== 采收表单 ========== -->
          <template v-if="recordType === 'harvest'">
            <el-form-item label="计划砍收日期" prop="planned_date">
              <el-date-picker
                v-model="form.planned_date"
                type="date"
                placeholder="选择计划砍收日期"
                style="width: 100%"
                value-format="YYYY-MM-DD"
              />
            </el-form-item>
            <el-form-item label="实际砍收日期" prop="actual_date">
              <el-date-picker
                v-model="form.actual_date"
                type="date"
                placeholder="选择实际砍收日期"
                style="width: 100%"
                value-format="YYYY-MM-DD"
              />
            </el-form-item>
            <el-form-item label="砍收面积 (亩)" prop="harvest_area">
              <el-input-number v-model="form.harvest_area" :min="0" :step="1" controls-position="right" style="width: 100%" />
            </el-form-item>
            <el-form-item label="产量 (吨)" prop="yield_amount">
              <el-input-number v-model="form.yield_amount" :min="0" :step="0.1" :precision="2" controls-position="right" style="width: 100%" />
            </el-form-item>
            <el-form-item label="田间锤度 (%)" prop="brix">
              <el-input-number v-model="form.brix" :min="0" :max="30" :step="0.1" :precision="1" controls-position="right" style="width: 100%" />
            </el-form-item>
            <el-form-item label="蔗糖分 (%)" prop="sugar_content">
              <el-input-number v-model="form.sugar_content" :min="0" :max="25" :step="0.1" :precision="1" controls-position="right" style="width: 100%" />
            </el-form-item>
            <el-form-item label="收购单价 (元/吨)" prop="unit_price">
              <el-input-number v-model="form.unit_price" :min="0" :step="10" controls-position="right" style="width: 100%" />
            </el-form-item>
            <el-form-item label="交售糖厂" prop="factory_id">
              <el-select v-model="form.factory_id" placeholder="选择糖厂" style="width: 100%">
                <el-option v-for="f in factoryOptions" :key="f.id" :label="f.name" :value="f.id" />
              </el-select>
            </el-form-item>
            <el-form-item label="运输费用 (元)" prop="transport_cost">
              <el-input-number v-model="form.transport_cost" :min="0" :step="100" controls-position="right" style="width: 100%" />
            </el-form-item>

            <!-- 自动计算区域 -->
            <div class="auto-calc">
              <div class="auto-calc__row">
                <span class="auto-calc__label">亩产值</span>
                <span class="auto-calc__value">{{ perMuRevenue }} 元/亩</span>
              </div>
              <div class="auto-calc__row">
                <span class="auto-calc__label">总收入</span>
                <span class="auto-calc__value">{{ totalRevenue }} 元</span>
              </div>
            </div>
          </template>

          <div class="form-actions">
            <HudButton type="cyan" :disabled="loading" @click="handleSubmit">保存</HudButton>
            <HudButton type="ghost" @click="handleCancel">取消</HudButton>
          </div>
        </el-form>
      </HudPanel>
    </div>
  </div>
</template>

<script setup>
import { ref, reactive, computed, onMounted } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { ElMessage } from 'element-plus'
import { farmingApi } from '@/api/farming'
import { dictionaryApi } from '@/api/dictionary'
import { plotApi } from '@/api/plot'
import HudPanel from '@/components/hud/HudPanel.vue'
import HudButton from '@/components/hud/HudButton.vue'

const route = useRoute()
const router = useRouter()

const recordType = route.query.type || 'fertilization'
const cycleId = route.query.cycle_id

const formRef = ref(null)
const loading = ref(false)
const plotOptions = ref([])
const factoryOptions = ref([])

const titleMap = {
  fertilization: '新增施肥记录',
  irrigation: '新增灌溉记录',
  pest_disease: '新增病虫害记录',
  harvest: '新增采收记录',
}

const pageTitle = computed(() => titleMap[recordType] || '新增记录')

// 各类型表单数据
const fertilizationForm = reactive({
  date: '',
  fertilizer_type: '',
  fertilizer_name: '',
  n_content: '',
  p_content: '',
  k_content: '',
  amount: 0,
  method: '',
  plot_ids: [],
})

const irrigationForm = reactive({
  date: '',
  irrigation_method: '',
  water_amount: 0,
  water_source: '',
})

const pestDiseaseForm = reactive({
  discovery_date: '',
  pest_type: '',
  affected_part: '',
  severity: '',
  treatment_date: '',
  pesticide_name: '',
  pesticide_dosage: '',
  treatment_effect: '',
})

const harvestForm = reactive({
  planned_date: '',
  actual_date: '',
  harvest_area: 0,
  yield_amount: 0,
  brix: 0,
  sugar_content: 0,
  unit_price: 0,
  factory_id: '',
  transport_cost: 0,
})

const currentRules = computed(() => rules[recordType] || {})

const form = computed(() => {
  switch (recordType) {
    case 'fertilization': return fertilizationForm
    case 'irrigation': return irrigationForm
    case 'pest_disease': return pestDiseaseForm
    case 'harvest': return harvestForm
    default: return fertilizationForm
  }
})

const rules = {
  fertilization: {
    date: [{ required: true, message: '请选择日期', trigger: 'change' }],
    fertilizer_type: [{ required: true, message: '请选择肥料类型', trigger: 'change' }],
    amount: [{ required: true, message: '请输入施用量', trigger: 'blur' }],
    method: [{ required: true, message: '请选择施用方式', trigger: 'change' }],
  },
  irrigation: {
    date: [{ required: true, message: '请选择日期', trigger: 'change' }],
    irrigation_method: [{ required: true, message: '请选择灌溉方式', trigger: 'change' }],
  },
  pest_disease: {
    discovery_date: [{ required: true, message: '请选择发现日期', trigger: 'change' }],
    pest_type: [{ required: true, message: '请选择病虫害类型', trigger: 'change' }],
    severity: [{ required: true, message: '请选择危害程度', trigger: 'change' }],
  },
  harvest: {
    actual_date: [{ required: true, message: '请选择实际砍收日期', trigger: 'change' }],
    harvest_area: [{ required: true, message: '请输入砍收面积', trigger: 'blur' }],
    yield_amount: [{ required: true, message: '请输入产量', trigger: 'blur' }],
  },
}

// 采收自动计算
const perMuRevenue = computed(() => {
  const area = harvestForm.harvest_area || 0
  const yieldAmt = harvestForm.yield_amount || 0
  const price = harvestForm.unit_price || 0
  if (area === 0) return '0.00'
  return ((yieldAmt * price) / area).toFixed(2)
})

const totalRevenue = computed(() => {
  const yieldAmt = harvestForm.yield_amount || 0
  const price = harvestForm.unit_price || 0
  const transport = harvestForm.transport_cost || 0
  return (yieldAmt * price - transport).toFixed(2)
})

const handleSubmit = async () => {
  const valid = await formRef.value.validate().catch(() => false)
  if (!valid) return

  if (!cycleId) {
    ElMessage.warning('缺少周期信息，无法创建记录')
    return
  }

  loading.value = true
  try {
    const data = { ...form.value }
    switch (recordType) {
      case 'fertilization':
        await farmingApi.createFertilization(cycleId, {
          ...data,
          npk_content: [data.n_content, data.p_content, data.k_content].filter(Boolean).join('-') || null,
          related_plots: data.plot_ids,
        })
        break
      case 'irrigation':
        await farmingApi.createIrrigation(cycleId, {
          date: data.date,
          method: data.irrigation_method,
          water_amount: data.water_amount,
          water_source: data.water_source,
        })
        break
      case 'pest_disease':
        await farmingApi.createPestDisease(cycleId, {
          discovery_date: data.discovery_date,
          pest_type: data.pest_type,
          affected_part: data.affected_part,
          severity: data.severity,
          control_date: data.treatment_date,
          pesticide_name: data.pesticide_name,
          dosage: data.pesticide_dosage,
          effect: data.treatment_effect,
        })
        break
      case 'harvest':
        await farmingApi.createHarvest(cycleId, {
          planned_date: data.planned_date,
          actual_date: data.actual_date,
          harvest_area: data.harvest_area,
          yield_tons: data.yield_amount,
          brix_percent: data.brix,
          sugar_percent: data.sugar_content,
          unit_price: data.unit_price,
          sugar_factory: data.factory_id,
          transport_cost: data.transport_cost,
        })
        break
    }
    ElMessage.success('记录保存成功')
    router.back()
  } catch {
    // 错误已由拦截器处理
  } finally {
    loading.value = false
  }
}

const handleCancel = () => {
  router.back()
}

const fetchPlots = async () => {
  try {
    const res = await plotApi.getPlots()
    plotOptions.value = res.data.plots || []
  } catch {
    plotOptions.value = []
  }
}

const fetchFactories = async () => {
  try {
    const res = await dictionaryApi.getSugarFactories()
    factoryOptions.value = res.data.factories || []
  } catch {
    factoryOptions.value = []
  }
}

onMounted(() => {
  if (recordType === 'fertilization') {
    fetchPlots()
  }
  if (recordType === 'harvest') {
    fetchFactories()
  }
})
</script>

<style lang="scss" scoped>
@use '@/styles/variables' as *;

.farming-form-page {
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

.npk-row {
  display: grid;
  grid-template-columns: 1fr 1fr 1fr;
  gap: $spacing-sm;
}

.auto-calc {
  margin-top: $spacing-md;
  padding: $spacing-md;
  background: rgba(0, 240, 255, 0.04);
  border: 1px solid rgba(0, 240, 255, 0.15);
  border-radius: $radius-md;

  &__row {
    display: flex;
    justify-content: space-between;
    align-items: center;
    padding: $spacing-xs 0;

    &:not(:last-child) {
      border-bottom: 1px solid rgba($border-color, 0.5);
    }
  }

  &__label {
    font-size: $font-size-sm;
    color: $text-muted;
    font-family: $font-mono;
  }

  &__value {
    font-size: $font-size-md;
    color: $accent-cyan;
    font-family: $font-mono;
    font-weight: 600;
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
