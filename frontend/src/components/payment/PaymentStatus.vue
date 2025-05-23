<template>
  <div class="payment-status-component">
    <div v-if="loading" class="loading-container">
      <div class="spinner"></div>
      <p>Loading payment information...</p>
    </div>
    
    <div v-else-if="error" class="error-container">
      <div class="error-icon">
        <i class="fas fa-exclamation-triangle"></i>
      </div>
      <h3>Error Loading Payment</h3>
      <p>{{ error }}</p>
      <button @click="fetchPaymentStatus" class="btn btn-primary">Retry</button>
    </div>
    
    <div v-else class="payment-details">
      <div class="status-header" :class="statusClass">
        <div class="status-icon">
          <i :class="statusIcon"></i>
        </div>
        <div class="status-text">
          <h3>{{ statusTitle }}</h3>
          <p>{{ statusDescription }}</p>
        </div>
      </div>
      
      <div class="payment-info">
        <div class="info-row">
          <div class="info-label">Payment ID:</div>
          <div class="info-value">{{ payment.payment_id }}</div>
        </div>
        <div class="info-row">
          <div class="info-label">Amount:</div>
          <div class="info-value">{{ formatCurrency(payment.amount, payment.currency) }}</div>
        </div>
        <div class="info-row">
          <div class="info-label">Payment Method:</div>
          <div class="info-value">{{ formatPaymentMethod(payment.payment_method) }}</div>
        </div>
        <div class="info-row">
          <div class="info-label">Date:</div>
          <div class="info-value">{{ formatDate(payment.created_at) }}</div>
        </div>
        <div class="info-row">
          <div class="info-label">Status:</div>
          <div class="info-value" :class="'status-' + payment.status">
            {{ formatStatus(payment.status) }}
          </div>
        </div>
        <div v-if="payment.transaction_id" class="info-row">
          <div class="info-label">Transaction ID:</div>
          <div class="info-value transaction-id">
            {{ payment.transaction_id }}
            <button @click="copyTransactionId" class="btn-copy">
              <i class="fas fa-copy"></i>
            </button>
          </div>
        </div>
      </div>
      
      <div v-if="payment.status === 'pending'" class="payment-actions">
        <button @click="refreshStatus" class="btn btn-primary">
          <i class="fas fa-sync-alt"></i> Refresh Status
        </button>
        <button @click="viewPaymentInstructions" class="btn btn-secondary">
          View Payment Instructions
        </button>
      </div>
      
      <div v-if="showInstructions && payment.status === 'pending'" class="payment-instructions">
        <h4>Payment Instructions</h4>
        <div v-if="cryptoPayment" class="crypto-instructions">
          <p>Please send exactly <strong>{{ cryptoPayment.pay_amount }} {{ cryptoPayment.pay_currency }}</strong> to the following address:</p>
          <div class="crypto-address">
            <input type="text" readonly :value="cryptoPayment.pay_address" ref="addressInput" />
            <button @click="copyAddress" class="btn-copy">
              <i class="fas fa-copy"></i>
            </button>
          </div>
          <div class="qr-code">
            <img :src="getQRCode(cryptoPayment.pay_address, cryptoPayment.pay_amount, cryptoPayment.pay_currency)" alt="QR Code" />
          </div>
          <p class="note">The payment status will update automatically once confirmed on the blockchain.</p>
        </div>
        <div v-else class="general-instructions">
          <p>Please complete your payment using the method you selected.</p>
          <p v-if="payment.payment_data && payment.payment_data.invoice_url">
            <a :href="payment.payment_data.invoice_url" target="_blank" class="btn btn-primary">
              Go to Payment Page
            </a>
          </p>
        </div>
      </div>
      
      <div class="order-link">
        <router-link :to="{ name: 'order-detail', params: { id: payment.order.order_number } }" class="btn btn-link">
          <i class="fas fa-arrow-left"></i> Back to Order
        </router-link>
      </div>
    </div>
  </div>
</template>

<script>
import PaymentService from '@/services/payment.service';

export default {
  name: 'PaymentStatus',
  props: {
    paymentId: {
      type: String,
      required: true
    }
  },
  data() {
    return {
      loading: true,
      error: null,
      payment: null,
      showInstructions: false,
      pollingInterval: null,
      cryptoPayment: null
    };
  },
  computed: {
    statusClass() {
      const statusClasses = {
        'pending': 'status-pending',
        'processing': 'status-processing',
        'completed': 'status-completed',
        'failed': 'status-failed',
        'refunded': 'status-refunded'
      };
      
      return statusClasses[this.payment?.status] || 'status-unknown';
    },
    statusIcon() {
      const statusIcons = {
        'pending': 'fas fa-clock',
        'processing': 'fas fa-spinner fa-spin',
        'completed': 'fas fa-check-circle',
        'failed': 'fas fa-times-circle',
        'refunded': 'fas fa-undo'
      };
      
      return statusIcons[this.payment?.status] || 'fas fa-question-circle';
    },
    statusTitle() {
      const statusTitles = {
        'pending': 'Payment Pending',
        'processing': 'Payment Processing',
        'completed': 'Payment Completed',
        'failed': 'Payment Failed',
        'refunded': 'Payment Refunded'
      };
      
      return statusTitles[this.payment?.status] || 'Unknown Status';
    },
    statusDescription() {
      const statusDescriptions = {
        'pending': 'We are waiting for your payment to be confirmed.',
        'processing': 'Your payment is being processed.',
        'completed': 'Your payment has been successfully processed.',
        'failed': 'There was an issue processing your payment.',
        'refunded': 'Your payment has been refunded.'
      };
      
      return statusDescriptions[this.payment?.status] || '';
    }
  },
  created() {
    this.fetchPaymentStatus();
  },
  beforeDestroy() {
    this.stopPolling();
  },
  methods: {
    fetchPaymentStatus() {
      this.loading = true;
      this.error = null;
      
      PaymentService.getPaymentStatus(this.paymentId)
        .then(response => {
          this.payment = response.data;
          this.loading = false;
          
          // Extract crypto payment details if available
          if (this.payment.payment_data && 
              this.payment.payment_data.pay_address && 
              this.payment.payment_data.pay_amount) {
            this.cryptoPayment = this.payment.payment_data;
          }
          
          // Start polling if payment is still pending
          if (this.payment.status === 'pending' || this.payment.status === 'processing') {
            this.startPolling();
          }
        })
        .catch(error => {
          this.loading = false;
          this.error = error.response?.data?.error || 'Failed to load payment information.';
        });
    },
    refreshStatus() {
      this.fetchPaymentStatus();
    },
    startPolling() {
      // Poll for payment status updates
      this.pollingInterval = PaymentService.pollPaymentStatus(
        this.paymentId,
        (error, status, data) => {
          if (error) {
            console.error('Payment polling error:', error);
            return;
          }
          
          this.payment = data;
          
          // Stop polling if payment is complete
          if (['completed', 'failed', 'refunded'].includes(status)) {
            this.stopPolling();
          }
        }
      );
    },
    stopPolling() {
      if (this.pollingInterval) {
        this.pollingInterval.stop();
      }
    },
    viewPaymentInstructions() {
      this.showInstructions = !this.showInstructions;
    },
    copyTransactionId() {
      if (this.payment.transaction_id) {
        navigator.clipboard.writeText(this.payment.transaction_id)
          .then(() => {
            this.$toast.success('Transaction ID copied to clipboard');
          })
          .catch(err => {
            console.error('Failed to copy transaction ID:', err);
          });
      }
    },
    copyAddress() {
      const addressInput = this.$refs.addressInput;
      addressInput.select();
      document.execCommand('copy');
      
      this.$toast.success('Address copied to clipboard');
    },
    formatCurrency(amount, currency) {
      return new Intl.NumberFormat('en-US', {
        style: 'currency',
        currency: currency || 'USD'
      }).format(amount);
    },
    formatPaymentMethod(method) {
      const methodMap = {
        'crypto': 'Cryptocurrency',
        'card': 'Credit/Debit Card',
        'bank': 'Bank Transfer'
      };
      
      return methodMap[method] || method;
    },
    formatStatus(status) {
      const statusMap = {
        'pending': 'Pending',
        'processing': 'Processing',
        'completed': 'Completed',
        'failed': 'Failed',
        'refunded': 'Refunded'
      };
      
      return statusMap[status] || status;
    },
    formatDate(dateString) {
      if (!dateString) return '';
      
      const date = new Date(dateString);
      return date.toLocaleString();
    },
    getQRCode(address, amount, currency) {
      // Generate a QR code URL for the payment
      const data = `${currency.toLowerCase()}:${address}?amount=${amount}`;
      return `https://chart.googleapis.com/chart?chs=200x200&cht=qr&chl=${encodeURIComponent(data)}`;
    }
  }
};
</script>

<style scoped>
.payment-status-component {
  max-width: 800px;
  margin: 0 auto;
  padding: 2rem;
  background-color: #fff;
  border-radius: 8px;
  box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
}

.loading-container,
.error-container {
  text-align: center;
  padding: 2rem;
}

.spinner {
  display: inline-block;
  width: 40px;
  height: 40px;
  border: 3px solid rgba(0, 0, 0, 0.1);
  border-radius: 50%;
  border-top-color: #3498db;
  animation: spin 1s ease-in-out infinite;
}

@keyframes spin {
  to { transform: rotate(360deg); }
}

.error-icon {
  font-size: 3rem;
  color: #e74c3c;
  margin-bottom: 1rem;
}

.status-header {
  display: flex;
  align-items: center;
  padding: 1.5rem;
  border-radius: 8px;
  margin-bottom: 2rem;
}

.status-pending {
  background-color: #f8f9fa;
  border-left: 5px solid #ffc107;
}

.status-processing {
  background-color: #e8f4fd;
  border-left: 5px solid #3498db;
}

.status-completed {
  background-color: #e8f8f5;
  border-left: 5px solid #2ecc71;
}

.status-failed {
  background-color: #fdeeee;
  border-left: 5px solid #e74c3c;
}

.status-refunded {
  background-color: #f8f9fa;
  border-left: 5px solid #95a5a6;
}

.status-icon {
  font-size: 2.5rem;
  margin-right: 1.5rem;
}

.status-pending .status-icon {
  color: #ffc107;
}

.status-processing .status-icon {
  color: #3498db;
}

.status-completed .status-icon {
  color: #2ecc71;
}

.status-failed .status-icon {
  color: #e74c3c;
}

.status-refunded .status-icon {
  color: #95a5a6;
}

.status-text h3 {
  margin: 0 0 0.5rem 0;
  font-size: 1.5rem;
}

.status-text p {
  margin: 0;
  color: #666;
}

.payment-info {
  margin-bottom: 2rem;
}

.info-row {
  display: flex;
  padding: 0.75rem 0;
  border-bottom: 1px solid #eee;
}

.info-label {
  flex: 0 0 150px;
  font-weight: bold;
  color: #555;
}

.info-value {
  flex: 1;
}

.status-pending {
  color: #ffc107;
}

.status-processing {
  color: #3498db;
}

.status-completed {
  color: #2ecc71;
}

.status-failed {
  color: #e74c3c;
}

.status-refunded {
  color: #95a5a6;
}

.transaction-id {
  display: flex;
  align-items: center;
  word-break: break-all;
}

.btn-copy {
  background: none;
  border: none;
  color: #3498db;
  cursor: pointer;
  margin-left: 0.5rem;
  padding: 0.25rem;
}

.btn-copy:hover {
  color: #2980b9;
}

.payment-actions {
  display: flex;
  gap: 1rem;
  margin-bottom: 1.5rem;
}

.payment-instructions {
  background-color: #f8f9fa;
  padding: 1.5rem;
  border-radius: 8px;
  margin-bottom: 1.5rem;
}

.payment-instructions h4 {
  margin-top: 0;
  margin-bottom: 1rem;
}

.crypto-address {
  display: flex;
  margin: 1rem 0;
}

.crypto-address input {
  flex: 1;
  padding: 0.5rem;
  border: 1px solid #ddd;
  border-radius: 4px;
  font-size: 0.9rem;
}

.qr-code {
  margin: 1.5rem 0;
  text-align: center;
}

.note {
  font-size: 0.9rem;
  color: #666;
  font-style: italic;
}

.order-link {
  margin-top: 2rem;
  text-align: center;
}

.btn {
  display: inline-block;
  padding: 0.5rem 1rem;
  border: none;
  border-radius: 4px;
  cursor: pointer;
  font-size: 1rem;
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
  background-color: #f1f1f1;
  color: #333;
}

.btn-secondary:hover {
  background-color: #e1e1e1;
}

.btn-link {
  background: none;
  color: #3498db;
  text-decoration: none;
}

.btn-link:hover {
  text-decoration: underline;
}

@media (max-width: 768px) {
  .payment-status-component {
    padding: 1rem;
  }
  
  .status-header {
    flex-direction: column;
    text-align: center;
  }
  
  .status-icon {
    margin-right: 0;
    margin-bottom: 1rem;
  }
  
  .info-row {
    flex-direction: column;
  }
  
  .info-label {
    flex: none;
    margin-bottom: 0.25rem;
  }
  
  .payment-actions {
    flex-direction: column;
  }
}
</style>