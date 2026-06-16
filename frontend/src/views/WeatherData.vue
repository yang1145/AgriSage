<template>
  <div class="weather-page">
    <!-- Header -->
    <div class="page-header">
      <h1 class="page-title">气象数据</h1>
      <div class="page-controls">
        <el-select
          v-model="selectedStation"
          filterable
          remote
          reserve-keyword
          placeholder="搜索城市/监测站"
          :remote-method="searchStations"
          :loading="searchLoading"
          class="hud-select"
          @change="onStationChange"
        >
          <el-option
            v-for="s in searchResults"
            :key="s.id"
            :label="`${s.name_cn} (${s.name_en})`"
            :value="s.id"
          />
          <el-option label="默认（三水）" value="59279" />
        </el-select>
        <el-button
          type="primary"
          class="hud-btn"
          :loading="loading"
          @click="loadWeather"
        >
          刷新数据
        </el-button>
      </div>
    </div>

    <!-- Loading -->
    <div v-if="loading && !currentData" class="page-loading">
      <el-icon class="is-loading" :size="32"><Loading /></el-icon>
      <span>正在获取天气数据...</span>
    </div>

    <!-- Error -->
    <div v-else-if="error" class="page-error">
      <el-icon :size="48"><Warning /></el-icon>
      <span>{{ error }}</span>
      <el-button type="primary" @click="loadWeather">重试</el-button>
    </div>

    <!-- Content -->
    <template v-else-if="currentData || forecastData">
      <!-- 实时天气 -->
      <HudPanel v-if="currentData?.now" title="CURRENT WEATHER / 当前气象">
        <div class="weather-now">
          <div class="weather-main">
            <div class="location-info">
              <span class="city-name">{{ currentData.location?.name }}</span>
              <span class="location-path">{{ currentData.location?.path }}</span>
              <span class="update-time">{{ currentData.lastUpdate }} 更新</span>
            </div>
            <div class="temp-display">
              <span class="temp-value">{{ currentData.now.temperature }}</span>
              <span class="temp-unit">°C</span>
            </div>
            <div class="feels-like">体感 {{ currentData.now.feelst }}°C</div>
          </div>

          <div class="weather-grid">
            <div class="weather-item">
              <span class="item-label">湿度 HUMIDITY</span>
              <span class="item-value">{{ currentData.now.humidity }}%</span>
            </div>
            <div class="weather-item">
              <span class="item-label">气压 PRESSURE</span>
              <span class="item-value">{{ currentData.now.pressure }} hPa</span>
            </div>
            <div class="weather-item">
              <span class="item-label">风向 WIND DIR</span>
              <span class="item-value">{{ currentData.now.windDirection }}</span>
            </div>
            <div class="weather-item">
              <span class="item-label">风速 WIND SPEED</span>
              <span class="item-value">{{ currentData.now.windSpeed }} m/s ({{ currentData.now.windScale }})</span>
            </div>
            <div class="weather-item">
              <span class="item-label">降雨 PRECIPITATION</span>
              <span class="item-value">{{ currentData.now.precipitation }} mm</span>
            </div>
            <div class="weather-item">
              <span class="item-label">风向角 DEGREE</span>
              <span class="item-value">{{ currentData.now.windDirectionDegree }}°</span>
            </div>
          </div>
        </div>
      </HudPanel>

      <!-- 未来天气预报 -->
      <HudPanel v-if="forecastData?.daily" title="FORECAST / 未来预报">
        <div class="forecast-list">
          <div v-for="day in forecastData.daily" :key="day.date" class="forecast-card">
            <div class="forecast-date">{{ day.date }}</div>
            <div class="forecast-temps">
              <span class="temp-high">{{ day.high }}°</span>
              <span class="temp-low">{{ day.low }}°</span>
            </div>
            <div class="forecast-text">
              <span class="day-text">{{ day.dayText }}</span>
              <span class="night-text">{{ day.nightText }}</span>
            </div>
            <div class="forecast-wind">
              <span>{{ day.dayWindDirection }} {{ day.dayWindScale }}</span>
            </div>
          </div>
        </div>
      </HudPanel>

      <!-- 气象预警 -->
      <HudPanel v-if="alarms.length > 0" title="ALARM / 气象预警" class="alarm-panel">
        <div class="alarm-list">
          <div v-for="(alarm, index) in alarms" :key="index" class="alarm-card">
            <div class="alarm-header">
              <span class="alarm-title">{{ alarm.title }}</span>
              <span class="alarm-time">{{ alarm.effective }}</span>
            </div>
            <p class="alarm-desc">{{ alarm.description }}</p>
          </div>
        </div>
      </HudPanel>
    </template>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { Loading, Warning } from '@element-plus/icons-vue'
import { ElMessage } from 'element-plus'
import { dictionaryApi } from '@/api/dictionary'
import HudPanel from '@/components/hud/HudPanel.vue'

const selectedStation = ref('59279')
const loading = ref(false)
const error = ref('')
const searchLoading = ref(false)
const searchResults = ref([])

const currentData = ref(null)
const forecastData = ref(null)
const alarms = ref([])

// 搜索监测站
const searchStations = async (query) => {
  if (!query) {
    searchResults.value = []
    return
  }
  searchLoading.value = true
  try {
    const res = await dictionaryApi.searchWeatherStations(query)
    searchResults.value = res.data.stations || []
  } catch {
    // 静默失败
  } finally {
    searchLoading.value = false
  }
}

// 切换监测站
const onStationChange = () => {
  loadWeather()
}

// 加载天气数据
const loadWeather = async () => {
  if (!selectedStation.value) return

  loading.value = true
  error.value = ''

  try {
    const [currRes, foreRes, alarmRes] = await Promise.allSettled([
      dictionaryApi.getCurrentWeather(selectedStation.value),
      dictionaryApi.getWeatherForecast(selectedStation.value),
      dictionaryApi.getWeatherAlarm('44'), // 广东
    ])

    if (currRes.status === 'fulfilled') {
      currentData.value = currRes.value.data.data
    }
    if (foreRes.status === 'fulfilled') {
      forecastData.value = foreRes.value.data.data
    }
    if (alarmRes.status === 'fulfilled') {
      alarms.value = alarmRes.value.data.alarms || []
    }

    if (currRes.status === 'rejected' && foreRes.status === 'rejected') {
      error.value = '无法获取天气数据，请检查网络连接或稍后重试'
    }
  } catch {
    error.value = '获取天气数据时发生错误'
  } finally {
    loading.value = false
  }
}

onMounted(() => {
  loadWeather()
})
</script>

<style lang="scss" scoped>
@use '@/styles/variables' as *;

.weather-page {
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

.page-controls {
  display: flex;
  align-items: center;
  gap: $spacing-md;
}

.hud-select {
  width: 260px;

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
  }

  :deep(.el-select__caret) {
    color: $accent-cyan;
  }
}

.hud-btn {
  font-family: $font-mono;
  letter-spacing: 1px;
}

.page-loading,
.page-error {
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

.alarm-panel {
  border-color: rgba(255, 107, 53, 0.4);
  box-shadow: 0 0 16px rgba(255, 107, 53, 0.08);
}

/* 实时天气 */
.weather-now {
  display: flex;
  flex-direction: column;
  gap: $spacing-xl;
}

.weather-main {
  display: flex;
  align-items: center;
  gap: $spacing-xl;
  padding-bottom: $spacing-lg;
  border-bottom: 1px solid $border-color;

  .location-info {
    display: flex;
    flex-direction: column;
    gap: 4px;

    .city-name {
      font-size: $font-size-xl;
      font-weight: 700;
      color: $text-primary;
      font-family: $font-mono;
    }

    .location-path {
      font-size: $font-size-xs;
      color: $text-muted;
      font-family: $font-mono;
    }

    .update-time {
      font-size: $font-size-xs;
      color: $text-muted;
      opacity: 0.6;
    }
  }

  .temp-display {
    .temp-value {
      font-size: 56px;
      font-weight: 700;
      color: $accent-orange;
      font-family: $font-mono;
      line-height: 1;
      text-shadow: 0 0 20px rgba(255, 107, 53, 0.3);
    }

    .temp-unit {
      font-size: $font-size-lg;
      color: $text-muted;
      margin-left: 4px;
    }
  }

  .feels-like {
    font-size: $font-size-sm;
    color: $text-muted;
    font-family: $font-mono;
  }
}

.weather-grid {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: $spacing-md;

  @media (max-width: 768px) {
    grid-template-columns: repeat(2, 1fr);
  }

  @media (max-width: 480px) {
    grid-template-columns: 1fr;
  }
}

.weather-item {
  display: flex;
  flex-direction: column;
  gap: 6px;
  padding: $spacing-md;
  background: rgba(10, 15, 20, 0.5);
  border: 1px solid $border-color;
  border-radius: $radius-sm;

  .item-label {
    font-size: $font-size-xs;
    color: $text-muted;
    font-family: $font-mono;
    letter-spacing: 1px;
  }

  .item-value {
    font-size: $font-size-lg;
    font-weight: 600;
    color: $accent-cyan;
    font-family: $font-mono;
  }
}

/* 天气预报 */
.forecast-list {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(160px, 1fr));
  gap: $spacing-md;
}

.forecast-card {
  display: flex;
  flex-direction: column;
  gap: 8px;
  padding: $spacing-md;
  background: rgba(10, 15, 20, 0.5);
  border: 1px solid $border-color;
  border-radius: $radius-sm;
  transition: border-color 0.2s ease;

  &:hover {
    border-color: rgba(0, 240, 255, 0.3);
  }

  .forecast-date {
    font-size: $font-size-sm;
    color: $text-muted;
    font-family: $font-mono;
  }

  .forecast-temps {
    display: flex;
    align-items: baseline;
    gap: $spacing-sm;

    .temp-high {
      font-size: $font-size-xl;
      font-weight: 700;
      color: $accent-orange;
      font-family: $font-mono;
    }

    .temp-low {
      font-size: $font-size-md;
      color: $accent-cyan;
      font-family: $font-mono;
    }
  }

  .forecast-text {
    display: flex;
    flex-direction: column;
    gap: 2px;
    font-size: $font-size-sm;
    color: $text-secondary;

    .day-text {
      color: $text-primary;
    }

    .night-text {
      color: $text-muted;
      font-size: $font-size-xs;
    }
  }

  .forecast-wind {
    font-size: $font-size-xs;
    color: $text-muted;
    font-family: $font-mono;
  }
}

/* 气象预警 */
.alarm-list {
  display: flex;
  flex-direction: column;
  gap: $spacing-md;
}

.alarm-card {
  padding: $spacing-md;
  background: rgba(40, 20, 10, 0.6);
  border: 1px solid rgba(255, 107, 53, 0.25);
  border-radius: $radius-sm;
  border-left: 3px solid $accent-orange;

  .alarm-header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    gap: $spacing-md;
    margin-bottom: $spacing-sm;
    flex-wrap: wrap;

    .alarm-title {
      font-size: $font-size-sm;
      font-weight: 600;
      color: $accent-orange;
      font-family: $font-mono;
    }

    .alarm-time {
      font-size: $font-size-xs;
      color: $text-muted;
      font-family: $font-mono;
    }
  }

  .alarm-desc {
    font-size: $font-size-sm;
    color: $text-secondary;
    line-height: 1.6;
    margin: 0;
  }
}
</style>
