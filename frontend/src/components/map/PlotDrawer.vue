<template>
  <div class="plot-drawer">
    <div ref="mapContainer" class="plot-drawer__map" />
    <div v-if="drawing" class="plot-drawer__area-info">
      <span class="plot-drawer__area-label">当前面积</span>
      <span class="plot-drawer__area-value">{{ formattedArea }} 亩</span>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted, onUnmounted } from 'vue'
import L from 'leaflet'
import 'leaflet-draw'
import 'leaflet-draw/dist/leaflet.draw.css'

const props = defineProps({
  center: {
    type: Array,
    default: () => [22.8, 108.3],
  },
  zoom: {
    type: Number,
    default: 13,
  },
})

const emit = defineEmits(['created'])

const mapContainer = ref(null)
const drawing = ref(false)
const currentArea = ref(0)
let map = null
let drawnItems = null
let drawControl = null

const formattedArea = computed(() => {
  // Convert sq meters to 亩 (1 亩 ≈ 666.67 sq meters)
  const mu = currentArea.value / 666.67
  return mu.toFixed(2)
})

const calculateArea = (latlngs) => {
  if (!latlngs || latlngs.length < 3) return 0
  return L.GeometryUtil.geodesicArea(latlngs)
}

onMounted(() => {
  if (!mapContainer.value) return

  map = L.map(mapContainer.value, {
    center: props.center,
    zoom: props.zoom,
    zoomControl: false,
    attributionControl: false,
  })

  // 优先使用在线瓦片，离线环境回退到本地瓦片
  const onlineTileUrl = 'https://{s}.basemaps.cartocdn.com/dark_all/{z}/{x}/{y}{r}.png'
  const localTileUrl = '/tiles/{z}/{x}/{y}.png'

  let switchedToLocal = false
  const tileLayer = L.tileLayer(onlineTileUrl, {
    maxZoom: 19,
    subdomains: 'abcd',
  })

  tileLayer.on('tileerror', () => {
    if (!switchedToLocal) {
      switchedToLocal = true
      map.removeLayer(tileLayer)
      L.tileLayer(localTileUrl, { maxZoom: 18 }).addTo(map)
    }
  })

  tileLayer.addTo(map)

  L.control.zoom({ position: 'bottomright' }).addTo(map)

  // Initialize draw layer
  drawnItems = new L.FeatureGroup()
  map.addLayer(drawnItems)

  // Draw control with polygon only
  drawControl = new L.Control.Draw({
    position: 'topright',
    draw: {
      polygon: {
        shapeOptions: {
          color: '#00f0ff',
          weight: 2,
          fillColor: 'rgba(0, 240, 255, 0.12)',
          fillOpacity: 0.6,
          dashArray: null,
        },
        allowIntersection: false,
        showArea: true,
      },
      polyline: false,
      circle: false,
      rectangle: false,
      marker: false,
      circlemarker: false,
    },
    edit: {
      featureGroup: drawnItems,
    },
  })

  map.addControl(drawControl)

  // Style the draw controls
  const drawBtn = mapContainer.value.querySelector('.leaflet-draw-draw-polygon')
  if (drawBtn) {
    drawBtn.title = '绘制地块边界'
  }

  // Event handlers
  map.on(L.Draw.Event.DRAWSTART, () => {
    drawing.value = true
    currentArea.value = 0
  })

  map.on(L.Draw.Event.DRAWVERTEX, (e) => {
    const layers = e.layers
    layers.eachLayer((layer) => {
      const latlngs = layer.getLatLngs()
      if (latlngs && latlngs[0] && latlngs[0].length >= 3) {
        currentArea.value = calculateArea(latlngs[0])
      }
    })
  })

  map.on(L.Draw.Event.CREATED, (e) => {
    const layer = e.layer
    drawnItems.addLayer(layer)

    // Get GeoJSON
    const geojson = layer.toGeoJSON()

    // Calculate area
    const latlngs = layer.getLatLngs()
    const area = latlngs && latlngs[0] ? calculateArea(latlngs[0]) : 0
    const areaMu = area / 666.67

    emit('created', {
      geojson,
      area: areaMu,
    })

    drawing.value = false
  })

  map.on(L.Draw.Event.DRAWSTOP, () => {
    drawing.value = false
  })
})

onUnmounted(() => {
  if (map) {
    map.remove()
    map = null
  }
})
</script>

<style lang="scss" scoped>
@use '@/styles/variables' as *;

.plot-drawer {
  position: relative;
  width: 100%;
  height: 100%;
  min-height: 400px;

  &__map {
    width: 100%;
    height: 100%;
    min-height: 400px;
    border: 1px solid $border-color;
    border-radius: $radius-md;
    overflow: hidden;
  }

  &__area-info {
    position: absolute;
    top: $spacing-md;
    left: $spacing-md;
    z-index: 1000;
    display: flex;
    flex-direction: column;
    gap: $spacing-xs;
    padding: $spacing-sm $spacing-md;
    background: rgba(13, 17, 23, 0.9);
    border: 1px solid rgba(0, 240, 255, 0.3);
    border-radius: $radius-sm;
    box-shadow: 0 0 12px rgba(0, 240, 255, 0.15);
  }

  &__area-label {
    font-family: $font-mono;
    font-size: $font-size-xs;
    color: $text-muted;
    text-transform: uppercase;
    letter-spacing: 1px;
  }

  &__area-value {
    font-family: $font-mono;
    font-size: $font-size-lg;
    font-weight: 700;
    color: $accent-cyan;
    text-shadow: 0 0 8px rgba(0, 240, 255, 0.4);
  }
}
</style>

<style lang="scss">
// Override Leaflet Draw styles for HUD theme
.leaflet-draw-toolbar a {
  background-color: #0d1117 !important;
  border-color: #1a2332 !important;
  color: #00f0ff !important;

  &:hover {
    background-color: #111820 !important;
    border-color: rgba(0, 240, 255, 0.4) !important;
  }
}

.leaflet-draw-actions {
  background: #0d1117 !important;
  border-color: #1a2332 !important;

  a {
    background: #0d1117 !important;
    color: #8b9bb4 !important;
    border-color: #1a2332 !important;

    &:hover {
      background: #111820 !important;
      color: #00f0ff !important;
    }
  }
}

.leaflet-draw-tooltip {
  background: #0d1117 !important;
  border: 1px solid #1a2332 !important;
  color: #00f0ff !important;
  font-family: 'Roboto Mono', monospace !important;
  font-size: 11px !important;
  border-radius: 2px !important;
}

.leaflet-draw-tooltip-subtext {
  color: #8b9bb4 !important;
}
</style>
