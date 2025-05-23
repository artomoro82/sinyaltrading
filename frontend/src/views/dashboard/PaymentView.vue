<template>
  <div class="payment-view">
    <div class="payment-header">
      <h1>Payment</h1>
      <p v-if="order">Complete your payment for order #{{ order.order_number }}</p>
    </div>
    
    <div v-if="loading" class="loading-container">
      <div class="spinner"></div>
      <p>Loading order details...</p>
    </div>
    
    <div v-else-if="error" class="error-container">
      <div class="error-icon">❌</div>
      <h3>Error</h3>
      <p>{{ error }}</p>
      <button @click="goBack" class="btn btn-secondary">Go Back</button>
    </div>
    
    <div v-else-if="order" class="order-details">
      <div class="order-summary">
        <h3>Order Summary</h3>
        <div class="order-info">
          <p><strong>Order Number:</strong> {{ order.order_number }}</p>
          <p><strong>Date:</strong> {{ formatDate(order.created_at) }}</p>
          <p><strong>Status:</strong> <span :class="'status-' + order.status">{{ order.status }}</span></p>
          <p><strong>Payment Status:</strong> <span :class="'status-' + order.payment_status">{{ order.payment_status }}</span></p>
        </div>
        
        <div class="order-items">
          <h4>Items</h4>
          <div v-for="(item, index) in order.items" :key="index" class="order-item">
            <div class="item-details">
              <p class="item-name">{{ item.product ? item.product.name : item.product_bundle.name }}</p>
              <p class="item-price">{{ formatCurrency(item.price) }} x {{ item.quantity }}</p>
            </div>
            <div class="item-subtotal">{{ formatCurrency(item.subtotal) }}</div>
          </div>
        </div>
        
        <div class="order-totals">
          <div class="total-row">
            <span>Subtotal</span>
            <span>{{ formatCurrency(order.subtotal) }}</span>
          </div>
          <div v-if="order.tax > 0" class="total-row">
            <span>Tax</span>
            <span>{{ formatCurrency(order.tax) }}</span>
          </div>
          <div v-if="order.discount > 0" class="total-row">
            <span>Discount</span>
            <span>-{{ formatCurrency(order.discount) }}</span>
          </div>
          <div class="total-row grand-total">
            <span>Total</span>
            <span>{{ formatCurrency(order.total) }}</span>
          </div>
        </div>
      </div>
      
      <div class="payment-container">
        <payment-form 
          :order-id="orderId"
        ></payment-form>
      </div>
    </div>
    
    <div v-else class="no-order">
      <p>No order found. Please go back and try again.</p>
      <button @click="goBack" class="btn btn-primary">Go Back</button>
    </div>
    
    <div v-if="notification" class="notification">
      {{ notification }}
    </div>
  </div>
</template>

<script>
import PaymentForm from '@/components/payment/PaymentProcessor.vue';
import axios from 'axios';
import authHeader from '@/services/auth-header';
import { API_URL } from '@/services/config';

export default {
  name: 'PaymentView',
  components: {
    PaymentForm
  },
  data() {
    return {
      loading: true,
      error: null,
      order: null,
      notification: null,
      notificationTimeout: null
    };
  },
  computed: {
    orderId() {
      return this.$route.params.id;
    }
  },
  methods: {
    fetchOrder() {
      this.loading = true;
      
      axios.get(`${API_URL}/orders/${this.orderId}/`, { headers: authHeader() })
        .then(response => {
          this.order = response.data;
        })
        .catch(error => {
          this.error = error.response?.data?.error || 'Failed to load order details';
        })
        .finally(() => {
          this.loading = false;
        });
    },
    
    formatDate(dateString) {
      const date = new Date(dateString);
      return date.toLocaleDateString() + ' ' + date.toLocaleTimeString();
    },
    
    formatCurrency(amount) {
      return new Intl.NumberFormat('en-US', {
        style: 'currency',
        currency: this.order?.currency || 'USD'
      }).format(amount);
    },
    
    goBack() {
      this.$router.go(-1);
    },
    
    showNotification(message) {
      this.notification = message;
      
      if (this.notificationTimeout) {
        clearTimeout(this.notificationTimeout);
      }
      
      this.notificationTimeout = setTimeout(() => {
        this.notification = null;
      }, 3000);
    }
  },
  mounted() {
    if (this.orderId) {
      this.fetchOrder();
    } else {
      this.loading = false;
      this.error = 'No order ID provided';
    }
  },
  beforeDestroy() {
    if (this.notificationTimeout) {
      clearTimeout(this.notificationTimeout);
    }
  }
};
</script>

<style scoped>
.payment-view {
  padding: 20px;
  position: relative;
}

.payment-header {
  margin-bottom: 20px;
}

.loading-container,
.error-container,
.no-order {
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

.error-icon {
  font-size: 48px;
  margin-bottom: 20px;
}

.order-details {
  display: flex;
  flex-wrap: wrap;
  gap: 20px;
}

.order-summary {
  flex: 1;
  min-width: 300px;
  background-color: #fff;
  border-radius: 8px;
  box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
  padding: 20px;
}

.order-info {
  margin-bottom: 20px;
}

.status-pending,
.status-processing {
  color: #f39c12;
}

.status-completed,
.status-paid {
  color: #2ecc71;
}

.status-cancelled,
.status-failed {
  color: #e74c3c;
}

.status-refunded {
  color: #3498db;
}

.order-items {
  margin-bottom: 20px;
}

.order-item {
  display: flex;
  justify-content: space-between;
  padding: 10px 0;
  border-bottom: 1px solid #eee;
}

.item-details {
  flex: 1;
}

.item-name {
  font-weight: bold;
  margin-bottom: 5px;
}

.order-totals {
  margin-top: 20px;
}

.total-row {
  display: flex;
  justify-content: space-between;
  padding: 5px 0;
}

.grand-total {
  font-weight: bold;
  font-size: 1.2em;
  border-top: 1px solid #ddd;
  padding-top: 10px;
  margin-top: 10px;
}

.payment-container {
  flex: 1;
  min-width: 300px;
}

.notification {
  position: fixed;
  bottom: 20px;
  right: 20px;
  background-color: #2ecc71;
  color: white;
  padding: 10px 20px;
  border-radius: 4px;
  box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
  z-index: 1000;
}

.btn {
  display: inline-block;
  padding: 10px 20px;
  margin: 10px 0;
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

@media (max-width: 768px) {
  .order-details {
    flex-direction: column;
  }
}
</style>