<template>
  <div class="plot-create">
    <!-- 左侧表单 -->
    <aside class="plot-create__sidebar">
      <HudPanel title="新建地块" class="plot-create__form-panel">
        <div class="plot-create__title">测绘模式</div>

        <el-form
          ref="formRef"
          :model="form"
          :rules="rules"
          label-position="top"
          class="plot-create__form"
        >
          <el-form-item label="地块名称" prop="name">
            <el-input v-model="form.name" placeholder="输入地块名称" />
          </el-form-item>

          <el-form-item label="乡镇选择" prop="township">
            <el-select
              v-model="form.township"
              placeholder="选择乡镇"
              filterable
              @change="onTownshipChange"
            >
              <el-option
                v-for="t in townships"
                :key="t"
                :label="t"
                :value="t"
              />
            </el-select>
          </el-form-item>

          <el-form-item label="海拔 (米)" prop="elevation">
            <el-input-number
              v-model="form.elevation"
              :min="0"
              :max="5000"
              :step="10"
              controls-position="right"
              placeholder="海拔"
            />
          </el-form-item>

          <el-form-item label="坡度 (度)" prop="slope">
            <el-input-number
              v-model="form.slope"
              :min="0"
              :max="90"
              :step="1"
              controls-position="right"
              placeholder="坡度"
            />
          </el-form-item>

          <el-form-item label="坡向" prop="slope_aspect">
            <el-select v-model="form.slope_aspect" placeholder="选择坡向">
              <el-option label="东" value="东" />
              <el-option label="南" value="南" />
              <el-option label="西" value="西" />
              <el-option label="北" value="北" />
              <el-option label="东南" value="东南" />
              <el-option label="东北" value="东北" />
              <el-option label="西南" value="西南" />
              <el-option label="西北" value="西北" />
            </el-select>
          </el-form-item>

          <el-form-item label="土壤类型" prop="soil_type">
            <el-select v-model="form.soil_type" placeholder="选择土壤类型">
              <el-option label="红壤" value="红壤" />
              <el-option label="赤红壤" value="赤红壤" />
              <el-option label="砖红壤" value="砖红壤" />
              <el-option label="石灰土" value="石灰土" />
              <el-option label="紫色土" value="紫色土" />
            </el-select>
          </el-form-item>

          <el-form-item label="土壤pH" prop="soil_ph">
            <el-input-number
              v-model="form.soil_ph"
              :min="0"
              :max="14"
              :step="0.1"
              :precision="1"
              controls-position="right"
              placeholder="pH值"
            />
          </el-form-item>

          <el-form-item label="有机质 (%)" prop="organic_matter">
            <el-input-number
              v-model="form.organic_matter"
              :min="0"
              :max="100"
              :step="0.1"
              :precision="2"
              controls-position="right"
              placeholder="有机质含量"
            />
          </el-form-item>

          <el-form-item label="土层厚度 (cm)" prop="soil_depth">
            <el-input-number
              v-model="form.soil_depth"
              :min="0"
              :max="500"
              :step="5"
              controls-position="right"
              placeholder="土层厚度"
            />
          </el-form-item>
        </el-form>

        <!-- 面积显示 -->
        <div class="plot-create__area-display">
          <span class="plot-create__area-label">测绘面积</span>
          <div class="plot-create__area-value-row">
            <span class="plot-create__area-value">{{ calculatedArea.toFixed(2) }}</span>
            <span class="plot-create__area-unit">亩</span>
          </div>
        </div>

        <!-- 操作按钮 -->
        <div class="plot-create__actions">
          <HudButton type="cyan" :disabled="saving" @click="onSave">
            {{ saving ? '保存中...' : '保存' }}
          </HudButton>
          <HudButton type="ghost" @click="onCancel">取消</HudButton>
        </div>
      </HudPanel>
    </aside>

    <!-- 右侧地图绘制区域 -->
    <div class="plot-create__map-area">
      <PlotDrawer
        :center="mapCenter"
        :zoom="mapZoom"
        @created="onBoundaryCreated"
      />
    </div>
  </div>
</template>

<script setup>
import { ref, reactive, computed } from 'vue'
import { useRouter } from 'vue-router'
import { usePlotStore } from '@/stores/plot'
import { dictionaryApi } from '@/api/dictionary'
import HudPanel from '@/components/hud/HudPanel.vue'
import HudButton from '@/components/hud/HudButton.vue'
import PlotDrawer from '@/components/map/PlotDrawer.vue'

const router = useRouter()
const plotStore = usePlotStore()

const formRef = ref(null)
const saving = ref(false)
const mapCenter = ref([22.8, 108.3])
const mapZoom = ref(13)

const boundaryGeojson = ref(null)
const calculatedArea = ref(0)

const townships = ref([])

const form = reactive({
  name: '',
  township: '',
  elevation: null,
  slope: null,
  slope_aspect: '',
  soil_type: '',
  soil_ph: null,
  organic_matter: null,
  soil_depth: null,
})

const rules = {
  name: [{ required: true, message: '请输入地块名称', trigger: 'blur' }],
}

const onTownshipChange = async (township) => {
  try {
    const res = await dictionaryApi.getSoilTemplates(township)
    const templates = res.data.templates || []
    const template = templates[0]
    if (template) {
      if (template.soil_type) form.soil_type = template.soil_type
      if (template.default_ph != null) form.soil_ph = template.default_ph
      if (template.default_organic_matter != null) form.organic_matter = template.default_organic_matter
      if (template.default_soil_depth != null) form.soil_depth = template.default_soil_depth
    }
  } catch {
    // 模板加载失败不影响操作
  }
}

const onBoundaryCreated = ({ geojson, area }) => {
  boundaryGeojson.value = geojson
  calculatedArea.value = area
}

const onSave = async () => {
  if (!formRef.value) return

  try {
    await formRef.value.validate()
  } catch {
    return
  }

  if (!boundaryGeojson.value) {
    ElMessage.warning('请在地图上绘制地块边界')
    return
  }

  saving.value = true
  try {
    const data = {
      name: form.name,
      township: form.township,
      elevation: form.elevation,
      slope: form.slope,
      slope_aspect: form.slope_aspect,
      soil_type: form.soil_type,
      soil_ph: form.soil_ph,
      organic_matter: form.organic_matter,
      soil_depth: form.soil_depth,
      area: calculatedArea.value,
      boundary_geojson: boundaryGeojson.value,
    }
    const created = await plotStore.createPlot(data)
    ElMessage.success('地块创建成功')
    router.push(`/plots/${created.id}`)
  } catch (e) {
    ElMessage.error('创建失败: ' + (e.message || '未知错误'))
  } finally {
    saving.value = false
  }
}

const onCancel = () => {
  router.push('/plots')
}
</script>

<style lang="scss" scoped>
@use '@/styles/variables' as *;

.plot-create {
  display: flex;
  height: calc(100vh - #{$topbar-height} - #{$spacing-lg * 2});
  gap: $spacing-md;

  &__sidebar {
    width: 380px;
    flex-shrink: 0;
    overflow-y: auto;
    padding-right: $spacing-xs;

    &::-webkit-scrollbar {
      width: 4px;
    }

    &::-webkit-scrollbar-thumb {
      background: rgba(0, 240, 255, 0.2);
      border-radius: 2px;
    }

    &::-webkit-scrollbar-track {
      background: transparent;
    }
  }

  &__map-area {
    flex: 1;
    min-width: 0;
    position: relative;
  }

  &__title {
    font-family: $font-mono;
    font-size: $font-size-lg;
    font-weight: 700;
    color: $accent-cyan;
    text-shadow: 0 0 12px rgba(0, 240, 255, 0.4);
    margin-bottom: $spacing-md;
    letter-spacing: 2px;
  }

  &__form {
    :deep(.el-form-item__label) {
      font-family: $font-mono;
      font-size: $font-size-xs;
      color: $text-secondary;
      letter-spacing: 1px;
      padding-bottom: $spacing-xs;
    }

    :deep(.el-input__wrapper),
    :deep(.el-select__wrapper),
    :deep(.el-input-number) {
      background: $bg-secondary;
      border: 1px solid $border-color;
      box-shadow: none;
      border-radius: $radius-sm;

      &:hover {
        border-color: rgba(0, 240, 255, 0.3);
      }

      &.is-focus {
        border-color: $accent-cyan;
        box-shadow: 0 0 4px rgba(0, 240, 255, 0.15);
      }
    }

    :deep(.el-input__inner),
    :deep(.el-select__placeholder),
    :deep(.el-input-number__decrease),
    :deep(.el-input-number__increase) {
      color: $text-primary;
      font-family: $font-mono;
      font-size: $font-size-sm;
    }

    :deep(.el-input-number__decrease),
    :deep(.el-input-number__increase) {
      background: $bg-card;
      border-color: $border-color;
      color: $text-secondary;

      &:hover {
        color: $accent-cyan;
      }
    }

    :deep(.el-select__placeholder) {
      color: $text-muted;
    }

    :deep(.el-form-item) {
      margin-bottom: $spacing-md;
    }
  }

  &__area-display {
    margin: $spacing-lg 0;
    padding: $spacing-md;
    background: rgba(0, 240, 255, 0.04);
    border: 1px solid rgba(0, 240, 255, 0.15);
    border-radius: $radius-md;
  }

  &__area-label {
    font-family: $font-mono;
    font-size: $font-size-xs;
    color: $text-muted;
    text-transform: uppercase;
    letter-spacing: 1px;
  }

  &__area-value-row {
    display: flex;
    align-items: baseline;
    gap: $spacing-xs;
    margin-top: $spacing-xs;
  }

  &__area-value {
    font-family: $font-mono;
    font-size: $font-size-2xl;
    font-weight: 700;
    color: $accent-cyan;
    text-shadow: 0 0 8px rgba(0, 240, 255, 0.3);
  }

  &__area-unit {
    font-family: $font-mono;
    font-size: $font-size-sm;
    color: $text-secondary;
  }

  &__actions {
    display: flex;
    gap: $spacing-md;
    margin-top: $spacing-lg;
  }
}
</style>
