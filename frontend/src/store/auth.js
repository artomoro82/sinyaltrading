import { defineStore } from 'pinia'
import axios from 'axios'

export const useAuthStore = defineStore('auth', {
  state: () => ({
    user: null,
    token: localStorage.getItem('token') || null,
    loading: false,
    error: null
  }),
  
  getters: {
    isAuthenticated: (state) => !!state.token,
    userRole: (state) => state.user?.role || null,
    userName: (state) => state.user?.full_name || null
  },
  
  actions: {
    async login(credentials) {
      this.loading = true
      this.error = null
      
      try {
        const response = await axios.post('https://pyscalp.com/api/users/login/', credentials)
        
        this.token = response.data.access
        this.user = response.data.user
        
        localStorage.setItem('token', response.data.access)
        localStorage.setItem('refreshToken', response.data.refresh)
        
        // Set default Authorization header for all future requests
        axios.defaults.headers.common['Authorization'] = `Bearer ${response.data.access}`
        
        return response.data
      } catch (error) {
        this.error = error.response?.data?.error || 'Login failed'
        throw error
      } finally {
        this.loading = false
      }
    },
    
    async register(userData) {
      this.loading = true
      this.error = null
      
      try {
        const response = await axios.post('https://pyscalp.com/api/users/register/', userData)
        
        this.token = response.data.access
        this.user = response.data.user
        
        localStorage.setItem('token', response.data.access)
        localStorage.setItem('refreshToken', response.data.refresh)
        
        // Set default Authorization header for all future requests
        axios.defaults.headers.common['Authorization'] = `Bearer ${response.data.access}`
        
        return response.data
      } catch (error) {
        this.error = error.response?.data || 'Registration failed'
        throw error
      } finally {
        this.loading = false
      }
    },
    
    async requestPasswordReset(data) {
      this.loading = true
      this.error = null
      
      try {
        const response = await axios.post('https://pyscalp.com/api/users/forgot-password/', data)
        return response.data
      } catch (error) {
        this.error = error.response?.data?.error || 'Failed to process password reset request'
        throw error
      } finally {
        this.loading = false
      }
    },
    
    async fetchUserProfile() {
      if (!this.token) return null
      
      this.loading = true
      
      try {
        const response = await axios.get('https://pyscalp.com/api/users/profile/')
        this.user = response.data
        return response.data
      } catch (error) {
        if (error.response?.status === 401) {
          this.logout()
        }
        this.error = error.response?.data || 'Failed to fetch user profile'
        throw error
      } finally {
        this.loading = false
      }
    },
    
    async refreshToken() {
      const refreshToken = localStorage.getItem('refreshToken')
      if (!refreshToken) {
        this.logout()
        return
      }
      
      try {
        const response = await axios.post('https://pyscalp.com/api/token/refresh/', {
          refresh: refreshToken
        })
        
        this.token = response.data.access
        localStorage.setItem('token', response.data.access)
        
        // Update Authorization header
        axios.defaults.headers.common['Authorization'] = `Bearer ${response.data.access}`
        
        return response.data
      } catch (error) {
        this.logout()
        throw error
      }
    },
    
    logout() {
      this.user = null
      this.token = null
      
      localStorage.removeItem('token')
      localStorage.removeItem('refreshToken')
      localStorage.removeItem('userRole')
      
      // Remove Authorization header
      delete axios.defaults.headers.common['Authorization']
    }
  }
})
