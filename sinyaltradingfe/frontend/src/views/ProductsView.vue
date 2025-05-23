<template>
  <div class="products-page">
    <div class="products-header">
      <h1>Our Products</h1>
      <p>Explore our range of trading signals and financial tools</p>
    </div>
    
    <div v-if="loading" class="loading-container">
      <div class="loading-spinner"></div>
      <p>Loading products...</p>
    </div>
    
    <div v-else-if="error" class="error-container">
      <p>{{ error }}</p>
      <button @click="fetchProducts" class="btn-retry">Try Again</button>
    </div>
    
    <div v-else-if="products.length === 0" class="empty-container">
      <p>No products available at the moment. Please check back later.</p>
    </div>
    
    <div v-else class="products-grid">
      <div v-for="product in products" :key="product.id" class="product-card">
        <div class="product-image">
          <img :src="product.image || 'https://via.placeholder.com/300x200'" :alt="product.name">
          <div v-if="product.featured" class="featured-badge">Featured</div>
        </div>
        <div class="product-content">
          <h3>{{ product.name }}</h3>
          <p class="product-description">{{ product.short_description }}</p>
          <div class="product-price">
            <span class="price">${{ product.price }}</span>
            <span v-if="product.discount_price" class="discount-price">${{ product.discount_price }}</span>
          </div>
          <button class="btn-view-details">View Details</button>
        </div>
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
      // Sample products for initial display if API fails
      sampleProducts: [
        {
          id: 1,
          name: 'Basic Trading Signals',
          short_description: 'Get access to our basic trading signals with daily updates.',
          price: 29.99,
          discount_price: null,
          featured: false,
          image: 'https://via.placeholder.com/300x200?text=Basic+Trading+Signals'
        },
        {
          id: 2,
          name: 'Premium Trading Signals',
          short_description: 'Advanced trading signals with real-time updates and analysis.',
          price: 99.99,
          discount_price: 79.99,
          featured: true,
          image: 'https://via.placeholder.com/300x200?text=Premium+Trading+Signals'
        },
        {
          id: 3,
          name: 'Market Analysis Tool',
          short_description: 'Comprehensive tool for market analysis and trend prediction.',
          price: 149.99,
          discount_price: null,
          featured: false,
          image: 'https://via.placeholder.com/300x200?text=Market+Analysis+Tool'
        }
      ]
    }
  },
  computed: {
    ...mapState(useProductStore, ['products', 'loading', 'error'])
  },
  methods: {
    ...mapActions(useProductStore, ['fetchProducts']),
    
    // Fallback method to use sample products if API fails
    useSampleProducts() {
      const productStore = useProductStore()
      productStore.$patch({
        products: this.sampleProducts,
        loading: false,
        error: null
      })
    }
  },
  async mounted() {
    try {
      await this.fetchProducts()
      
      // If no products returned from API, use sample products
      if (this.products.length === 0) {
        this.useSampleProducts()
      }
    } catch (error) {
      console.error('Failed to fetch products:', error)
      // Use sample products as fallback
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

.loading-spinner {
  display: inline-block;
  width: 50px;
  height: 50px;
  border: 5px solid rgba(0, 0, 0, 0.1);
  border-radius: 50%;
  border-top-color: var(--primary-color, #4361ee);
  animation: spin 1s ease-in-out infinite;
  margin-bottom: 20px;
}

@keyframes spin {
  to { transform: rotate(360deg); }
}

.btn-retry {
  background-color: var(--primary-color, #4361ee);
  color: white;
  border: none;
  padding: 10px 20px;
  border-radius: 5px;
  cursor: pointer;
  font-weight: 600;
  margin-top: 20px;
}

.products-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(300px, 1fr));
  gap: 30px;
}

.product-card {
  background-color: white;
  border-radius: 10px;
  overflow: hidden;
  box-shadow: 0 5px 15px rgba(0, 0, 0, 0.1);
  transition: transform 0.3s ease, box-shadow 0.3s ease;
}

.product-card:hover {
  transform: translateY(-5px);
  box-shadow: 0 10px 25px rgba(0, 0, 0, 0.15);
}

.product-image {
  position: relative;
  height: 200px;
  overflow: hidden;
}

.product-image img {
  width: 100%;
  height: 100%;
  object-fit: cover;
  transition: transform 0.5s ease;
}

.product-card:hover .product-image img {
  transform: scale(1.05);
}

.featured-badge {
  position: absolute;
  top: 10px;
  right: 10px;
  background-color: var(--accent-color, #ff6b6b);
  color: white;
  padding: 5px 10px;
  border-radius: 4px;
  font-size: 0.8rem;
  font-weight: 600;
}

.product-content {
  padding: 20px;
}

.product-content h3 {
  margin-top: 0;
  margin-bottom: 10px;
  font-size: 1.3rem;
  color: var(--text-color, #333);
}

.product-description {
  color: var(--secondary-text-color, #666);
  margin-bottom: 15px;
  line-height: 1.5;
  height: 4.5em;
  overflow: hidden;
  display: -webkit-box;
  -webkit-line-clamp: 3;
  -webkit-box-orient: vertical;
}

.product-price {
  display: flex;
  align-items: center;
  margin-bottom: 15px;
}

.price {
  font-size: 1.2rem;
  font-weight: 700;
  color: var(--text-color, #333);
}

.discount-price {
  margin-left: 10px;
  font-size: 1rem;
  text-decoration: line-through;
  color: var(--secondary-text-color, #666);
}

.btn-view-details {
  width: 100%;
  padding: 12px;
  background-color: var(--primary-color, #4361ee);
  color: white;
  border: none;
  border-radius: 5px;
  font-weight: 600;
  cursor: pointer;
  transition: background-color 0.3s ease;
}

.btn-view-details:hover {
  background-color: var(--secondary-color, #3a56d4);
}

@media (max-width: 768px) {
  .products-grid {
    grid-template-columns: repeat(auto-fill, minmax(250px, 1fr));
    gap: 20px;
  }
  
  .products-header h1 {
    font-size: 2rem;
  }
}

@media (max-width: 480px) {
  .products-grid {
    grid-template-columns: 1fr;
  }
  
  .products-header h1 {
    font-size: 1.8rem;
  }
}
</style>
