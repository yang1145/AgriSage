import request from './index'

export const dictionaryApi = {
  getVarieties(search) {
    return request.get('/dict/varieties', { params: { search } })
  },

  getVariety(id) {
    return request.get(`/dict/varieties/${id}`)
  },

  createVariety(data) {
    return request.post('/dict/varieties', data)
  },

  getSugarFactories(search) {
    return request.get('/dict/sugar-factories', { params: { search } })
  },

  getWeatherStations(region) {
    return request.get('/dict/weather-stations', { params: { region } })
  },

  getSoilTemplates(township) {
    return request.get('/dict/soil-templates', { params: { township } })
  },

  // 中国气象局天气接口
  getCurrentWeather(stationId) {
    return request.get('/dict/weather/current', { params: { station_id: stationId } })
  },

  getWeatherForecast(stationId) {
    return request.get('/dict/weather/forecast', { params: { station_id: stationId } })
  },

  searchWeatherStations(q) {
    return request.get('/dict/weather/search', { params: { q } })
  },

  getWeatherAlarm(adcode) {
    return request.get('/dict/weather/alarm', { params: { adcode } })
  },
}
