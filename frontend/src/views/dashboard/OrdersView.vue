<template>
  <div class="orders-view">
    <h1>My Orders</h1>
    
    <div v-if="loading" class="loading-container">
      <div class="spinner"></div>
      <p>Loading orders...</p>
    </div>
    
    <div v-else-if="error" class="error-container">
      <p class="error-message">{{ error }}</p>
      <button @click="fetchOrders" class="btn btn-primary">Try Again</button>
    </div>
    
    <div v-else-if="orders.length === 0" class="no-orders">
      <p>You don't have any orders yet.</p>
      <button @click="goToProducts" class="btn btn-primary">Browse Products</button>
    </div>
    
    <div v-else class="orders-list">
      <div class="orders-header">
        <div class="order-number">Order #</div>
        <div class="order-date">Date</div>
        <div class="order-total">Total</div>
        <div class="order-status">Status</div>
        <div class="order-actions">Actions</div>
      </div>
      
      <div v-for="order in orders" :key="order.id" class="order-item">
        <div class="order-number">{{ order.order_number }}</div>
        <div class="order-date">{{ formatDate(order.created_at) }}</div>
        <div class="order-total">{{ formatCurrency(order.total) }}</div>
        <div class="order-status">
          <span :class="'status-' + order.status">{{ order.status }}</span>
        </div>
        <div class="order-actions">
          <button @click="viewOrder(order)" class="btn btn-sm btn-secondary">View</button>
          <button 
            v-if="order.payment_status === 'pending'" 
            @click="payOrder(order)" 
            class="btn btn-sm btn-primary"
          >
            Pay Now
          </button>
        </div>
      </div>
    </div>
    
    <div class="pagination" v-if="totalPages > 1">
      <button 
        @click="changePage(currentPage - 1)" 
        :disabled="currentPage === 1"
        class="btn btn-sm btn-secondary"
      >
        Previous
      </button>
      
      <span class="page-info">Page {{ currentPage }} of {{ totalPages }}</span>
      
      <button 
        @click="changePage(currentPage + 1)" 
        :disabled="currentPage === totalPages"
        class="btn btn-sm btn-secondary"
      >
        Next
      </button>
    </div>
  </div>
</template>

<script>
import axios from 'axios';
import authHeader from '@/services/auth-header';
import { API_URL } from '@/services/config';

export default {
  name: 'OrdersView',
  data() {
    return {
      orders: [],
      loading: true,
      error: null,
      currentPage: 1,
      totalPages: 1,
      pageSize: 10
    };
  },
  methods: {
    fetchOrders() {
      this.loading = true;
      this.error = null;
      
      axios.get(`${API_URL}/orders/?page=${this.currentPage}`, { headers: authHeader() })
        .then(response => {
          this.orders = response.data.results;
          this.totalPages = Math.ceil(response.data.count / this.pageSize);
        })
        .catch(error => {
          this.error = error.response?.data?.error || 'Failed to load orders';
        })
        .finally(() => {
          this.loading = false;
        });
    },
    
    formatDate(dateString) {
      const date = new Date(dateString);
      return date.toLocaleDateString();
    },
    
    formatCurrency(amount) {
      return new Intl.NumberFormat('en-US', {
        style: 'currency',
        currency: 'USD'
      }).format(amount);
    },
    
    viewOrder(order) {
      // Navigate to order details page
      this.$router.push(`/dashboard/orders/${order.order_number}`);
    },
    
    payOrder(order) {
      // Navigate to payment page
      this.$router.push(`/dashboard/payment/${order.order_number}`);
    },
    
    goToProducts() {
      this.$router.push('/products');
    },
    
    changePage(page) {
      if (page >= 1 && page <= this.totalPages) {
        this.currentPage = page;
        this.fetchOrders();
      }
    }
  },
  mounted() {
    this.fetchOrders();
  }
};
</script>

<style scoped>
.orders-view {
  padding: 20px;
}

.loading-container,
.error-container,
.no-orders {
  text-align: center;
  padding: 40px;
}

.spinner {
  display: inline-block;
  width: 50px;
  height: 50px;
  border: 3px solid rgba(0, 0, 0, 0.1);
  border-radius: 50%;
  border-top-color: #3498db;
  animation: spin 1s ease-in-out infinite;
  margin-bottom: 20px;
}

@keyframes spin {
  to { transform: rotate(360deg); }
}

.error-message {
  color: #e74c3c;
  margin-bottom: 20px;
}

.orders-list {
  background-color: #fff;
  border-radius: 8px;
  box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
  overflow: hidden;
}

.orders-header {
  display: flex;
  background-color: #f8f9fa;
  padding: 15px;
  font-weight: bold;
  border-bottom: 1px solid #eee;
}

.order-item {
  display: flex;
  padding: 15px;
  border-bottom: 1px solid #eee;
}

.order-item:last-child {
  border-bottom: none;
}

.order-number,
.order-date,
.order-total,
.order-status,
.order-actions {
  flex: 1;
}

.order-actions {
  display: flex;
  gap: 10px;
  justify-content: flex-end;
}

.status-pending {
  color: #f39c12;
}

.status-processing {
  color: #3498db;
}

.status-completed {
  color: #2ecc71;
}

.status-cancelled {
  color: #e74c3c;
}

.pagination {
  display: flex;
  justify-content: center;
  align-items: center;
  margin-top: 20px;
  gap: 10px;
}

.page-info {
  margin: 0 10px;
}

.btn {
  display: inline-block;
  padding: 10px 20px;
  border: none;
  border-radius: 4px;
  cursor: pointer;
  font-weight: bold;
  transition: background-color 0.3s;
}

.btn-primary {
  background-color: #3498db;
  color: white;
}

.btn-primary:hover {
  background-color: #2980b9;
}

.btn-secondary {
  background-color: #95a5a6;
  color: white;
}

.btn-secondary:hover {
  background-color: #7f8c8d;
}

.btn-sm {
  padding: 5px 10px;
  font-size: 0.8em;
}

.btn:disabled {
  opacity: 0.5;
  cursor: not-allowed;
}

@media (max-width: 768px) {
  .orders-header {
    display: none;
  }
  
  .order-item {
    flex-direction: column;
    gap: 5px;
  }
  
  .order-number,
  .order-date,
  .order-total,
  .order-status,
  .order-actions {
    flex: none;
    width: 100%;
  }
  
  .order-actions {
    margin-top: 10px;
  }
}
</style>