import request from './index'

export const plotApi = {
  getPlots(params = {}) {
    return request.get('/plots/', { params })
  },

  getPlot(id) {
    return request.get(`/plots/${id}`)
  },

  createPlot(data) {
    return request.post('/plots/', data)
  },

  updatePlot(id, data) {
    return request.put(`/plots/${id}`, data)
  },

  deletePlot(id) {
    return request.delete(`/plots/${id}`)
  },

  getPlotStats() {
    return request.get('/plots/stats')
  },
}
