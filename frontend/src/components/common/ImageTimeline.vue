<template>
  <div class="image-timeline">
    <div
      v-for="group in groupedImages"
      :key="group.stage"
      class="image-timeline__track"
    >
      <div class="image-timeline__track-label">
        <span class="image-timeline__track-dot" />
        {{ group.label }}
      </div>
      <div class="image-timeline__track-content">
        <div
          v-for="(img, index) in group.images"
          :key="index"
          class="image-timeline__card"
          @click="previewImage(img)"
        >
          <div class="image-timeline__card-image">
            <img :src="img.thumbnail || img.url" :alt="img.taken_at" />
            <div class="image-timeline__card-overlay">
              <el-icon :size="20"><ZoomIn /></el-icon>
            </div>
          </div>
          <div class="image-timeline__card-date">{{ img.taken_at }}</div>
        </div>
      </div>
    </div>

    <!-- Empty state -->
    <div v-if="!images || images.length === 0" class="image-timeline__empty">
      <el-icon :size="32"><Picture /></el-icon>
      <span>暂无图片记录</span>
    </div>

    <!-- Preview dialog -->
    <el-dialog
      v-model="showPreview"
      :show-close="true"
      width="auto"
      class="image-timeline__preview-dialog"
      append-to-body
    >
      <img
        v-if="previewingImage"
        :src="previewingImage.url"
        :alt="previewingImage.taken_at"
        class="image-timeline__preview-image"
      />
      <div v-if="previewingImage" class="image-timeline__preview-info">
        <span>{{ previewingImage.taken_at }}</span>
        <span>{{ stageLabel(previewingImage.growth_stage) }}</span>
      </div>
    </el-dialog>
  </div>
</template>

<script setup>
import { ref, computed } from 'vue'

const props = defineProps({
  images: {
    type: Array,
    default: () => [],
  },
})

const stageLabels = {
  sprouting: '萌芽期',
  tillering: '分蘖期',
  jointing: '拔节期',
  elongation: '伸长期',
  maturity: '成熟期',
  harvest: '收获期',
}

const stageOrder = ['sprouting', 'tillering', 'jointing', 'elongation', 'maturity', 'harvest']

const stageLabel = (stage) => stageLabels[stage] || stage

const groupedImages = computed(() => {
  const groups = {}

  props.images.forEach((img) => {
    const stage = img.growth_stage || 'unknown'
    if (!groups[stage]) {
      groups[stage] = {
        stage,
        label: stageLabel(stage),
        images: [],
      }
    }
    groups[stage].images.push(img)
  })

  // Sort by stage order
  return stageOrder
    .filter((s) => groups[s])
    .map((s) => groups[s])
    .concat(
      Object.keys(groups)
        .filter((s) => !stageOrder.includes(s) && s !== 'unknown')
        .map((s) => groups[s])
    )
})

const showPreview = ref(false)
const previewingImage = ref(null)

const previewImage = (img) => {
  previewingImage.value = img
  showPreview.value = true
}
</script>

<style lang="scss" scoped>
@use '@/styles/variables' as *;

.image-timeline {
  display: flex;
  flex-direction: column;
  gap: $spacing-lg;

  &__track {
    display: flex;
    gap: $spacing-md;
  }

  &__track-label {
    display: flex;
    align-items: center;
    gap: $spacing-xs;
    width: 72px;
    flex-shrink: 0;
    font-family: $font-mono;
    font-size: $font-size-xs;
    color: $accent-cyan;
    text-transform: uppercase;
    letter-spacing: 1px;
    padding-top: $spacing-sm;
  }

  &__track-dot {
    display: inline-block;
    width: 6px;
    height: 6px;
    border-radius: 50%;
    background: $accent-cyan;
    box-shadow: 0 0 4px rgba(0, 240, 255, 0.5);
    flex-shrink: 0;
  }

  &__track-content {
    display: flex;
    gap: $spacing-sm;
    overflow-x: auto;
    padding-bottom: $spacing-sm;

    // Custom scrollbar
    &::-webkit-scrollbar {
      height: 4px;
    }

    &::-webkit-scrollbar-thumb {
      background: rgba(0, 240, 255, 0.2);
      border-radius: 2px;
    }

    &::-webkit-scrollbar-track {
      background: transparent;
    }
  }

  &__card {
    flex-shrink: 0;
    cursor: pointer;
    transition: transform $transition-fast;

    &:hover {
      transform: translateY(-2px);

      .image-timeline__card-overlay {
        opacity: 1;
      }
    }
  }

  &__card-image {
    position: relative;
    width: 120px;
    height: 90px;
    overflow: hidden;
    border: 1px solid $border-color;
    border-radius: $radius-sm;
    background: $bg-card;

    // Holographic card effect
    &::before {
      content: '';
      position: absolute;
      inset: 0;
      background: linear-gradient(
        135deg,
        rgba(0, 240, 255, 0.05) 0%,
        transparent 50%,
        rgba(57, 255, 20, 0.03) 100%
      );
      z-index: 1;
      pointer-events: none;
    }

    img {
      width: 100%;
      height: 100%;
      object-fit: cover;
    }
  }

  &__card-overlay {
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

  &__card-date {
    font-family: $font-mono;
    font-size: $font-size-xs;
    color: $text-muted;
    margin-top: $spacing-xs;
    text-align: center;
  }

  &__empty {
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    gap: $spacing-sm;
    padding: $spacing-2xl;
    color: $text-muted;
    font-size: $font-size-sm;
  }

  &__preview-image {
    max-width: 80vw;
    max-height: 70vh;
    object-fit: contain;
    border-radius: $radius-md;
  }

  &__preview-info {
    display: flex;
    justify-content: space-between;
    padding: $spacing-sm $spacing-md;
    font-family: $font-mono;
    font-size: $font-size-xs;
    color: $text-secondary;
  }
}
</style>
