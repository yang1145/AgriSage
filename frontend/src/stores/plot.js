import { defineStore } from 'pinia'
import { plotApi } from '@/api/plot'

export const usePlotStore = defineStore('plot', {
  state: () => ({
    plots: [],
    currentPlot: null,
    stats: null,
  }),

  actions: {
    async fetchPlots(params = {}) {
      const res = await plotApi.getPlots(params)
      this.plots = res.data.plots || []
    },

    async fetchPlot(id) {
      const res = await plotApi.getPlot(id)
      this.currentPlot = res.data.plot
    },

    async createPlot(data) {
      const res = await plotApi.createPlot(data)
      return res.data.plot
    },

    async updatePlot(id, data) {
      const res = await plotApi.updatePlot(id, data)
      return res.data.plot
    },

    async deletePlot(id) {
      await plotApi.deletePlot(id)
      this.plots = this.plots.filter((p) => p.id !== id)
    },

    async fetchStats() {
      const res = await plotApi.getPlotStats()
      this.stats = res.data
    },
  },
})
