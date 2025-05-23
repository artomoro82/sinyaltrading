import { defineStore } from 'pinia'
import axios from 'axios'

export const useProductStore = defineStore('product', {
  state: () => ({
    products: [],
    categories: [],
    featuredProducts: [],
    currentProduct: null,
    loading: false,
    error: null
  }),
  
  getters: {
    getProductsByCategory: (state) => (categorySlug) => {
      if (!categorySlug) return state.products
      return state.products.filter(product => product.category.slug === categorySlug)
    },
    
    getProductsByType: (state) => (type) => {
      if (!type) return state.products
      return state.products.filter(product => product.product_type === type)
    },
    
    getFeaturedProducts: (state) => {
      return state.featuredProducts
    }
  },
  
  actions: {
    async fetchProducts(params = {}) {
      this.loading = true
      this.error = null
      
      try {
        const response = await axios.get('https://pyscalp.com/api/products/', { params })
        this.products = response.data
        return response.data
      } catch (error) {
        this.error = error.response?.data || 'Failed to fetch products'
        throw error
      } finally {
        this.loading = false
      }
    },
    
    async fetchFeaturedProducts() {
      this.loading = true
      this.error = null
      
      try {
        const response = await axios.get('https://pyscalp.com/api/products/', { 
          params: { featured: true } 
        })
        this.featuredProducts = response.data
        return response.data
      } catch (error) {
        this.error = error.response?.data || 'Failed to fetch featured products'
        throw error
      } finally {
        this.loading = false
      }
    },
    
    async fetchProductBySlug(slug) {
      this.loading = true
      this.error = null
      
      try {
        const response = await axios.get(`https://pyscalp.com/api/products/${slug}/`)
        this.currentProduct = response.data
        return response.data
      } catch (error) {
        this.error = error.response?.data || 'Failed to fetch product details'
        throw error
      } finally {
        this.loading = false
      }
    },
    
    async fetchCategories() {
      this.loading = true
      this.error = null
      
      try {
        const response = await axios.get('https://pyscalp.com/api/categories/')
        this.categories = response.data
        return response.data
      } catch (error) {
        this.error = error.response?.data || 'Failed to fetch categories'
        throw error
      } finally {
        this.loading = false
      }
    }
  }
})
