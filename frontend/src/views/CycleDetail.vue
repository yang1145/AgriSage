<template>
  <div class="cycle-detail-page" v-loading="loading">
    <div v-if="cycle" class="detail-layout">
      <!-- 左侧面板 -->
      <div class="detail-left">
        <HudPanel title="周期信息">
          <div class="cycle-info">
            <div class="cycle-info__badge" :class="`cycle-info__badge--${badgeClass}`">
              {{ cycle.cycle_type }}
            </div>

            <div class="cycle-info__variety" v-if="variety">
              <span class="cycle-info__variety-name">{{ variety.name }}</span>
              <div class="variety-mini-card">
                <span class="variety-mini-card__item">
                  <span class="variety-mini-card__label">产量</span>
                  <span class="variety-mini-card__val">{{ variety.avg_yield || '-' }}</span>
                </span>
                <span class="variety-mini-card__item">
                  <span class="variety-mini-card__label">糖分</span>
                  <span class="variety-mini-card__val">{{ variety.avg_sugar || '-' }}</span>
                </span>
                <span class="variety-mini-card__item">
                  <span class="variety-mini-card__label">抗逆性</span>
                  <span class="variety-mini-card__val">{{ variety.resistance_rating || '-' }}</span>
                </span>
              </div>
            </div>

            <div class="cycle-info__rows">
              <div class="info-row">
                <span class="info-row__label">种植日期</span>
                <span class="info-row__value">{{ cycle.plant_date || '-' }}</span>
              </div>
              <div class="info-row">
                <span class="info-row__label">种苗来源</span>
                <span class="info-row__value">{{ cycle.seed_source || '-' }}</span>
              </div>
              <div class="info-row">
                <span class="info-row__label">下种量</span>
                <span class="info-row__value">{{ cycle.seed_amount ? cycle.seed_amount + ' 芽/亩' : '-' }}</span>
              </div>
              <div class="info-row">
                <span class="info-row__label">行距</span>
                <span class="info-row__value">{{ cycle.row_spacing ? cycle.row_spacing + ' cm' : '-' }}</span>
              </div>
              <div class="info-row">
                <span class="info-row__label">盖膜</span>
                <span class="info-row__value">{{ cycle.mulch ? '已盖膜' : '未盖膜' }}</span>
              </div>
              <div class="info-row">
                <span class="info-row__label">状态</span>
                <span class="info-row__value">
                  <HudStatusLight :status="cycle.status === '收获完毕' ? 'harvested' : cycle.status === '已废弃' ? 'idle' : 'growing'" />
                  <span class="status-text">{{ statusTextMap[cycle.status] || '生长中' }}</span>
                  <el-dropdown v-if="isOwner" size="small" trigger="click" @command="handleStatusChange">
                    <el-button size="small" type="primary" text style="margin-left: 4px;">变更</el-button>
                    <template #dropdown>
                      <el-dropdown-menu>
                        <el-dropdown-item command="种植中" :disabled="cycle.status === '种植中'">设为生长中</el-dropdown-item>
                        <el-dropdown-item command="收获完毕" :disabled="cycle.status === '收获完毕'">设为已收割</el-dropdown-item>
                        <el-dropdown-item command="已废弃" :disabled="cycle.status === '已废弃'">设为已废弃</el-dropdown-item>
                      </el-dropdown-menu>
                    </template>
                  </el-dropdown>
                </span>
              </div>
            </div>

            <div class="cycle-info__edit">
              <HudButton type="ghost" size="small" @click="handleEdit">编辑</HudButton>
              <HudButton v-if="isOwner" type="ghost" size="small" style="margin-left: 8px; color: #ff4757; border-color: rgba(255, 71, 87, 0.3);" @click="handleDelete">删除周期</HudButton>
            </div>
          </div>
        </HudPanel>

        <HudPanel title="快捷录入" style="margin-top: 16px">
          <div class="quick-actions">
            <HudButton type="green" @click="goFarming('fertilization')">施肥记录</HudButton>
            <HudButton type="cyan" @click="goFarming('irrigation')">灌溉记录</HudButton>
            <HudButton type="orange" @click="goFarming('pest_disease')">病虫害记录</HudButton>
            <HudButton type="cyan" @click="goFarming('harvest')">采收记录</HudButton>
          </div>
        </HudPanel>
      </div>

      <!-- 右侧时间线 -->
      <div class="detail-right">
        <HudPanel title="周期时间线">
          <div v-if="timelineItems.length === 0 && !timelineLoading" class="empty-state">
            暂无时间线记录
          </div>
          <HudTimeline v-else :items="timelineItems">
            <template v-for="(_, index) in timelineItems" :key="index" #[`item-${index}`]="{ item }">
              <div v-if="expandedIndex === index" class="timeline-detail">
                <div v-for="(val, key) in item.detail" :key="key" class="timeline-detail__row">
                  <span class="timeline-detail__key">{{ key }}</span>
                  <span class="timeline-detail__val">{{ val }}</span>
                </div>
              </div>
              <div class="timeline-expand-btn" @click="toggleExpand(index)">
                {{ expandedIndex === index ? '收起' : '展开详情' }}
              </div>
            </template>
          </HudTimeline>
        </HudPanel>
      </div>
    </div>

    <div v-else-if="!loading" class="empty-state">未找到周期信息</div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { ElMessage, ElMessageBox } from 'element-plus'
import { plantingApi } from '@/api/planting'
import { dictionaryApi } from '@/api/dictionary'
import { useAuthStore } from '@/stores/auth'
import HudPanel from '@/components/hud/HudPanel.vue'
import HudButton from '@/components/hud/HudButton.vue'
import HudStatusLight from '@/components/hud/HudStatusLight.vue'
import HudTimeline from '@/components/hud/HudTimeline.vue'

const route = useRoute()
const router = useRouter()
const authStore = useAuthStore()

const cycleId = route.params.id
const isOwner = computed(() => authStore.userRole === 'owner')
const loading = ref(true)
const timelineLoading = ref(false)
const cycle = ref(null)
const variety = ref(null)
const timelineData = ref([])
const expandedIndex = ref(-1)

const statusTextMap = {
  '种植中': '生长中',
  '收获完毕': '已收割',
  '已废弃': '已废弃',
}

const badgeClass = computed(() => {
  const t = cycle.value?.cycle_type
  if (t === '新植蔗') return 'new'
  return 'ratoon'
})

const typeColorMap = {
  fertilization: '#39ff14',
  irrigation: '#00f0ff',
  pest_disease: '#ff6b35',
  harvest: '#00f0ff',
}

const typeLabelMap = {
  fertilization: '施肥',
  irrigation: '灌溉',
  pest_disease: '病虫害',
  harvest: '采收',
  cycle_created: '周期创建',
}

const timelineItems = computed(() => {
  return timelineData.value.map((item) => ({
    time: item.date || item.created_at || '',
    label: typeLabelMap[item.type] || item.type,
    description: item.summary || '',
    active: item.type === 'cycle_created',
    dotColor: typeColorMap[item.type],
    detail: item.detail || {},
  }))
})

const toggleExpand = (index) => {
  expandedIndex.value = expandedIndex.value === index ? -1 : index
}

const fetchData = async () => {
  loading.value = true
  try {
    const res = await plantingApi.getCycle(cycleId)
    cycle.value = res.data.cycle
    if (cycle.value?.variety_id) {
      try {
        const vRes = await dictionaryApi.getVariety(cycle.value.variety_id)
        variety.value = vRes.data.variety || vRes.data
      } catch {
        variety.value = null
      }
    }
  } catch {
    cycle.value = null
  } finally {
    loading.value = false
  }
}

const fetchTimeline = async () => {
  timelineLoading.value = true
  try {
    const res = await plantingApi.getCycleTimeline(cycleId)
    timelineData.value = res.data.timeline || []
  } catch {
    timelineData.value = []
  } finally {
    timelineLoading.value = false
  }
}

const goFarming = (type) => {
  router.push({ name: 'FarmingForm', query: { type, cycle_id: cycleId } })
}

const handleEdit = () => {
  // 可扩展：跳转编辑页
}

const handleStatusChange = async (newStatus) => {
  try {
    await ElMessageBox.confirm(`确定将周期状态变更为「${statusTextMap[newStatus]}」吗？`, '状态变更确认', {
      confirmButtonText: '确认',
      cancelButtonText: '取消',
      type: 'warning',
    })
    await plantingApi.updateCycle(cycleId, { status: newStatus })
    ElMessage.success('状态变更成功')
    await fetchData()
  } catch {
    // cancelled
  }
}

const handleDelete = async () => {
  try {
    await ElMessageBox.confirm('确定删除该种植周期吗？关联的农事记录将一并删除。', '删除确认', {
      confirmButtonText: '确认删除',
      cancelButtonText: '取消',
      type: 'warning',
    })
    await plantingApi.deleteCycle(cycleId)
    ElMessage.success('种植周期已删除')
    router.push('/plots')
  } catch {
    // cancelled
  }
}

onMounted(() => {
  fetchData()
  fetchTimeline()
})
</script>

<style lang="scss" scoped>
@use '@/styles/variables' as *;

.cycle-detail-page {
  min-height: 100%;
}

.detail-layout {
  display: flex;
  gap: $spacing-lg;
  align-items: flex-start;
}

.detail-left {
  width: 350px;
  flex-shrink: 0;
}

.detail-right {
  flex: 1;
  min-width: 0;
}

.cycle-info {
  &__badge {
    display: inline-block;
    padding: 4px 12px;
    border-radius: $radius-sm;
    font-family: $font-mono;
    font-size: $font-size-sm;
    font-weight: 600;
    letter-spacing: 1px;
    margin-bottom: $spacing-md;

    &--new {
      background: rgba(0, 240, 255, 0.1);
      color: $accent-cyan;
      border: 1px solid rgba(0, 240, 255, 0.3);
    }

    &--ratoon {
      background: rgba(57, 255, 20, 0.1);
      color: $accent-green;
      border: 1px solid rgba(57, 255, 20, 0.3);
    }
  }

  &__variety-name {
    font-size: $font-size-md;
    color: $text-primary;
    font-weight: 600;
  }
}

.variety-mini-card {
  display: flex;
  gap: $spacing-md;
  margin-top: $spacing-sm;
  padding: $spacing-sm;
  background: rgba(0, 240, 255, 0.04);
  border: 1px solid rgba(0, 240, 255, 0.1);
  border-radius: $radius-sm;

  &__item {
    display: flex;
    flex-direction: column;
    gap: 2px;
  }

  &__label {
    font-size: $font-size-xs;
    color: $text-muted;
    font-family: $font-mono;
  }

  &__val {
    font-size: $font-size-sm;
    color: $text-primary;
    font-weight: 500;
  }
}

.info-row {
  display: flex;
  justify-content: space-between;
  align-items: center;
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
    display: flex;
    align-items: center;
    gap: $spacing-xs;
  }
}

.status-text {
  font-size: $font-size-sm;
  margin-left: 4px;
}

.cycle-info__edit {
  margin-top: $spacing-md;
  padding-top: $spacing-sm;
  border-top: 1px solid $border-color;
}

.quick-actions {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: $spacing-sm;
}

.empty-state {
  text-align: center;
  padding: $spacing-2xl;
  color: $text-muted;
  font-family: $font-mono;
  font-size: $font-size-sm;
}

.timeline-detail {
  margin-top: $spacing-xs;
  padding: $spacing-sm;
  background: rgba(0, 240, 255, 0.04);
  border: 1px solid rgba(0, 240, 255, 0.1);
  border-radius: $radius-sm;

  &__row {
    display: flex;
    justify-content: space-between;
    padding: 2px 0;
  }

  &__key {
    font-size: $font-size-xs;
    color: $text-muted;
    font-family: $font-mono;
  }

  &__val {
    font-size: $font-size-xs;
    color: $text-primary;
  }
}

.timeline-expand-btn {
  font-size: $font-size-xs;
  color: $accent-cyan;
  cursor: pointer;
  margin-top: 4px;
  font-family: $font-mono;
  opacity: 0.7;
  transition: opacity $transition-fast;

  &:hover {
    opacity: 1;
  }
}
</style>
