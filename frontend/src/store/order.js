import { defineStore } from 'pinia'
import axios from 'axios'

export const useOrderStore = defineStore('order', {
  state: () => ({
    orders: [],
    currentOrder: null,
    loading: false,
    error: null
  }),
  
  actions: {
    async fetchOrders() {
      this.loading = true
      this.error = null
      
      try {
        const response = await axios.get('https://pyscalp.com/api/orders/')
        this.orders = response.data
        return response.data
      } catch (error) {
        this.error = error.response?.data || 'Failed to fetch orders'
        throw error
      } finally {
        this.loading = false
      }
    },
    
    async fetchOrderByNumber(orderNumber) {
      this.loading = true
      this.error = null
      
      try {
        const response = await axios.get(`https://pyscalp.com/api/orders/${orderNumber}/`)
        this.currentOrder = response.data
        return response.data
      } catch (error) {
        this.error = error.response?.data || 'Failed to fetch order details'
        throw error
      } finally {
        this.loading = false
      }
    },
    
    async createOrder(orderData) {
      this.loading = true
      this.error = null
      
      try {
        const response = await axios.post('https://pyscalp.com/api/orders/create/', orderData)
        return response.data
      } catch (error) {
        this.error = error.response?.data || 'Failed to create order'
        throw error
      } finally {
        this.loading = false
      }
    }
  }
})
