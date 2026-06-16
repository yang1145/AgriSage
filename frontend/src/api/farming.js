import request from './index'

export const farmingApi = {
  getRecords(cycleId) {
    return request.get(`/farming/cycle/${cycleId}`)
  },

  createFertilization(cycleId, data) {
    return request.post(`/farming/cycle/${cycleId}/fertilization`, data)
  },

  createIrrigation(cycleId, data) {
    return request.post(`/farming/cycle/${cycleId}/irrigation`, data)
  },

  createPestDisease(cycleId, data) {
    return request.post(`/farming/cycle/${cycleId}/pest-disease`, data)
  },

  createHarvest(cycleId, data) {
    return request.post(`/farming/cycle/${cycleId}/harvest`, data)
  },

  updateRecord(type, id, data) {
    return request.put(`/farming/${type}/${id}`, data)
  },

  deleteRecord(type, id) {
    return request.delete(`/farming/${type}/${id}`)
  },
}
