<template>
  <div class="farming-record-page">
    <div class="page-header">
      <h1 class="page-title">农事记录</h1>
      <div class="filter-bar">
        <el-select
          v-model="filters.plot_id"
          placeholder="地块筛选"
          clearable
          style="width: 160px"
          @change="onPlotChange"
        >
          <el-option
            v-for="p in plotOptions"
            :key="p.id"
            :label="p.name"
            :value="p.id"
          />
        </el-select>
        <el-select
          v-model="filters.cycle_id"
          placeholder="周期筛选"
          clearable
          style="width: 160px"
          :disabled="!filters.plot_id"
        >
          <el-option
            v-for="c in cycleOptions"
            :key="c.id"
            :label="c.cycle_type"
            :value="c.id"
          />
        </el-select>
        <el-select v-model="filters.type" placeholder="记录类型" clearable style="width: 140px">
          <el-option label="全部" value="" />
          <el-option label="施肥" value="fertilization" />
          <el-option label="灌溉" value="irrigation" />
          <el-option label="病虫害" value="pest_disease" />
          <el-option label="采收" value="harvest" />
        </el-select>
        <el-date-picker
          v-model="filters.dateRange"
          type="daterange"
          range-separator="至"
          start-placeholder="开始日期"
          end-placeholder="结束日期"
          value-format="YYYY-MM-DD"
          style="width: 260px"
        />
      </div>
    </div>

    <div class="table-wrapper" v-loading="loading">
      <el-table
        :data="filteredRecords"
        class="hud-table"
        :header-cell-style="headerStyle"
        :cell-style="cellStyle"
        @row-click="handleRowClick"
        empty-text="暂无农事记录"
      >
        <el-table-column prop="date" label="日期" width="120" />
        <el-table-column label="类型" width="120">
          <template #default="{ row }">
            <span class="type-tag" :class="`type-tag--${row.type}`">
              <span class="type-tag__dot" />
              {{ typeLabelMap[row.type] || row.type }}
            </span>
          </template>
        </el-table-column>
        <el-table-column prop="plot_name" label="地块" width="140" />
        <el-table-column prop="cycle_label" label="周期" width="120" />
        <el-table-column prop="summary" label="详情摘要" min-width="200" show-overflow-tooltip />
        <el-table-column label="操作" width="100" fixed="right">
          <template #default="{ row }">
            <span class="action-link" @click.stop="viewDetail(row)">查看</span>
          </template>
        </el-table-column>
      </el-table>

      <div class="pagination-wrapper">
        <el-pagination
          v-model:current-page="pagination.page"
          v-model:page-size="pagination.pageSize"
          :total="pagination.total"
          :page-sizes="[10, 20, 50]"
          layout="total, sizes, prev, pager, next"
          background
          @current-change="fetchRecords"
          @size-change="fetchRecords"
        />
      </div>
    </div>

    <!-- 记录详情弹窗 -->
    <el-dialog
      v-model="detailVisible"
      title="记录详情"
      width="500px"
      class="hud-dialog"
      :append-to-body="true"
    >
      <div v-if="currentRecord" class="detail-content">
        <div v-for="(val, key) in currentRecord.detail" :key="key" class="detail-row">
          <span class="detail-row__label">{{ key }}</span>
          <span class="detail-row__value">{{ val }}</span>
        </div>
      </div>
    </el-dialog>

    <!-- 浮动新增按钮 -->
    <div class="fab-button">
      <HudButton type="cyan" size="large" @click="goCreate">+ 记一笔</HudButton>
    </div>
  </div>
</template>

<script setup>
import { ref, reactive, computed, onMounted, watch } from 'vue'
import { useRouter } from 'vue-router'
import { plotApi } from '@/api/plot'
import { plantingApi } from '@/api/planting'
import { farmingApi } from '@/api/farming'
import HudButton from '@/components/hud/HudButton.vue'

const router = useRouter()

const loading = ref(false)
const records = ref([])
const plotOptions = ref([])
const cycleOptions = ref([])
const detailVisible = ref(false)
const currentRecord = ref(null)

const filters = reactive({
  plot_id: '',
  cycle_id: '',
  type: '',
  dateRange: null,
})

const pagination = reactive({
  page: 1,
  pageSize: 10,
  total: 0,
})

const typeLabelMap = {
  fertilization: '施肥',
  irrigation: '灌溉',
  pest_disease: '病虫害',
  harvest: '采收',
}

const headerStyle = {
  background: '#111820',
  color: '#8b9bb4',
  fontFamily: 'Roboto Mono, monospace',
  fontSize: '12px',
  borderBottom: '1px solid #1a2332',
}

const cellStyle = {
  background: '#0d1117',
  color: '#e0e6ed',
  borderBottom: '1px solid #1a2332',
}

const filteredRecords = computed(() => {
  let list = records.value
  if (filters.type) {
    list = list.filter((r) => r.type === filters.type)
  }
  if (filters.dateRange && filters.dateRange.length === 2) {
    const [start, end] = filters.dateRange
    list = list.filter((r) => r.date >= start && r.date <= end)
  }
  return list
})

const onPlotChange = async (plotId) => {
  filters.cycle_id = ''
  cycleOptions.value = []
  if (!plotId) return
  try {
    const res = await plantingApi.getCycles(plotId)
    cycleOptions.value = res.data.cycles || []
  } catch {
    cycleOptions.value = []
  }
}

const fetchPlots = async () => {
  try {
    const res = await plotApi.getPlots()
    plotOptions.value = res.data.plots || []
  } catch {
    plotOptions.value = []
  }
}

const fetchRecords = async () => {
  loading.value = true
  try {
    const flatRecords = []

    // 如果选了周期，用周期ID查记录
    if (filters.cycle_id) {
      const res = await farmingApi.getRecords(filters.cycle_id)
      const recordsObj = res.data?.records || {}
      for (const [type, items] of Object.entries(recordsObj)) {
        if (Array.isArray(items)) {
          items.forEach((item) => {
            flatRecords.push({
              ...item,
              type,
              plot_name: item.plot_name || '',
              cycle_label: item.cycle_label || '',
            })
          })
        }
      }
    } else if (filters.plot_id && cycleOptions.value.length > 0) {
      // 选了地块但没选周期，加载该地块所有周期的记录
      for (const cycle of cycleOptions.value) {
        try {
          const res = await farmingApi.getRecords(cycle.id)
          const recordsObj = res.data?.records || {}
          for (const [type, items] of Object.entries(recordsObj)) {
            if (Array.isArray(items)) {
              items.forEach((item) => {
                flatRecords.push({
                  ...item,
                  type,
                  plot_name: plotOptions.value.find((p) => p.id === filters.plot_id)?.name || '',
                  cycle_label: cycle.cycle_type || '',
                })
              })
            }
          }
        } catch {
          // ignore single cycle error
        }
      }
    }

    records.value = flatRecords
    pagination.total = records.value.length
  } catch {
    records.value = []
  } finally {
    loading.value = false
  }
}

const handleRowClick = (row) => {
  viewDetail(row)
}

const viewDetail = (row) => {
  currentRecord.value = row
  detailVisible.value = true
}

const goCreate = () => {
  router.push({ name: 'FarmingForm' })
}

watch(() => filters.cycle_id, () => {
  fetchRecords()
})

onMounted(() => {
  fetchPlots()
})
</script>

<style lang="scss" scoped>
@use '@/styles/variables' as *;

.farming-record-page {
  min-height: 100%;
  position: relative;
  padding-bottom: 80px;
}

.page-header {
  margin-bottom: $spacing-lg;
}

.page-title {
  font-family: $font-mono;
  font-size: $font-size-xl;
  font-weight: 700;
  color: $accent-cyan;
  text-shadow: 0 0 20px rgba(0, 240, 255, 0.4);
  margin-bottom: $spacing-md;
  letter-spacing: 2px;
}

.filter-bar {
  display: flex;
  gap: $spacing-sm;
  flex-wrap: wrap;

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

  :deep(.el-date-editor) {
    .el-input__wrapper {
      background: $bg-secondary;
    }
  }

  :deep(.el-range-input) {
    color: $text-primary;
    background: transparent;
  }

  :deep(.el-range-separator) {
    color: $text-muted;
  }
}

.table-wrapper {
  background: $bg-card;
  border: 1px solid $border-color;
  border-radius: $radius-md;
  overflow: hidden;
}

.hud-table {
  --el-table-bg-color: #0d1117;
  --el-table-tr-bg-color: #0d1117;
  --el-table-header-bg-color: #111820;
  --el-table-row-hover-bg-color: rgba(0, 240, 255, 0.05);
  --el-table-border-color: #1a2332;
  --el-table-text-color: #e0e6ed;
  --el-table-header-text-color: #8b9bb4;
  width: 100%;
  cursor: pointer;
}

.type-tag {
  display: inline-flex;
  align-items: center;
  gap: 6px;
  font-size: $font-size-sm;
  font-family: $font-mono;

  &__dot {
    width: 8px;
    height: 8px;
    border-radius: 50%;
    flex-shrink: 0;
  }

  &--fertilization {
    color: $accent-green;
    .type-tag__dot { background: $accent-green; box-shadow: 0 0 4px rgba(57, 255, 20, 0.5); }
  }

  &--irrigation {
    color: $accent-cyan;
    .type-tag__dot { background: $accent-cyan; box-shadow: 0 0 4px rgba(0, 240, 255, 0.5); }
  }

  &--pest_disease {
    color: $accent-orange;
    .type-tag__dot { background: $accent-orange; box-shadow: 0 0 4px rgba(255, 107, 53, 0.5); }
  }

  &--harvest {
    color: $accent-cyan;
    .type-tag__dot { background: $accent-cyan; box-shadow: 0 0 4px rgba(0, 240, 255, 0.5); }
  }
}

.action-link {
  color: $accent-cyan;
  cursor: pointer;
  font-size: $font-size-sm;
  font-family: $font-mono;
  transition: opacity $transition-fast;

  &:hover {
    opacity: 0.7;
  }
}

.pagination-wrapper {
  padding: $spacing-md;
  display: flex;
  justify-content: flex-end;

  :deep(.el-pagination) {
    --el-pagination-bg-color: #111820;
    --el-pagination-text-color: #8b9bb4;
    --el-pagination-button-bg-color: #111820;
    --el-pagination-hover-color: #00f0ff;
  }
}

.fab-button {
  position: fixed;
  bottom: $spacing-lg;
  right: $spacing-xl;
  z-index: $z-fixed;
}

.detail-content {
  .detail-row {
    display: flex;
    justify-content: space-between;
    padding: $spacing-xs 0;
    border-bottom: 1px solid rgba($border-color, 0.5);

    &:last-child {
      border-bottom: none;
    }

    &__label {
      font-size: $font-size-sm;
      color: $text-muted;
      font-family: $font-mono;
    }

    &__value {
      font-size: $font-size-sm;
      color: $text-primary;
    }
  }
}
</style>
