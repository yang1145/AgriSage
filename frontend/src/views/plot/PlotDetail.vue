<template>
  <div class="plot-detail">
    <!-- 加载状态 -->
    <div v-if="loading" class="plot-detail__loading">
      <el-icon class="is-loading" :size="32"><Loading /></el-icon>
      <span>加载地块数据...</span>
    </div>

    <!-- 错误状态 -->
    <div v-else-if="loadError" class="plot-detail__error">
      <span>加载失败: {{ loadError }}</span>
      <HudButton type="ghost" size="small" @click="loadData">重试</HudButton>
    </div>

    <!-- 主内容 -->
    <template v-else-if="plot">
      <!-- 左侧信息面板 -->
      <aside class="plot-detail__sidebar">
        <!-- 基本信息 -->
        <HudPanel title="地块信息" class="plot-detail__panel">
          <div class="plot-detail__name-row">
            <template v-if="editing">
              <el-input v-model="editForm.name" size="small" class="plot-detail__edit-input" />
            </template>
            <template v-else>
              <span class="plot-detail__name">{{ plot.name }}</span>
            </template>
          </div>

          <div class="plot-detail__status-row">
            <HudStatusLight :status="plot.status || 'idle'" />
            <span class="plot-detail__status-text">{{ statusLabel(plot.status) }}</span>
          </div>

          <div class="plot-detail__info-grid">
            <div class="plot-detail__info-item">
              <span class="plot-detail__info-label">面积</span>
              <span class="plot-detail__info-value">{{ plot.area?.toFixed(1) || '-' }} 亩</span>
            </div>
            <div class="plot-detail__info-item">
              <span class="plot-detail__info-label">海拔</span>
              <span class="plot-detail__info-value">{{ plot.elevation ?? '-' }} m</span>
            </div>
            <div class="plot-detail__info-item">
              <span class="plot-detail__info-label">坡度</span>
              <span class="plot-detail__info-value">{{ plot.slope ?? '-' }}°</span>
            </div>
            <div class="plot-detail__info-item">
              <span class="plot-detail__info-label">坡向</span>
              <span class="plot-detail__info-value">{{ plot.slope_aspect || '-' }}</span>
            </div>
          </div>

          <div class="plot-detail__section-title">土壤信息</div>
          <div class="plot-detail__info-grid">
            <div class="plot-detail__info-item">
              <span class="plot-detail__info-label">类型</span>
              <template v-if="editing">
                <el-select v-model="editForm.soil_type" size="small" class="plot-detail__edit-select">
                  <el-option label="红壤" value="红壤" />
                  <el-option label="赤红壤" value="赤红壤" />
                  <el-option label="砖红壤" value="砖红壤" />
                  <el-option label="石灰土" value="石灰土" />
                  <el-option label="紫色土" value="紫色土" />
                </el-select>
              </template>
              <span v-else class="plot-detail__info-value">{{ plot.soil_type || '-' }}</span>
            </div>
            <div class="plot-detail__info-item">
              <span class="plot-detail__info-label">pH</span>
              <template v-if="editing">
                <el-input-number v-model="editForm.soil_ph" :min="0" :max="14" :step="0.1" :precision="1" size="small" controls-position="right" />
              </template>
              <span v-else class="plot-detail__info-value">{{ plot.soil_ph ?? '-' }}</span>
            </div>
            <div class="plot-detail__info-item">
              <span class="plot-detail__info-label">有机质</span>
              <template v-if="editing">
                <el-input-number v-model="editForm.organic_matter" :min="0" :max="100" :step="0.1" :precision="2" size="small" controls-position="right" />
              </template>
              <span v-else class="plot-detail__info-value">{{ plot.organic_matter ?? '-' }}%</span>
            </div>
            <div class="plot-detail__info-item">
              <span class="plot-detail__info-label">土层厚度</span>
              <template v-if="editing">
                <el-input-number v-model="editForm.soil_depth" :min="0" :max="500" :step="5" size="small" controls-position="right" />
              </template>
              <span v-else class="plot-detail__info-value">{{ plot.soil_depth ?? '-' }} cm</span>
            </div>
          </div>

          <div class="plot-detail__actions">
            <template v-if="editing">
              <HudButton type="cyan" size="small" :disabled="saving" @click="onSaveEdit">
                {{ saving ? '保存中...' : '确认' }}
              </HudButton>
              <HudButton type="ghost" size="small" @click="onCancelEdit">取消</HudButton>
            </template>
            <template v-else>
              <HudButton type="cyan" size="small" @click="onStartEdit">编辑</HudButton>
              <HudButton
                v-if="isOwner"
                type="orange"
                size="small"
                @click="onDeletePlot"
              >
                删除
              </HudButton>
            </template>
          </div>
        </HudPanel>

        <!-- 种植周期 -->
        <HudPanel title="种植周期" class="plot-detail__panel plot-detail__cycles-panel">
          <div v-if="cyclesLoading" class="plot-detail__loading-sm">
            <el-icon class="is-loading" :size="16"><Loading /></el-icon>
          </div>
          <div v-else-if="cycles.length === 0" class="plot-detail__empty-sm">
            暂无种植周期
          </div>
          <div v-else class="plot-detail__cycle-list">
            <div
              v-for="cycle in cycles"
              :key="cycle.id"
              class="plot-detail__cycle-item"
              @click="router.push(`/cycles/${cycle.id}`)"
            >
              <span class="plot-detail__cycle-type" :class="`plot-detail__cycle-type--${cycle.cycle_type || 'default'}`">
                {{ cycleTypeLabel(cycle.cycle_type) }}
              </span>
              <div class="plot-detail__cycle-info">
                <span class="plot-detail__cycle-variety">{{ cycle.variety_name || '-' }}</span>
                <span class="plot-detail__cycle-date">{{ cycle.plant_date || '-' }}</span>
              </div>
              <span class="plot-detail__cycle-status">{{ cycleStatusLabel(cycle.status) }}</span>
            </div>
          </div>
          <div class="plot-detail__cycle-add">
            <HudButton type="ghost" size="small" @click="router.push(`/plots/${plotId}/cycle/create`)">
              + 新建周期
            </HudButton>
          </div>
        </HudPanel>
      </aside>

      <!-- 右侧内容区域 -->
      <div class="plot-detail__content">
        <div class="plot-detail__tabs">
          <button
            v-for="tab in tabs"
            :key="tab.key"
            class="plot-detail__tab"
            :class="{ 'plot-detail__tab--active': activeTab === tab.key }"
            @click="activeTab = tab.key"
          >
            {{ tab.label }}
          </button>
        </div>

        <div class="plot-detail__tab-content">
          <!-- 地图 -->
          <div v-show="activeTab === 'map'" class="plot-detail__tab-pane">
            <PlotMap
              :plots="[plot]"
              :center="plotCenter"
              :zoom="14"
            />
          </div>

          <!-- 影像 -->
          <div v-show="activeTab === 'images'" class="plot-detail__tab-pane">
            <ImageTimeline :images="images" />
            <div v-if="images.length === 0" class="plot-detail__empty-content">
              暂无影像记录
            </div>
          </div>

          <!-- 农事记录 -->
          <div v-show="activeTab === 'records'" class="plot-detail__tab-pane">
            <div v-if="recordsLoading" class="plot-detail__loading-sm">
              <el-icon class="is-loading" :size="16"><Loading /></el-icon>
            </div>
            <div v-else-if="allRecords.length === 0" class="plot-detail__empty-content">
              暂无农事记录
            </div>
            <HudTimeline v-else :items="timelineItems" />
          </div>
        </div>
      </div>
    </template>
  </div>
</template>

<script setup>
import { ref, reactive, computed, onMounted, watch } from 'vue'
import { useRouter, useRoute } from 'vue-router'
import { usePlotStore } from '@/stores/plot'
import { useAuthStore } from '@/stores/auth'
import { plantingApi } from '@/api/planting'
import { farmingApi } from '@/api/farming'
import { storeToRefs } from 'pinia'
import HudPanel from '@/components/hud/HudPanel.vue'
import HudButton from '@/components/hud/HudButton.vue'
import HudStatusLight from '@/components/hud/HudStatusLight.vue'
import HudTimeline from '@/components/hud/HudTimeline.vue'
import PlotMap from '@/components/map/PlotMap.vue'
import ImageTimeline from '@/components/common/ImageTimeline.vue'

const router = useRouter()
const route = useRoute()
const plotStore = usePlotStore()
const authStore = useAuthStore()
const { currentPlot: plot } = storeToRefs(plotStore)

const plotId = computed(() => route.params.id)

const loading = ref(true)
const loadError = ref('')
const saving = ref(false)
const editing = ref(false)

const cycles = ref([])
const cyclesLoading = ref(false)
const images = ref([])
const allRecords = ref([])
const recordsLoading = ref(false)

const activeTab = ref('map')

const tabs = [
  { key: 'map', label: '地图' },
  { key: 'images', label: '影像' },
  { key: 'records', label: '农事记录' },
]

const isOwner = computed(() => authStore.userRole === 'owner')

const plotCenter = computed(() => {
  if (!plot.value?.boundary_geojson) return [22.8, 108.3]
  try {
    const geojson = typeof plot.value.boundary_geojson === 'string'
      ? JSON.parse(plot.value.boundary_geojson)
      : plot.value.boundary_geojson
    const coords = geojson.coordinates?.[0] || []
    if (coords.length === 0) return [22.8, 108.3]
    const lngs = coords.map((c) => c[0])
    const lats = coords.map((c) => c[1])
    return [
      (Math.min(...lats) + Math.max(...lats)) / 2,
      (Math.min(...lngs) + Math.max(...lngs)) / 2,
    ]
  } catch {
    return [22.8, 108.3]
  }
})

const editForm = reactive({
  name: '',
  soil_type: '',
  soil_ph: null,
  organic_matter: null,
  soil_depth: null,
})

const timelineItems = computed(() =>
  allRecords.value.map((r) => ({
    time: r.date || r.created_at || '',
    label: r.type_label || r.type || '',
    description: r.description || r.remark || '',
  }))
)

const statusLabel = (status) => {
  const map = { idle: '闲置', growing: '种植中', harvested: '已收割' }
  return map[status] || status || '未知'
}

const cycleTypeLabel = (type) => {
  const map = { new_planting: '新植', ratoon: '宿根' }
  return map[type] || type || '种植'
}

const cycleStatusLabel = (status) => {
  const map = { active: '进行中', completed: '已完成', aborted: '已终止' }
  return map[status] || status || ''
}

const loadData = async () => {
  loading.value = true
  loadError.value = ''
  try {
    await plotStore.fetchPlot(plotId.value)
    await loadCycles()
  } catch (e) {
    loadError.value = e.message || '加载失败'
  } finally {
    loading.value = false
  }
}

const loadCycles = async () => {
  cyclesLoading.value = true
  try {
    const res = await plantingApi.getCycles(plotId.value)
    cycles.value = res.data.cycles || []
  } catch {
    cycles.value = []
  } finally {
    cyclesLoading.value = false
  }
}

const loadRecords = async () => {
  if (cycles.value.length === 0) {
    allRecords.value = []
    return
  }
  recordsLoading.value = true
  try {
    const promises = cycles.value.map((c) =>
      farmingApi.getRecords(c.id).catch(() => ({ data: { records: {} } }))
    )
    const results = await Promise.all(promises)
    const typeLabels = {
      fertilization: '施肥',
      irrigation: '灌溉',
      pest_disease: '病虫害防治',
      harvest: '收割',
    }
    const typeDateKeys = {
      fertilization: 'date',
      irrigation: 'date',
      pest_disease: 'discovery_date',
      harvest: 'actual_date',
    }
    allRecords.value = results
      .flatMap((r) => {
        const records = r.data?.records || {}
        const flatList = []
        for (const [type, items] of Object.entries(records)) {
          if (Array.isArray(items)) {
            items.forEach((item) => {
              flatList.push({
                ...item,
                type,
                type_label: typeLabels[type] || type,
                date: item[typeDateKeys[type]] || item.date || item.created_at || '',
              })
            })
          }
        }
        return flatList
      })
      .sort((a, b) => (b.date || '').localeCompare(a.date || ''))
  } catch {
    allRecords.value = []
  } finally {
    recordsLoading.value = false
  }
}

const onStartEdit = () => {
  editing.value = true
  editForm.name = plot.value.name || ''
  editForm.soil_type = plot.value.soil_type || ''
  editForm.soil_ph = plot.value.soil_ph ?? null
  editForm.organic_matter = plot.value.organic_matter ?? null
  editForm.soil_depth = plot.value.soil_depth ?? null
}

const onCancelEdit = () => {
  editing.value = false
}

const onSaveEdit = async () => {
  saving.value = true
  try {
    await plotStore.updatePlot(plotId.value, {
      name: editForm.name,
      soil_type: editForm.soil_type,
      soil_ph: editForm.soil_ph,
      organic_matter: editForm.organic_matter,
      soil_depth: editForm.soil_depth,
    })
    editing.value = false
    ElMessage.success('更新成功')
  } catch (e) {
    ElMessage.error('更新失败: ' + (e.message || '未知错误'))
  } finally {
    saving.value = false
  }
}

const onDeletePlot = async () => {
  try {
    await ElMessageBox.confirm('确定要删除该地块吗？此操作不可撤销。', '删除确认', {
      confirmButtonText: '确定删除',
      cancelButtonText: '取消',
      type: 'warning',
    })
    await plotStore.deletePlot(plotId.value)
    ElMessage.success('地块已删除')
    router.push('/plots')
  } catch {
    // 用户取消
  }
}

watch(activeTab, async (tab) => {
  if (tab === 'records' && allRecords.value.length === 0 && !recordsLoading.value) {
    await loadRecords()
  }
})

watch(
  () => cycles.value,
  () => {
    if (activeTab.value === 'records') {
      loadRecords()
    }
  }
)

onMounted(() => {
  loadData()
})
</script>

<style lang="scss" scoped>
@use '@/styles/variables' as *;

.plot-detail {
  display: flex;
  height: calc(100vh - #{$topbar-height} - #{$spacing-lg * 2});
  gap: $spacing-md;

  &__sidebar {
    width: 380px;
    flex-shrink: 0;
    display: flex;
    flex-direction: column;
    gap: $spacing-md;
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

  &__content {
    flex: 1;
    min-width: 0;
    display: flex;
    flex-direction: column;
  }

  &__panel {
    flex-shrink: 0;
  }

  &__cycles-panel {
    flex: 1;
    min-height: 0;

    .hud-panel__content {
      display: flex;
      flex-direction: column;
      min-height: 0;
    }
  }

  &__loading {
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    gap: $spacing-md;
    height: 100%;
    color: $text-muted;
    font-size: $font-size-sm;
  }

  &__loading-sm {
    display: flex;
    align-items: center;
    justify-content: center;
    padding: $spacing-md;
    color: $text-muted;
  }

  &__error {
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    gap: $spacing-md;
    height: 100%;
    color: $status-error;
    font-size: $font-size-sm;
  }

  &__empty-sm {
    text-align: center;
    padding: $spacing-md;
    color: $text-muted;
    font-size: $font-size-sm;
  }

  &__empty-content {
    display: flex;
    align-items: center;
    justify-content: center;
    height: 200px;
    color: $text-muted;
    font-size: $font-size-sm;
  }

  &__name-row {
    margin-bottom: $spacing-sm;
  }

  &__name {
    font-family: $font-mono;
    font-size: $font-size-xl;
    font-weight: 700;
    color: $accent-cyan;
    text-shadow: 0 0 12px rgba(0, 240, 255, 0.4);
    letter-spacing: 1px;
  }

  &__edit-input {
    :deep(.el-input__wrapper) {
      background: $bg-secondary;
      border: 1px solid rgba(0, 240, 255, 0.3);
      box-shadow: none;

      .el-input__inner {
        color: $accent-cyan;
        font-family: $font-mono;
        font-weight: 700;
      }
    }
  }

  &__edit-select {
    width: 100%;

    :deep(.el-select__wrapper) {
      background: $bg-secondary;
      border: 1px solid rgba(0, 240, 255, 0.3);
      box-shadow: none;
    }
  }

  &__status-row {
    display: flex;
    align-items: center;
    gap: $spacing-sm;
    margin-bottom: $spacing-md;
  }

  &__status-text {
    font-size: $font-size-sm;
    color: $text-secondary;
  }

  &__section-title {
    font-family: $font-mono;
    font-size: $font-size-xs;
    color: $text-muted;
    text-transform: uppercase;
    letter-spacing: 1px;
    margin-top: $spacing-md;
    margin-bottom: $spacing-sm;
    padding-bottom: $spacing-xs;
    border-bottom: 1px solid $border-color;
  }

  &__info-grid {
    display: grid;
    grid-template-columns: 1fr 1fr;
    gap: $spacing-sm;
  }

  &__info-item {
    display: flex;
    flex-direction: column;
    gap: 2px;
  }

  &__info-label {
    font-family: $font-mono;
    font-size: $font-size-xs;
    color: $text-muted;
    letter-spacing: 1px;
  }

  &__info-value {
    font-family: $font-mono;
    font-size: $font-size-sm;
    color: $text-primary;
    font-weight: 500;
  }

  &__actions {
    display: flex;
    gap: $spacing-sm;
    margin-top: $spacing-lg;
    padding-top: $spacing-md;
    border-top: 1px solid $border-color;
  }

  &__cycle-list {
    display: flex;
    flex-direction: column;
    gap: 2px;
    overflow-y: auto;
    flex: 1;
    min-height: 0;

    &::-webkit-scrollbar {
      width: 3px;
    }

    &::-webkit-scrollbar-thumb {
      background: rgba(0, 240, 255, 0.15);
      border-radius: 2px;
    }

    &::-webkit-scrollbar-track {
      background: transparent;
    }
  }

  &__cycle-item {
    display: flex;
    align-items: center;
    gap: $spacing-sm;
    padding: $spacing-sm;
    border-radius: $radius-sm;
    cursor: pointer;
    transition: background $transition-fast;

    &:hover {
      background: rgba(0, 240, 255, 0.06);
    }
  }

  &__cycle-type {
    font-family: $font-mono;
    font-size: $font-size-xs;
    padding: 2px 6px;
    border-radius: $radius-sm;
    background: rgba(0, 240, 255, 0.1);
    color: $accent-cyan;
    flex-shrink: 0;

    &--ratoon {
      background: rgba(57, 255, 20, 0.1);
      color: $accent-green;
    }
  }

  &__cycle-info {
    flex: 1;
    min-width: 0;
    display: flex;
    flex-direction: column;
    gap: 2px;
  }

  &__cycle-variety {
    font-size: $font-size-sm;
    color: $text-primary;
    white-space: nowrap;
    overflow: hidden;
    text-overflow: ellipsis;
  }

  &__cycle-date {
    font-family: $font-mono;
    font-size: $font-size-xs;
    color: $text-muted;
  }

  &__cycle-status {
    font-family: $font-mono;
    font-size: $font-size-xs;
    color: $text-secondary;
    flex-shrink: 0;
  }

  &__cycle-add {
    margin-top: $spacing-sm;
    padding-top: $spacing-sm;
    border-top: 1px solid $border-color;
  }

  // 标签页
  &__tabs {
    display: flex;
    gap: 2px;
    margin-bottom: $spacing-md;
    border-bottom: 1px solid $border-color;
  }

  &__tab {
    font-family: $font-mono;
    font-size: $font-size-sm;
    color: $text-secondary;
    background: transparent;
    border: none;
    border-bottom: 2px solid transparent;
    padding: $spacing-sm $spacing-md;
    cursor: pointer;
    transition: all $transition-fast;
    letter-spacing: 1px;

    &:hover {
      color: $text-primary;
    }

    &--active {
      color: $accent-cyan;
      border-bottom-color: $accent-cyan;
    }
  }

  &__tab-content {
    flex: 1;
    min-height: 0;
  }

  &__tab-pane {
    height: 100%;
  }

  // Element Plus 暗色覆盖
  :deep(.el-input-number) {
    width: 100%;

    .el-input__wrapper {
      background: $bg-secondary;
      border: 1px solid $border-color;
      box-shadow: none;
    }

    .el-input-number__decrease,
    .el-input-number__increase {
      background: $bg-card;
      border-color: $border-color;
      color: $text-secondary;

      &:hover {
        color: $accent-cyan;
      }
    }
  }
}
</style>
