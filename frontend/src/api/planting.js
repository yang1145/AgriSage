import request from './index'

export const plantingApi = {
  getCycles(plotId) {
    return request.get(`/cycles/plot/${plotId}`)
  },

  getCycle(id) {
    return request.get(`/cycles/${id}`)
  },

  createCycle(plotId, data) {
    return request.post(`/cycles/plot/${plotId}`, data)
  },

  updateCycle(id, data) {
    return request.put(`/cycles/${id}`, data)
  },

  getCycleTimeline(id) {
    return request.get(`/cycles/${id}/timeline`)
  },

  deleteCycle(id) {
    return request.delete(`/cycles/${id}`)
  },
}
