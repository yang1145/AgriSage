import request from './index'

export const authApi = {
  login(username, password) {
    return request.post('/auth/login', { username, password })
  },

  register(data) {
    return request.post('/auth/register', data)
  },

  getMe() {
    return request.get('/auth/me')
  },

  changePassword(oldPwd, newPwd) {
    return request.post('/auth/change-password', { old_password: oldPwd, new_password: newPwd })
  },
}
