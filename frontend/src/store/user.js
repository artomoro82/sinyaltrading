import { defineStore } from 'pinia'
import axios from 'axios'

export const useUserStore = defineStore('user', {
  state: () => ({
    profile: null,
    subscriptions: [],
    botLicenses: [],
    loading: false,
    error: null
  }),
  
  actions: {
    async fetchUserProfile() {
      this.loading = true
      this.error = null
      
      try {
        const response = await axios.get('https://pyscalp.com/api/users/profile/')
        this.profile = response.data
        return response.data
      } catch (error) {
        this.error = error.response?.data || 'Failed to fetch user profile'
        throw error
      } finally {
        this.loading = false
      }
    },
    
    async updateUserProfile(profileData) {
      this.loading = true
      this.error = null
      
      try {
        const response = await axios.put('https://pyscalp.com/api/users/profile/', profileData)
        this.profile = response.data
        return response.data
      } catch (error) {
        this.error = error.response?.data || 'Failed to update user profile'
        throw error
      } finally {
        this.loading = false
      }
    },
    
    async fetchUserSubscriptions() {
      this.loading = true
      this.error = null
      
      try {
        const response = await axios.get('https://pyscalp.com/api/users/subscriptions/')
        this.subscriptions = response.data
        return response.data
      } catch (error) {
        this.error = error.response?.data || 'Failed to fetch user subscriptions'
        throw error
      } finally {
        this.loading = false
      }
    },
    
    async fetchUserBotLicenses() {
      this.loading = true
      this.error = null
      
      try {
        const response = await axios.get('https://pyscalp.com/api/users/bot-licenses/')
        this.botLicenses = response.data
        return response.data
      } catch (error) {
        this.error = error.response?.data || 'Failed to fetch bot licenses'
        throw error
      } finally {
        this.loading = false
      }
    }
  }
})
