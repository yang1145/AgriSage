<template>
  <div class="image-uploader">
    <div class="image-uploader__zone" @click="triggerUpload">
      <el-icon :size="32" class="image-uploader__zone-icon"><Upload /></el-icon>
      <div class="image-uploader__zone-text">点击或拖拽上传图片</div>
      <div class="image-uploader__zone-hint">支持 JPG / PNG 格式</div>
    </div>

    <!-- Metadata form -->
    <div v-if="pendingImages.length" class="image-uploader__form">
      <div class="image-uploader__form-title">图片信息</div>

      <div v-for="(img, index) in pendingImages" :key="index" class="image-uploader__item">
        <div class="image-uploader__item-preview">
          <img :src="img.preview" alt="预览" />
          <el-icon class="image-uploader__item-remove" @click="removePending(index)"><Close /></el-icon>
        </div>
        <div class="image-uploader__item-fields">
          <el-select v-model="img.growthStage" placeholder="生长阶段" size="small">
            <el-option
              v-for="stage in growthStages"
              :key="stage.value"
              :label="stage.label"
              :value="stage.value"
            />
          </el-select>
          <el-date-picker
            v-model="img.takenAt"
            type="date"
            placeholder="拍摄日期"
            size="small"
            value-format="YYYY-MM-DD"
          />
        </div>
      </div>
    </div>

    <!-- Upload button -->
    <div v-if="pendingImages.length" class="image-uploader__actions">
      <button class="hud-button hud-button--cyan" @click="uploadAll">
        上传全部 ({{ pendingImages.length }})
      </button>
    </div>

    <input
      ref="fileInput"
      type="file"
      multiple
      accept="image/jpeg,image/png"
      style="display: none"
      @change="handleFileSelect"
    />
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { ElMessage } from 'element-plus'
import dayjs from 'dayjs'

const props = defineProps({
  plotId: {
    type: [Number, String],
    default: null,
  },
  cycleId: {
    type: [Number, String],
    default: null,
  },
  growthStages: {
    type: Array,
    default: () => [
      { label: '萌芽期', value: 'sprouting' },
      { label: '分蘖期', value: 'tillering' },
      { label: '拔节期', value: 'jointing' },
      { label: '伸长期', value: 'elongation' },
      { label: '成熟期', value: 'maturity' },
      { label: '收获期', value: 'harvest' },
    ],
  },
})

const emit = defineEmits(['uploaded'])

const fileInput = ref(null)
const pendingImages = ref([])

const triggerUpload = () => {
  fileInput.value?.click()
}

const handleFileSelect = (event) => {
  const files = event.target.files
  if (!files) return

  for (const file of files) {
    if (!file.type.startsWith('image/')) continue

    const reader = new FileReader()
    reader.onload = (e) => {
      pendingImages.value.push({
        file,
        preview: e.target.result,
        growthStage: '',
        takenAt: dayjs().format('YYYY-MM-DD'),
      })
    }
    reader.readAsDataURL(file)
  }

  // Reset input
  event.target.value = ''
}

const removePending = (index) => {
  pendingImages.value.splice(index, 1)
}

const uploadAll = async () => {
  // Validate
  const invalid = pendingImages.value.find((img) => !img.growthStage)
  if (invalid) {
    ElMessage.warning('请为每张图片选择生长阶段')
    return
  }

  // TODO: 实际上传逻辑，调用 API
  emit('uploaded', pendingImages.value.map((img) => ({
    plotId: props.plotId,
    cycleId: props.cycleId,
    file: img.file,
    growthStage: img.growthStage,
    takenAt: img.takenAt,
  })))

  ElMessage.success('图片上传成功')
  pendingImages.value = []
}
</script>

<style lang="scss" scoped>
@use '@/styles/variables' as *;

.image-uploader {
  &__zone {
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    gap: $spacing-sm;
    padding: $spacing-xl;
    border: 1px dashed $border-color;
    border-radius: $radius-md;
    background: rgba(0, 240, 255, 0.02);
    cursor: pointer;
    transition: all $transition-base;

    &:hover {
      border-color: rgba(0, 240, 255, 0.4);
      background: rgba(0, 240, 255, 0.05);
      box-shadow: 0 0 12px rgba(0, 240, 255, 0.1);
    }
  }

  &__zone-icon {
    color: $accent-cyan;
    opacity: 0.6;
  }

  &__zone-text {
    font-size: $font-size-sm;
    color: $text-secondary;
  }

  &__zone-hint {
    font-size: $font-size-xs;
    color: $text-muted;
  }

  &__form {
    margin-top: $spacing-md;
  }

  &__form-title {
    font-family: $font-mono;
    font-size: $font-size-xs;
    color: $accent-cyan;
    text-transform: uppercase;
    letter-spacing: 1px;
    margin-bottom: $spacing-sm;
  }

  &__item {
    display: flex;
    gap: $spacing-md;
    padding: $spacing-sm;
    margin-bottom: $spacing-sm;
    border: 1px solid $border-color;
    border-radius: $radius-sm;
    background: $bg-card;
  }

  &__item-preview {
    position: relative;
    width: 64px;
    height: 64px;
    flex-shrink: 0;

    img {
      width: 100%;
      height: 100%;
      object-fit: cover;
      border-radius: $radius-sm;
      border: 1px solid $border-color;
    }
  }

  &__item-remove {
    position: absolute;
    top: -6px;
    right: -6px;
    width: 18px;
    height: 18px;
    display: flex;
    align-items: center;
    justify-content: center;
    background: $bg-card;
    border: 1px solid $border-color;
    border-radius: 50%;
    color: $accent-orange;
    cursor: pointer;
    font-size: 10px;
  }

  &__item-fields {
    flex: 1;
    display: flex;
    flex-direction: column;
    gap: $spacing-xs;
  }

  &__actions {
    margin-top: $spacing-md;
    display: flex;
    justify-content: flex-end;
  }
}
</style>
