<template>
  <div class="payment-processor">
    <div v-if="loading" class="payment-loading">
      <div class="spinner"></div>
      <p>{{ loadingMessage }}</p>
    </div>
    
    <div v-else-if="error" class="payment-error">
      <div class="error-icon">
        <i class="fas fa-exclamation-circle"></i>
      </div>
      <h3>Payment Error</h3>
      <p>{{ error }}</p>
      <button @click="retry" class="btn btn-primary">Try Again</button>
    </div>
    
    <div v-else-if="paymentStatus === 'completed'" class="payment-success">
      <div class="success-icon">
        <i class="fas fa-check-circle"></i>
      </div>
      <h3>Payment Successful!</h3>
      <p>Your payment has been processed successfully.</p>
      <button @click="goToOrder" class="btn btn-primary">View Order</button>
    </div>
    
    <div v-else-if="paymentStatus === 'pending' && cryptoPayment" class="crypto-payment">
      <h3>Crypto Payment</h3>
      <div class="crypto-details">
        <div class="qr-code">
          <img :src="getQRCode(cryptoPayment.pay_address, cryptoPayment.pay_amount, cryptoPayment.pay_currency)" alt="QR Code" />
        </div>
        <div class="payment-info">
          <p><strong>Amount:</strong> {{ cryptoPayment.pay_amount }} {{ cryptoPayment.pay_currency }}</p>
          <p><strong>Address:</strong> {{ cryptoPayment.pay_address }}</p>
          <div class="copy-address">
            <input type="text" readonly :value="cryptoPayment.pay_address" ref="addressInput" />
            <button @click="copyAddress" class="btn btn-sm btn-secondary">
              <i class="fas fa-copy"></i> Copy
            </button>
          </div>
          <p class="payment-note">
            Please send exactly {{ cryptoPayment.pay_amount }} {{ cryptoPayment.pay_currency }} to the address above.
            The payment status will update automatically once confirmed.
          </p>
        </div>
      </div>
      <div class="payment-status">
        <p><strong>Status:</strong> {{ getStatusText(paymentStatus) }}</p>
        <div class="progress">
          <div class="progress-bar" :style="{ width: getProgressWidth() }"></div>
        </div>
      </div>
    </div>
    
    <div v-else-if="paymentStatus === 'pending' && paymentUrl" class="redirect-payment">
      <h3>Complete Your Payment</h3>
      <p>You will be redirected to our payment processor to complete your payment.</p>
      <button @click="redirectToPayment" class="btn btn-primary">
        Proceed to Payment
      </button>
    </div>
    
    <div v-else class="payment-processing">
      <h3>Payment Processing</h3>
      <p>Your payment is being processed. Please do not close this window.</p>
      <div class="payment-status">
        <p><strong>Status:</strong> {{ getStatusText(paymentStatus) }}</p>
        <div class="progress">
          <div class="progress-bar" :style="{ width: getProgressWidth() }"></div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import PaymentService from '@/services/payment.service';

export default {
  name: 'PaymentProcessor',
  props: {
    orderId: {
      type: String,
      required: true
    }
  },
  data() {
    return {
      loading: true,
      loadingMessage: 'Initializing payment...',
      error: null,
      paymentId: null,
      paymentStatus: null,
      paymentData: null,
      cryptoPayment: null,
      paymentUrl: null,
      pollingInterval: null
    };
  },
  created() {
    this.initializePayment();
  },
  beforeDestroy() {
    this.stopPolling();
  },
  methods: {
    initializePayment() {
      this.loading = true;
      this.loadingMessage = 'Initializing payment...';
      this.error = null;
      
      PaymentService.createPayment(this.orderId)
        .then(response => {
          this.paymentId = response.data.payment_id;
          this.paymentStatus = response.data.status;
          this.paymentData = response.data;
          
          // Check if we have gateway data
          if (response.data.gateway_data) {
            const gatewayData = response.data.gateway_data;
            
            // Check if we have a payment URL
            if (gatewayData.invoice_url) {
              this.paymentUrl = gatewayData.invoice_url;
            }
            
            // Check if we have crypto payment details
            if (gatewayData.pay_address && gatewayData.pay_amount) {
              this.cryptoPayment = gatewayData;
            }
          }
          
          this.loading = false;
          this.startPolling();
        })
        .catch(error => {
          this.loading = false;
          this.error = error.response?.data?.error || 'Failed to initialize payment. Please try again.';
        });
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
          
          this.paymentStatus = status;
          this.paymentData = data;
          
          // If payment is complete, redirect to order page
          if (status === 'completed') {
            setTimeout(() => {
              this.goToOrder();
            }, 3000);
          }
        }
      );
    },
    stopPolling() {
      if (this.pollingInterval) {
        this.pollingInterval.stop();
      }
    },
    retry() {
      this.initializePayment();
    },
    goToOrder() {
      this.$router.push({ name: 'order-detail', params: { id: this.orderId } });
    },
    redirectToPayment() {
      if (this.paymentUrl) {
        window.location.href = this.paymentUrl;
      }
    },
    copyAddress() {
      const addressInput = this.$refs.addressInput;
      addressInput.select();
      document.execCommand('copy');
      
      // Show a toast or notification
      this.$toast.success('Address copied to clipboard');
    },
    getStatusText(status) {
      const statusMap = {
        'pending': 'Waiting for payment',
        'processing': 'Processing payment',
        'completed': 'Payment completed',
        'failed': 'Payment failed',
        'refunded': 'Payment refunded'
      };
      
      return statusMap[status] || status;
    },
    getProgressWidth() {
      const statusProgress = {
        'pending': '25%',
        'processing': '75%',
        'completed': '100%',
        'failed': '100%',
        'refunded': '100%'
      };
      
      return statusProgress[this.paymentStatus] || '0%';
    },
    getQRCode(address, amount, currency) {
      // Generate a QR code URL for the payment
      // Using a public QR code generator service
      const data = `${currency.toLowerCase()}:${address}?amount=${amount}`;
      return `https://chart.googleapis.com/chart?chs=250x250&cht=qr&chl=${encodeURIComponent(data)}`;
    }
  }
};
</script>

<style scoped>
.payment-processor {
  max-width: 800px;
  margin: 0 auto;
  padding: 2rem;
  background-color: #fff;
  border-radius: 8px;
  box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
}

.payment-loading,
.payment-error,
.payment-success,
.payment-processing,
.crypto-payment,
.redirect-payment {
  text-align: center;
  padding: 2rem;
}

.spinner {
  display: inline-block;
  width: 50px;
  height: 50px;
  border: 3px solid rgba(0, 0, 0, 0.1);
  border-radius: 50%;
  border-top-color: #3498db;
  animation: spin 1s ease-in-out infinite;
}

@keyframes spin {
  to { transform: rotate(360deg); }
}

.error-icon,
.success-icon {
  font-size: 4rem;
  margin-bottom: 1rem;
}

.error-icon {
  color: #e74c3c;
}

.success-icon {
  color: #2ecc71;
}

.crypto-details {
  display: flex;
  flex-wrap: wrap;
  justify-content: center;
  gap: 2rem;
  margin: 2rem 0;
}

.qr-code {
  flex: 0 0 250px;
}

.qr-code img {
  max-width: 100%;
  height: auto;
}

.payment-info {
  flex: 1 1 300px;
  text-align: left;
}

.copy-address {
  display: flex;
  margin: 1rem 0;
}

.copy-address input {
  flex: 1;
  padding: 0.5rem;
  border: 1px solid #ddd;
  border-radius: 4px 0 0 4px;
  font-size: 0.9rem;
}

.copy-address button {
  border-radius: 0 4px 4px 0;
}

.payment-note {
  font-size: 0.9rem;
  color: #666;
  margin-top: 1rem;
}

.payment-status {
  margin-top: 2rem;
}

.progress {
  height: 10px;
  background-color: #f1f1f1;
  border-radius: 5px;
  overflow: hidden;
  margin-top: 0.5rem;
}

.progress-bar {
  height: 100%;
  background-color: #3498db;
  transition: width 0.5s ease;
}

.btn {
  display: inline-block;
  padding: 0.5rem 1rem;
  background-color: #3498db;
  color: white;
  border: none;
  border-radius: 4px;
  cursor: pointer;
  font-size: 1rem;
  transition: background-color 0.3s;
}

.btn:hover {
  background-color: #2980b9;
}

.btn-secondary {
  background-color: #95a5a6;
}

.btn-secondary:hover {
  background-color: #7f8c8d;
}

.btn-sm {
  padding: 0.25rem 0.5rem;
  font-size: 0.875rem;
}

@media (max-width: 768px) {
  .payment-processor {
    padding: 1rem;
  }
  
  .crypto-details {
    flex-direction: column;
    align-items: center;
  }
  
  .payment-info {
    width: 100%;
  }
}
</style>