<template>
  <div class="subscriptions-view">
    <h1>My Subscriptions</h1>
    
    <div v-if="loading" class="loading-container">
      <div class="spinner"></div>
      <p>Loading subscriptions...</p>
    </div>
    
    <div v-else-if="error" class="error-container">
      <p class="error-message">{{ error }}</p>
      <button @click="fetchSubscriptions" class="btn btn-primary">Try Again</button>
    </div>
    
    <div v-else-if="subscriptions.length === 0" class="no-subscriptions">
      <p>You don't have any active subscriptions.</p>
      <button @click="browsePlans" class="btn btn-primary">Browse Subscription Plans</button>
    </div>
    
    <div v-else class="subscriptions-list">
      <div v-for="subscription in subscriptions" :key="subscription.id" class="subscription-card">
        <div class="subscription-header">
          <h3>{{ subscription.subscription_plan.name }}</h3>
          <span :class="'status-' + subscription.status">{{ subscription.status }}</span>
        </div>
        
        <div class="subscription-details">
          <div class="detail-row">
            <span class="detail-label">Product:</span>
            <span class="detail-value">{{ subscription.subscription_plan.product.name }}</span>
          </div>
          
          <div class="detail-row">
            <span class="detail-label">Billing Cycle:</span>
            <span class="detail-value">{{ formatBillingCycle(subscription.subscription_plan.billing_cycle) }}</span>
          </div>
          
          <div class="detail-row">
            <span class="detail-label">Price:</span>
            <span class="detail-value">{{ formatCurrency(subscription.subscription_plan.price) }}</span>
          </div>
          
          <div class="detail-row">
            <span class="detail-label">Start Date:</span>
            <span class="detail-value">{{ formatDate(subscription.start_date) }}</span>
          </div>
          
          <div class="detail-row">
            <span class="detail-label">End Date:</span>
            <span class="detail-value">{{ formatDate(subscription.end_date) }}</span>
          </div>
          
          <div class="detail-row">
            <span class="detail-label">Auto Renew:</span>
            <span class="detail-value">{{ subscription.auto_renew ? 'Yes' : 'No' }}</span>
          </div>
          
          <div v-if="subscription.next_payment_date" class="detail-row">
            <span class="detail-label">Next Payment:</span>
            <span class="detail-value">{{ formatDate(subscription.next_payment_date) }}</span>
          </div>
        </div>
        
        <div class="subscription-features">
          <h4>Features</h4>
          <ul>
            <li v-for="(feature, index) in subscription.subscription_plan.features" :key="index">
              {{ feature }}
            </li>
          </ul>
        </div>
        
        <div class="subscription-actions">
          <button 
            v-if="subscription.status === 'active' && subscription.auto_renew" 
            @click="cancelAutoRenew(subscription)" 
            class="btn btn-danger"
          >
            Cancel Auto Renew
          </button>
          
          <button 
            v-if="subscription.status === 'active' && !subscription.auto_renew" 
            @click="enableAutoRenew(subscription)" 
            class="btn btn-primary"
          >
            Enable Auto Renew
          </button>
          
          <button 
            v-if="subscription.status === 'cancelled'" 
            @click="renewSubscription(subscription)" 
            class="btn btn-primary"
          >
            Renew Subscription
          </button>
          
          <button 
            v-if="subscription.status === 'expired'" 
            @click="reactivateSubscription(subscription)" 
            class="btn btn-primary"
          >
            Reactivate
          </button>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import axios from 'axios';
import authHeader from '@/services/auth-header';
import { API_URL } from '@/services/config';

export default {
  name: 'SubscriptionsView',
  data() {
    return {
      subscriptions: [],
      loading: true,
      error: null
    };
  },
  methods: {
    fetchSubscriptions() {
      this.loading = true;
      this.error = null;
      
      axios.get(`${API_URL}/subscriptions/`, { headers: authHeader() })
        .then(response => {
          this.subscriptions = response.data;
        })
        .catch(error => {
          this.error = error.response?.data?.error || 'Failed to load subscriptions';
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
    
    formatBillingCycle(cycle) {
      const cycles = {
        'monthly': 'Monthly',
        'quarterly': 'Quarterly (Every 3 Months)',
        'biannually': 'Biannually (Every 6 Months)',
        'annually': 'Annually (Yearly)'
      };
      
      return cycles[cycle] || cycle;
    },
    
    browsePlans() {
      this.$router.push('/products?type=subscription');
    },
    
    cancelAutoRenew(subscription) {
      if (confirm('Are you sure you want to cancel auto-renewal for this subscription?')) {
        axios.post(
          `${API_URL}/subscriptions/${subscription.id}/cancel-auto-renew/`,
          {},
          { headers: authHeader() }
        )
          .then(() => {
            this.$emit('success', 'Auto-renewal has been cancelled');
            this.fetchSubscriptions();
          })
          .catch(error => {
            this.$emit('error', error.response?.data?.error || 'Failed to cancel auto-renewal');
          });
      }
    },
    
    enableAutoRenew(subscription) {
      axios.post(
        `${API_URL}/subscriptions/${subscription.id}/enable-auto-renew/`,
        {},
        { headers: authHeader() }
      )
        .then(() => {
          this.$emit('success', 'Auto-renewal has been enabled');
          this.fetchSubscriptions();
        })
        .catch(error => {
          this.$emit('error', error.response?.data?.error || 'Failed to enable auto-renewal');
        });
    },
    
    renewSubscription(subscription) {
      this.$router.push(`/products/${subscription.subscription_plan.product.slug}?plan=${subscription.subscription_plan.id}`);
    },
    
    reactivateSubscription(subscription) {
      this.$router.push(`/products/${subscription.subscription_plan.product.slug}?plan=${subscription.subscription_plan.id}`);
    }
  },
  mounted() {
    this.fetchSubscriptions();
  }
};
</script>

<style scoped>
.subscriptions-view {
  padding: 20px;
}

.loading-container,
.error-container,
.no-subscriptions {
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

.subscriptions-list {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(300px, 1fr));
  gap: 20px;
}

.subscription-card {
  background-color: #fff;
  border-radius: 8px;
  box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
  overflow: hidden;
}

.subscription-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 15px;
  background-color: #f8f9fa;
  border-bottom: 1px solid #eee;
}

.subscription-header h3 {
  margin: 0;
}

.status-active {
  color: #2ecc71;
  font-weight: bold;
}

.status-cancelled {
  color: #e74c3c;
  font-weight: bold;
}

.status-expired {
  color: #95a5a6;
  font-weight: bold;
}

.status-pending {
  color: #f39c12;
  font-weight: bold;
}

.subscription-details {
  padding: 15px;
  border-bottom: 1px solid #eee;
}

.detail-row {
  display: flex;
  margin-bottom: 10px;
}

.detail-row:last-child {
  margin-bottom: 0;
}

.detail-label {
  flex: 1;
  font-weight: bold;
}

.detail-value {
  flex: 2;
}

.subscription-features {
  padding: 15px;
  border-bottom: 1px solid #eee;
}

.subscription-features h4 {
  margin-top: 0;
  margin-bottom: 10px;
}

.subscription-features ul {
  margin: 0;
  padding-left: 20px;
}

.subscription-features li {
  margin-bottom: 5px;
}

.subscription-actions {
  padding: 15px;
  display: flex;
  justify-content: center;
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

.btn-danger {
  background-color: #e74c3c;
  color: white;
}

.btn-danger:hover {
  background-color: #c0392b;
}

@media (max-width: 768px) {
  .subscriptions-list {
    grid-template-columns: 1fr;
  }
}
</style>