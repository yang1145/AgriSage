import request from './index'

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
