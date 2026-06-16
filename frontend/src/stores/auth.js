import { defineStore } from 'pinia'
import { authApi } from '@/api/auth'

export const useAuthStore = defineStore('auth', {
  state: () => ({
    token: localStorage.getItem('token') || '',
    user: {
      id: null,
      name: '',
      role: '',
      phone: '',
    },
  }),

  getters: {
    isLoggedIn: (state) => !!state.token,
    userRole: (state) => state.user.role,
  },

  actions: {
    async login(username, password) {
      const res = await authApi.login(username, password)
      this.token = res.data.token
      localStorage.setItem('token', res.data.token)
      if (res.data.user) {
        this.user = res.data.user
        if (this.user.role) {
          localStorage.setItem('userRole', this.user.role)
        }
      }
      await this.fetchUser()
    },

    logout() {
      this.token = ''
      this.user = { id: null, name: '', role: '', phone: '' }
      localStorage.removeItem('token')
    },

    async fetchUser() {
      try {
        const res = await authApi.getMe()
        this.user = res.data.user
      } catch {
        this.logout()
      }
    },

    hasRole(role) {
      return this.user.role === role
    },

    async initAuth() {
      const token = localStorage.getItem('token')
      if (token) {
        this.token = token
        await this.fetchUser()
      }
    },
  },
})
