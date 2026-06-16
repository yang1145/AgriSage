<template>
  <div class="plot-images-page">
    <!-- Header -->
    <div class="page-header">
      <div class="page-header__left">
        <h1 class="page-title">地块影像</h1>
        <span v-if="plotName" class="page-subtitle">{{ plotName }}</span>
      </div>
      <HudButton type="cyan" @click="showUploadDialog = true">上传图片</HudButton>
    </div>

    <!-- Loading -->
    <div v-if="loading" class="page-loading">
      <el-icon class="is-loading" :size="32"><Loading /></el-icon>
      <span>正在加载影像数据...</span>
    </div>

    <!-- Content -->
    <template v-else>
      <!-- Filters -->
      <div class="image-filters">
        <div class="stage-tabs">
          <button
            v-for="tab in stageTabs"
            :key="tab.value"
            class="stage-tab"
            :class="{ 'stage-tab--active': activeStage === tab.value }"
            @click="activeStage = tab.value"
          >
            {{ tab.label }}
            <span v-if="tab.count > 0" class="stage-tab__count">{{ tab.count }}</span>
          </button>
        </div>
        <div class="date-filters">
          <el-date-picker
            v-model="dateRange"
            type="daterange"
            range-separator="至"
            start-placeholder="开始日期"
            end-placeholder="结束日期"
            size="small"
            class="hud-date-picker"
            value-format="YYYY-MM-DD"
            @change="onDateChange"
          />
        </div>
      </div>

      <!-- Empty -->
      <div v-if="filteredImages.length === 0" class="page-empty">
        <el-icon :size="48"><Picture /></el-icon>
        <span>暂无影像记录</span>
      </div>

      <!-- Image Grid -->
      <div v-else class="image-grid">
        <div
          v-for="img in filteredImages"
          :key="img.id"
          class="image-card"
          @click="previewImage(img)"
        >
          <div class="image-card__wrapper">
            <img :src="getImageUrl(img.file_path)" :alt="formatDate(img.taken_at)" />
            <div class="image-card__overlay">
              <el-icon :size="24"><ZoomIn /></el-icon>
            </div>
            <div v-if="img.annotations && img.annotations.length" class="image-card__badge">
              <el-icon :size="12"><CircleCheck /></el-icon>
              {{ img.annotations.length }}
            </div>
          </div>
          <div class="image-card__info">
            <span class="image-card__date">{{ formatDate(img.taken_at) }}</span>
            <span class="image-card__stage">{{ stageLabel(img.growth_stage) }}</span>
          </div>
        </div>
      </div>
    </template>

    <!-- Preview Dialog with Annotation -->
    <el-dialog
      v-model="showPreview"
      :show-close="true"
      width="auto"
      class="hud-dialog hud-dialog--preview"
      append-to-body
      @close="closePreview"
    >
      <div v-if="previewingImage" class="preview-container">
        <div ref="previewImageRef" class="preview-image-wrapper" @click="onImageClick">
          <img
            :src="getImageUrl(previewingImage.file_path)"
            :alt="formatDate(previewingImage.taken_at)"
            class="preview-image"
            @load="onPreviewLoad"
          />
          <!-- Annotation dots -->
          <div
            v-for="(anno, idx) in previewAnnotations"
            :key="idx"
            class="annotation-dot"
            :style="{ left: anno.x + '%', top: anno.y + '%' }"
            :title="anno.label"
            @click.stop="removeAnnotation(idx)"
          >
            <span class="annotation-dot__label">{{ anno.label }}</span>
          </div>
        </div>
        <div class="preview-toolbar">
          <div class="preview-info">
            <span>{{ formatDate(previewingImage.taken_at) }}</span>
            <span>{{ stageLabel(previewingImage.growth_stage) }}</span>
            <span v-if="previewAnnotations.length">标注: {{ previewAnnotations.length }}</span>
            <span v-if="previewingImage.gps_lat && previewingImage.gps_lon">
              GPS: {{ previewingImage.gps_lat.toFixed(5) }}, {{ previewingImage.gps_lon.toFixed(5) }}
            </span>
          </div>
          <div class="preview-actions">
            <el-select v-model="newAnnotationLabel" placeholder="标注类型" size="small" style="width: 120px;">
              <el-option label="黄叶" value="黄叶" />
              <el-option label="倒伏" value="倒伏" />
              <el-option label="病斑" value="病斑" />
              <el-option label="虫害" value="虫害" />
              <el-option label="其他" value="其他" />
            </el-select>
            <el-button size="small" type="primary" @click="saveAnnotations">保存标注</el-button>
            <el-button size="small" type="danger" @click="handleDeleteImage">删除图片</el-button>
          </div>
        </div>
        <div class="preview-hint">点击图片添加标注，点击标注点删除</div>
      </div>
    </el-dialog>

    <!-- Upload Dialog -->
    <el-dialog
      v-model="showUploadDialog"
      title="上传图片"
      width="480px"
      class="hud-dialog"
      :close-on-click-modal="false"
    >
      <el-form label-position="top" class="hud-form">
        <el-form-item label="生长阶段">
          <el-select v-model="uploadStage" placeholder="请选择生长阶段" class="hud-select--full">
            <el-option label="萌芽" value="萌芽" />
            <el-option label="分蘖" value="分蘖" />
            <el-option label="伸长期" value="伸长期" />
            <el-option label="成熟期" value="成熟期" />
            <el-option label="收获" value="收获" />
          </el-select>
        </el-form-item>
        <el-form-item label="选择图片">
          <el-upload
            ref="uploadRef"
            :auto-upload="false"
            :limit="5"
            accept="image/*"
            :on-change="handleUploadChange"
            :file-list="uploadFiles"
            list-type="picture-card"
            class="hud-upload"
            multiple
          >
            <el-icon :size="20"><Plus /></el-icon>
          </el-upload>
        </el-form-item>
      </el-form>
      <template #footer>
        <HudButton type="ghost" @click="showUploadDialog = false">取消</HudButton>
        <HudButton type="cyan" :disabled="uploading" @click="handleUpload">
          {{ uploading ? '上传中...' : '确认上传' }}
        </HudButton>
      </template>
    </el-dialog>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { useRoute } from 'vue-router'
import { Loading, Picture, ZoomIn, Plus, CircleCheck } from '@element-plus/icons-vue'
import { ElMessage, ElMessageBox } from 'element-plus'
import { plotApi } from '@/api/plot'
import { imageApi } from '@/api/image'
import HudButton from '@/components/hud/HudButton.vue'

const route = useRoute()
const plotId = computed(() => route.params.plotId)

const images = ref([])
const loading = ref(false)
const plotName = ref('')
const activeStage = ref('all')
const dateRange = ref(null)
const showPreview = ref(false)
const previewingImage = ref(null)
const previewAnnotations = ref([])
const previewImageRef = ref(null)
const newAnnotationLabel = ref('病斑')
const showUploadDialog = ref(false)
const uploading = ref(false)
const uploadStage = ref('')
const uploadFiles = ref([])
const uploadRef = ref(null)

const stageLabels = {
  '萌芽': '萌芽期',
  '分蘖': '分蘖期',
  '伸长期': '伸长期',
  '成熟期': '成熟期',
  '收获': '收获期',
}

const stageLabel = (stage) => stageLabels[stage] || stage || '--'

const formatDate = (iso) => {
  if (!iso) return '--'
  const d = new Date(iso)
  return `${d.getFullYear()}-${String(d.getMonth() + 1).padStart(2, '0')}-${String(d.getDate()).padStart(2, '0')}`
}

const getImageUrl = (filePath) => {
  if (!filePath) return ''
  if (filePath.startsWith('http')) return filePath
  return `/api/uploads/${filePath}`
}

const stageTabs = computed(() => {
  const tabs = [{ label: '全部', value: 'all', count: images.value.length }]
  const stageOrder = ['萌芽', '分蘖', '伸长期', '成熟期', '收获']
  stageOrder.forEach((stage) => {
    const count = images.value.filter((img) => img.growth_stage === stage).length
    tabs.push({ label: stageLabels[stage], value: stage, count })
  })
  return tabs
})

const filteredImages = computed(() => {
  let result = images.value
  if (activeStage.value !== 'all') {
    result = result.filter((img) => img.growth_stage === activeStage.value)
  }
  if (dateRange.value && dateRange.value.length === 2) {
    const start = new Date(dateRange.value[0]).getTime()
    const end = new Date(dateRange.value[1]).getTime() + 24 * 60 * 60 * 1000
    result = result.filter((img) => {
      if (!img.taken_at) return false
      const t = new Date(img.taken_at).getTime()
      return t >= start && t < end
    })
  }
  return result
})

const onDateChange = () => {
  // dateRange changed, computed will recalculate
}

const fetchPlotImages = async () => {
  loading.value = true
  try {
    const plotRes = await plotApi.getPlot(plotId.value)
    plotName.value = plotRes.data?.plot?.name || ''

    const imgRes = await imageApi.getPlotImages(plotId.value)
    const grouped = imgRes.data?.images || {}
    const flat = []
    for (const items of Object.values(grouped)) {
      if (Array.isArray(items)) flat.push(...items)
    }
    images.value = flat
  } catch {
    ElMessage.error('获取影像数据失败')
  } finally {
    loading.value = false
  }
}

const previewImage = (img) => {
  previewingImage.value = img
  previewAnnotations.value = img.annotations ? [...img.annotations] : []
  showPreview.value = true
}

const closePreview = () => {
  previewingImage.value = null
  previewAnnotations.value = []
}

const onPreviewLoad = () => {
  // image loaded
}

const onImageClick = (e) => {
  if (!previewImageRef.value) return
  const rect = previewImageRef.value.getBoundingClientRect()
  const x = ((e.clientX - rect.left) / rect.width) * 100
  const y = ((e.clientY - rect.top) / rect.height) * 100
  previewAnnotations.value.push({
    x: Math.max(0, Math.min(100, x)),
    y: Math.max(0, Math.min(100, y)),
    label: newAnnotationLabel.value || '其他',
  })
}

const removeAnnotation = (idx) => {
  previewAnnotations.value.splice(idx, 1)
}

const saveAnnotations = async () => {
  if (!previewingImage.value) return
  try {
    await imageApi.updateImage(previewingImage.value.id, {
      annotations: previewAnnotations.value,
    })
    previewingImage.value.annotations = [...previewAnnotations.value]
    ElMessage.success('标注保存成功')
  } catch {
    ElMessage.error('标注保存失败')
  }
}

const handleDeleteImage = async () => {
  if (!previewingImage.value) return
  try {
    await ElMessageBox.confirm('确定删除这张图片吗？', '删除确认', {
      confirmButtonText: '删除',
      cancelButtonText: '取消',
      type: 'warning',
    })
    await imageApi.deleteImage(previewingImage.value.id)
    ElMessage.success('图片已删除')
    showPreview.value = false
    await fetchPlotImages()
  } catch {
    // cancelled
  }
}

const handleUploadChange = (file, fileList) => {
  uploadFiles.value = fileList
}

const handleUpload = async () => {
  if (uploadFiles.value.length === 0) {
    ElMessage.warning('请选择要上传的图片')
    return
  }
  uploading.value = true
  try {
    const formData = new FormData()
    uploadFiles.value.forEach((file) => {
      formData.append('files', file.raw)
    })
    if (uploadStage.value) {
      formData.append('growth_stage', uploadStage.value)
    }
    await imageApi.uploadImages(plotId.value, formData)
    ElMessage.success('图片上传成功')
    showUploadDialog.value = false
    uploadFiles.value = []
    uploadStage.value = ''
    await fetchPlotImages()
  } catch {
    ElMessage.error('图片上传失败')
  } finally {
    uploading.value = false
  }
}

onMounted(fetchPlotImages)
</script>

<style lang="scss" scoped>
@use '@/styles/variables' as *;

.plot-images-page {
  min-height: 100%;
}

.page-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  margin-bottom: $spacing-lg;
  flex-wrap: wrap;
  gap: $spacing-md;

  &__left {
    display: flex;
    align-items: baseline;
    gap: $spacing-md;
  }
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

.page-subtitle {
  font-family: $font-mono;
  font-size: $font-size-base;
  color: $text-secondary;
  letter-spacing: 1px;
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

// Filters
.image-filters {
  display: flex;
  align-items: center;
  justify-content: space-between;
  flex-wrap: wrap;
  gap: $spacing-sm;
  margin-bottom: $spacing-lg;
  border-bottom: 1px solid $border-color;
}

.stage-tabs {
  display: flex;
  gap: 2px;
  overflow-x: auto;
}

.date-filters {
  display: flex;
  align-items: center;
  padding-bottom: $spacing-xs;
}

.stage-tab {
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
  white-space: nowrap;
  display: flex;
  align-items: center;
  gap: $spacing-xs;

  &:hover {
    color: $text-primary;
  }

  &--active {
    color: $accent-cyan;
    border-bottom-color: $accent-cyan;
  }

  &__count {
    font-size: $font-size-xs;
    color: $text-muted;
    background: rgba(0, 240, 255, 0.08);
    padding: 0 5px;
    border-radius: $radius-sm;
  }
}

// Image Grid
.image-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(180px, 1fr));
  gap: $spacing-md;
}

.image-card {
  cursor: pointer;
  transition: transform $transition-fast;

  &:hover {
    transform: translateY(-2px);

    .image-card__overlay {
      opacity: 1;
    }
  }
}

.image-card__wrapper {
  position: relative;
  width: 100%;
  padding-top: 75%;
  overflow: hidden;
  border: 1px solid $border-color;
  border-radius: $radius-md;
  background: $bg-card;

  img {
    position: absolute;
    top: 0;
    left: 0;
    width: 100%;
    height: 100%;
    object-fit: cover;
  }
}

.image-card__overlay {
  position: absolute;
  inset: 0;
  display: flex;
  align-items: center;
  justify-content: center;
  background: rgba(10, 15, 20, 0.6);
  color: $accent-cyan;
  opacity: 0;
  transition: opacity $transition-fast;
  z-index: 2;
}

.image-card__badge {
  position: absolute;
  top: 6px;
  right: 6px;
  display: flex;
  align-items: center;
  gap: 2px;
  font-family: $font-mono;
  font-size: 10px;
  color: $accent-green;
  background: rgba(10, 15, 20, 0.8);
  border: 1px solid rgba(57, 255, 20, 0.3);
  padding: 2px 6px;
  border-radius: $radius-sm;
  z-index: 3;
}

.image-card__info {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-top: $spacing-xs;
  padding: 0 2px;
}

.image-card__date {
  font-family: $font-mono;
  font-size: $font-size-xs;
  color: $text-muted;
}

.image-card__stage {
  font-family: $font-mono;
  font-size: 10px;
  color: $accent-cyan;
  border: 1px solid rgba(0, 240, 255, 0.2);
  background: rgba(0, 240, 255, 0.06);
  padding: 1px 5px;
  border-radius: $radius-sm;
}

// Preview
.preview-container {
  display: flex;
  flex-direction: column;
  gap: $spacing-sm;
}

.preview-image-wrapper {
  position: relative;
  display: inline-block;
  cursor: crosshair;
}

.preview-image {
  max-width: 80vw;
  max-height: 60vh;
  object-fit: contain;
  border-radius: $radius-md;
}

.annotation-dot {
  position: absolute;
  width: 16px;
  height: 16px;
  border-radius: 50%;
  background: $accent-orange;
  border: 2px solid #fff;
  transform: translate(-50%, -50%);
  cursor: pointer;
  z-index: 10;
  box-shadow: 0 0 6px rgba(255, 107, 53, 0.6);
  transition: transform $transition-fast;

  &:hover {
    transform: translate(-50%, -50%) scale(1.3);

    .annotation-dot__label {
      opacity: 1;
    }
  }

  &__label {
    position: absolute;
    top: -22px;
    left: 50%;
    transform: translateX(-50%);
    font-family: $font-mono;
    font-size: 10px;
    color: #fff;
    background: rgba(255, 107, 53, 0.9);
    padding: 1px 6px;
    border-radius: 3px;
    white-space: nowrap;
    opacity: 0;
    transition: opacity $transition-fast;
    pointer-events: none;
  }
}

.preview-toolbar {
  display: flex;
  justify-content: space-between;
  align-items: center;
  flex-wrap: wrap;
  gap: $spacing-sm;
  padding: $spacing-sm $spacing-md;
  background: $bg-card;
  border: 1px solid $border-color;
  border-radius: $radius-sm;
}

.preview-info {
  display: flex;
  gap: $spacing-md;
  font-family: $font-mono;
  font-size: $font-size-xs;
  color: $text-secondary;
}

.preview-actions {
  display: flex;
  gap: $spacing-sm;
  align-items: center;
}

.preview-hint {
  font-family: $font-mono;
  font-size: 10px;
  color: $text-muted;
  text-align: center;
  letter-spacing: 1px;
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

  &--preview {
    :deep(.el-dialog__header) {
      display: none;
    }

    :deep(.el-dialog__body) {
      padding: $spacing-md;
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

.hud-date-picker {
  :deep(.el-input__wrapper) {
    background: $bg-card;
    border: 1px solid $border-color;
    box-shadow: none;
  }

  :deep(.el-input__inner) {
    color: $text-primary;
    font-family: $font-mono;
    font-size: $font-size-sm;
  }

  :deep(.el-range-separator) {
    color: $text-muted;
  }
}

.hud-upload {
  :deep(.el-upload--picture-card) {
    background: $bg-card;
    border: 1px dashed $border-color;
    border-radius: $radius-sm;
    color: $text-muted;
    transition: border-color $transition-fast;

    &:hover {
      border-color: rgba(0, 240, 255, 0.4);
      color: $accent-cyan;
    }
  }

  :deep(.el-upload-list__item) {
    background: $bg-card;
    border-color: $border-color;
  }
}
</style>
