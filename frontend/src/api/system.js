import request from './index'

export const systemApi = {
  getStats() {
    return request.get('/system/stats')
  },

  reloadSeed() {
    return request.post('/system/seed')
  },
}
