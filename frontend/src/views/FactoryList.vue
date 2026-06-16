<template>
  <div class="factory-list-page">
    <!-- Header -->
    <div class="page-header">
      <h1 class="page-title">糖厂通讯录</h1>
      <el-input
        v-model="searchText"
        placeholder="按名称/区域搜索..."
        class="hud-search"
        :prefix-icon="Search"
        clearable
        @input="onSearch"
      />
    </div>

    <!-- Loading -->
    <div v-if="loading" class="page-loading">
      <el-icon class="is-loading" :size="32"><Loading /></el-icon>
      <span>正在加载糖厂数据...</span>
    </div>

    <!-- Empty -->
    <div v-else-if="filteredFactories.length === 0" class="page-empty">
      <el-icon :size="48"><OfficeBuilding /></el-icon>
      <span>{{ searchText ? '未找到匹配的糖厂' : '暂无糖厂数据' }}</span>
    </div>

    <!-- Table -->
    <el-table
      v-else
      :data="filteredFactories"
      class="hud-table"
      :header-cell-style="headerStyle"
      :cell-style="cellStyle"
      stripe
    >
      <el-table-column prop="name" label="糖厂名称" min-width="160">
        <template #default="{ row }">
          <span class="factory-name">{{ row.name }}</span>
        </template>
      </el-table-column>
      <el-table-column prop="city_county" label="所属地市/县" min-width="120" />
      <el-table-column prop="service_scope" label="服务范围" min-width="140" />
      <el-table-column prop="contact_phone" label="联系电话" min-width="140">
        <template #default="{ row }">
          <a v-if="row.contact_phone" :href="`tel:${row.contact_phone}`" class="phone-link">
            {{ row.contact_phone }}
          </a>
          <span v-else class="text-muted">--</span>
        </template>
      </el-table-column>
      <el-table-column label="操作" width="100" align="center">
        <template #default="{ row }">
          <a v-if="row.contact_phone" :href="`tel:${row.contact_phone}`" class="dial-btn">
            拨号
          </a>
          <span v-else class="text-muted">--</span>
        </template>
      </el-table-column>
    </el-table>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { Search, Loading, OfficeBuilding } from '@element-plus/icons-vue'
import { ElMessage } from 'element-plus'
import { dictionaryApi } from '@/api/dictionary'

const factories = ref([])
const loading = ref(false)
const searchText = ref('')
let searchTimer = null

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

const filteredFactories = computed(() => factories.value)

const fetchFactories = async (search = '') => {
  loading.value = true
  try {
    const res = await dictionaryApi.getSugarFactories(search)
    factories.value = res.data.factories || []
  } catch {
    ElMessage.error('获取糖厂数据失败')
  } finally {
    loading.value = false
  }
}

const onSearch = () => {
  if (searchTimer) clearTimeout(searchTimer)
  searchTimer = setTimeout(() => {
    fetchFactories(searchText.value)
  }, 300)
}

onMounted(fetchFactories)
</script>

<style lang="scss" scoped>
@use '@/styles/variables' as *;

.factory-list-page {
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

.factory-name {
  color: $accent-cyan;
  font-weight: 600;
}

.phone-link {
  color: $accent-green;
  text-decoration: none;
  font-family: $font-mono;
  transition: color $transition-fast;

  &:hover {
    color: #5fff5f;
    text-shadow: 0 0 6px rgba(57, 255, 20, 0.3);
  }
}

.dial-btn {
  display: inline-block;
  padding: 2px 12px;
  font-family: $font-mono;
  font-size: $font-size-xs;
  color: $accent-green;
  border: 1px solid rgba(57, 255, 20, 0.3);
  border-radius: $radius-sm;
  background: rgba(57, 255, 20, 0.08);
  text-decoration: none;
  letter-spacing: 1px;
  transition: all $transition-fast;

  &:hover {
    background: rgba(57, 255, 20, 0.15);
    border-color: $accent-green;
    box-shadow: 0 0 8px rgba(57, 255, 20, 0.2);
  }
}

.text-muted {
  color: $text-muted;
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

  :deep(.el-table__body tr.stripe) {
    background: rgba(17, 24, 32, 0.5);
  }

  :deep(.el-table__empty-block) {
    background: $bg-card;
  }

  :deep(.el-table__inner-wrapper::before) {
    display: none;
  }
}
</style>
