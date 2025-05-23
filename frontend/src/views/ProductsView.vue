<template>
  <div>
    <div class="products-header">
      <h1>Products</h1>
      <p>Discover our range of trading solutions</p>
    </div>
    <div v-if="loading" class="loading-container">
      <div class="loading-spinner"></div>
      <p>Loading products...</p>
    </div>
    <div v-else-if="error" class="error-container">
      <p>{{ error }}</p>
    </div>
    <div v-else class="products-list">
      <div v-if="products && products.length > 0" class="product-cards">
        <div v-for="product in products" :key="product.id" class="product-card">
          <img :src="product.image_url || 'https://via.placeholder.com/300x200?text=No+Image'" alt="Product Image" class="product-image"/>
          <div class="product-info">
            <h3>{{ product.name }}</h3>
            <p>{{ product.short_description }}</p>
            <div class="product-price">
              <span v-if="product.sale_price" class="sale-price">${{ product.sale_price }}</span>
              <span :class="{ 'old-price': product.sale_price }">${{ product.price }}</span>
            </div>
          </div>
          <button class="btn-view-details">View Details</button>
        </div>
      </div>
      <div v-else class="empty-container">
        <p>No products available.</p>
      </div>
    </div>
  </div>
</template>

<script>
import { useProductStore } from '@/store/product'
import { mapState, mapActions } from 'pinia'

export default {
  name: 'ProductsView',
  data() {
    return {
      // Sudah diperbaiki: gunakan image_url
      sampleProducts: [
        {
          id: 1,
          name: 'Basic Trading Signals',
          short_description: 'Get access to our basic trading signals with daily updates.',
          price: 29.99,
          sale_price: null,
          featured: false,
          image_url: 'https://via.placeholder.com/300x200?text=Basic+Trading+Signals'
        },
        {
          id: 2,
          name: 'Premium Trading Signals',
          short_description: 'Advanced trading signals with real-time updates and analysis.',
          price: 99.99,
          sale_price: 79.99,
          featured: true,
          image_url: 'https://via.placeholder.com/300x200?text=Premium+Trading+Signals'
        },
        {
          id: 3,
          name: 'Market Analysis Tool',
          short_description: 'Comprehensive tool for market analysis and trend prediction.',
          price: 149.99,
          sale_price: null,
          featured: false,
          image_url: 'https://via.placeholder.com/300x200?text=Market+Analysis+Tool'
        }
      ]
    }
  },
  computed: {
    ...mapState(useProductStore, ['products', 'loading', 'error'])
  },
  methods: {
    ...mapActions(useProductStore, ['fetchProducts']),
    useSampleProducts() {
      const productStore = useProductStore()
      productStore.$patch({
        products: this.sampleProducts,
        loading: false,
        error: null
      })
    },
    initializeWithSampleProducts() {
      this.useSampleProducts()
    }
  },
  created() {
    this.initializeWithSampleProducts()
  },
  async mounted() {
    try {
      await this.fetchProducts()
      if (!this.products || this.products.length === 0) {
        this.useSampleProducts()
      }
    } catch (error) {
      this.useSampleProducts()
    }
    document.title = 'Products - PyScalp'
  }
}
</script>

<style scoped>
.products-page {
  max-width: 1200px;
  margin: 0 auto;
  padding: 40px 20px;
}
.products-header {
  text-align: center;
  margin-bottom: 40px;
}
.products-header h1 {
  font-size: 2.5rem;
  margin-bottom: 10px;
  color: var(--text-color, #333);
}
.products-header p {
  font-size: 1.1rem;
  color: var(--secondary-text-color, #666);
}
.loading-container, .error-container, .empty-container {
  text-align: center;
  padding: 60px 20px;
}
.product-cards {
  display: flex;
  flex-wrap: wrap;
  gap: 24px;
  justify-content: center;
}
.product-card {
  background: #fff;
  border-radius: 10px;
  box-shadow: 0 2px 10px rgba(0,0,0,0.07);
  padding: 18px;
  width: 320px;
  display: flex;
  flex-direction: column;
  align-items: center;
}
.product-image {
  width: 100%;
  height: 200px;
  object-fit: cover;
  border-radius: 8px;
}
.product-info {
  text-align: center;
}
.product-price {
  margin-top: 12px;
  font-size: 1.2rem;
}
.sale-price {
  color: #e53935;
  font-weight: bold;
  margin-right: 8px;
}
.old-price {
  text-decoration: line-through;
  color: #888;
}
.btn-view-details {
  margin-top: 16px;
  background: #3a86ff;
  color: #fff;
  border: none;
  padding: 10px 24px;
  border-radius: 6px;
  cursor: pointer;
  font-weight: bold;
}
</style>
