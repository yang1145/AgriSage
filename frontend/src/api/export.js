import request from './index'

export const exportApi = {
  exportExcel(plotIds) {
    return request.post('/export/excel', { plot_ids: plotIds }, { responseType: 'blob' })
  },

  exportPdf(plotId) {
    return request.post(`/export/pdf/${plotId}`, null, { responseType: 'blob' })
  },

  importExcel(file) {
    const formData = new FormData()
    formData.append('file', file)
    return request.post('/export/import-excel', formData, {
      headers: { 'Content-Type': 'multipart/form-data' },
    })
  },

  downloadBackup() {
    return request.get('/export/backup/download', { responseType: 'blob' })
  },

  restoreBackup(file) {
    const formData = new FormData()
    formData.append('file', file)
    return request.post('/export/backup/restore', formData, {
      headers: { 'Content-Type': 'multipart/form-data' },
    })
  },

  downloadTemplate() {
    return request.get('/export/template', { responseType: 'blob' })
  },
}

export const userApi = {
  getUsers() {
    return request.get('/users/')
  },

  createUser(data) {
    return request.post('/users/', data)
  },

  updateUser(id, data) {
    return request.put(`/users/${id}`, data)
  },

  deleteUser(id) {
    return request.delete(`/users/${id}`)
  },
}
