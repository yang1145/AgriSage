import request from './index'

export const imageApi = {
  getPlotImages(plotId) {
    return request.get(`/images/plot/${plotId}`)
  },

  uploadImages(plotId, formData) {
    return request.post(`/images/plot/${plotId}`, formData, {
      headers: { 'Content-Type': 'multipart/form-data' },
    })
  },

  updateImage(imageId, data) {
    return request.put(`/images/${imageId}`, data)
  },

  deleteImage(imageId) {
    return request.delete(`/images/${imageId}`)
  },
}
