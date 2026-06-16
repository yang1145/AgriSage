<template>
  <div ref="mapContainer" class="plot-map" />
</template>

<script setup>
import { ref, onMounted, onUnmounted, watch } from 'vue'
import L from 'leaflet'
import 'leaflet/dist/leaflet.css'

const props = defineProps({
  plots: {
    type: Array,
    default: () => [],
  },
  center: {
    type: Array,
    default: () => [22.8, 108.3],
  },
  zoom: {
    type: Number,
    default: 9,
  },
})

const emit = defineEmits(['select'])

const mapContainer = ref(null)
let map = null
let polygonLayers = []

const statusColors = {
  idle: { color: '#4a5568', fillColor: 'rgba(74, 85, 104, 0.15)' },
  growing: { color: '#39ff14', fillColor: 'rgba(57, 255, 20, 0.12)' },
  harvested: { color: '#ff6b35', fillColor: 'rgba(255, 107, 53, 0.12)' },
}

const createPolygon = (plot) => {
  if (!plot.boundary_geojson) return null

  const geojson = typeof plot.boundary_geojson === 'string'
    ? JSON.parse(plot.boundary_geojson)
    : plot.boundary_geojson

  const status = plot.status || 'idle'
  const colors = statusColors[status] || statusColors.idle

  const polygon = L.geoJSON(geojson, {
    style: {
      color: colors.color,
      weight: 2,
      opacity: 0.9,
      fillColor: colors.fillColor,
      fillOpacity: 0.6,
      dashArray: status === 'idle' ? '4 4' : null,
    },
    onEachFeature: (feature, layer) => {
      layer.on({
        click: () => {
          emit('select', plot.id)
        },
        mouseover: (e) => {
          const l = e.target
          l.setStyle({
            weight: 3,
            opacity: 1,
            fillOpacity: 0.8,
          })
        },
        mouseout: (e) => {
          const l = e.target
          l.setStyle({
            weight: 2,
            opacity: 0.9,
            fillOpacity: 0.6,
          })
        },
      })

      // Tooltip
      if (plot.name) {
        layer.bindTooltip(plot.name, {
          className: 'plot-map-tooltip',
          direction: 'top',
          offset: [0, -10],
        })
      }
    },
  })

  return polygon
}

const renderPlots = () => {
  // Clear existing polygons
  polygonLayers.forEach((layer) => layer.remove())
  polygonLayers = []

  if (!map) return

  props.plots.forEach((plot) => {
    const polygon = createPolygon(plot)
    if (polygon) {
      polygon.addTo(map)
      polygonLayers.push(polygon)
    }
  })
}

onMounted(() => {
  if (!mapContainer.value) return

  map = L.map(mapContainer.value, {
    center: props.center,
    zoom: props.zoom,
    zoomControl: false,
    attributionControl: false,
  })

  // 瓦片源：高德卫星图（国内CDN速度快）+ 离线兜底
  const onlineUrl = 'https://webst0{s}.is.autonavi.com/appmaptile?style=6&x={x}&y={y}&z={z}'
  const localUrl = '/tiles/{z}/{x}/{y}.png'

  let currentLayer = L.tileLayer(onlineUrl, {
    maxZoom: 18,
    subdomains: '1234',
    attributionControl: false,
  })

  // 检测在线瓦片是否可用（首个瓦片失败则切换离线）
  let switchedToLocal = false
  currentLayer.on('tileerror', () => {
    if (!switchedToLocal) {
      switchedToLocal = true
      map.removeLayer(currentLayer)
      currentLayer = L.tileLayer(localUrl, { maxZoom: 18 })
      currentLayer.addTo(map)
    }
  })

  currentLayer.addTo(map)

  // Custom zoom control position
  L.control.zoom({ position: 'bottomright' }).addTo(map)

  renderPlots()
})

onUnmounted(() => {
  if (map) {
    map.remove()
    map = null
  }
})

watch(() => props.plots, renderPlots, { deep: true })
</script>

<style lang="scss" scoped>
@use '@/styles/variables' as *;

.plot-map {
  width: 100%;
  height: 100%;
  min-height: 400px;
  border: 1px solid $border-color;
  border-radius: $radius-md;
  overflow: hidden;
}
</style>

<style lang="scss">
// Global tooltip style (not scoped)
.plot-map-tooltip {
  background: #0d1117 !important;
  border: 1px solid #1a2332 !important;
  color: #00f0ff !important;
  font-family: 'Roboto Mono', monospace !important;
  font-size: 12px !important;
  padding: 4px 8px !important;
  border-radius: 2px !important;
  box-shadow: 0 0 8px rgba(0, 240, 255, 0.2) !important;

  &::before {
    border-top-color: #1a2332 !important;
  }
}
</style>
