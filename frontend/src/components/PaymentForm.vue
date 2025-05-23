<template>
  <div class="payment-form">
    <div v-if="loading" class="payment-loading">
      <div class="spinner"></div>
      <p>Processing your payment...</p>
    </div>
    
    <div v-else-if="error" class="payment-error">
      <div class="error-icon">❌</div>
      <h3>Payment Error</h3>
      <p>{{ error }}</p>
      <button @click="retryPayment" class="btn btn-primary">Try Again</button>
    </div>
    
    <div v-else-if="paymentStatus === 'completed'" class="payment-success">
      <div class="success-icon">✅</div>
      <h3>Payment Successful!</h3>
      <p>Your payment has been processed successfully.</p>
      <button @click="goToDashboard" class="btn btn-primary">Go to Dashboard</button>
    </div>
    
    <div v-else-if="paymentStatus === 'processing'" class="payment-processing">
      <div class="spinner"></div>
      <h3>Payment Processing</h3>
      <p>Your payment is being processed. This may take a few minutes.</p>
      <p>Payment ID: {{ paymentId }}</p>
      <button @click="checkStatus" class="btn btn-secondary">Check Status</button>
    </div>
    
    <div v-else-if="paymentData" class="payment-gateway">
      <h3>Complete Your Payment</h3>
      <div v-if="paymentData.invoice_url" class="payment-redirect">
        <p>You will be redirected to the payment gateway to complete your payment.</p>
        <button @click="redirectToGateway" class="btn btn-primary">Proceed to Payment</button>
      </div>
      
      <div v-else class="payment-details">
        <div class="payment-info">
          <p><strong>Amount:</strong> {{ paymentData.price_amount }} {{ paymentData.price_currency }}</p>
          <p><strong>Order ID:</strong> {{ paymentData.order_id }}</p>
          <p v-if="paymentData.pay_address"><strong>Payment Address:</strong> {{ paymentData.pay_address }}</p>
        </div>
        
        <div v-if="paymentData.pay_address" class="crypto-payment">
          <div class="qr-code">
            <img :src="paymentData.pay_address_qr_code_url" alt="QR Code" />
          </div>
          <p class="instructions">Scan the QR code or copy the address to make your payment.</p>
          <div class="copy-address">
            <input type="text" readonly :value="paymentData.pay_address" />
            <button @click="copyToClipboard(paymentData.pay_address)" class="btn btn-sm btn-secondary">Copy</button>
          </div>
        </div>
      </div>
    </div>
    
    <div v-else class="payment-init">
      <h3>Initialize Payment</h3>
      <p>Click the button below to initialize your payment.</p>
      <button @click="initializePayment" class="btn btn-primary">Pay Now</button>
    </div>
  </div>
</template>

<script>
import PaymentService from '@/services/payment.service';

export default {
  name: 'PaymentForm',
  props: {
    orderId: {
      type: String,
      required: true
    }
  },
  data() {
    return {
      loading: false,
      error: null,
      paymentData: null,
      paymentId: null,
      paymentStatus: 'pending',
      statusPoller: null
    };
  },
  methods: {
    initializePayment() {
      this.loading = true;
      this.error = null;
      
      PaymentService.createPayment(this.orderId)
        .then(response => {
          this.paymentId = response.data.payment_id;
          this.paymentData = response.data.gateway_data;
          this.paymentStatus = 'pending';
          
          // Start polling for status updates
          this.startStatusPolling();
        })
        .catch(error => {
          this.error = error.response?.data?.error || 'Failed to initialize payment';
        })
        .finally(() => {
          this.loading = false;
        });
    },
    
    redirectToGateway() {
      if (this.paymentData && this.paymentData.invoice_url) {
        window.location.href = this.paymentData.invoice_url;
      }
    },
    
    checkStatus() {
      if (!this.paymentId) return;
      
      this.loading = true;
      
      PaymentService.getPaymentStatus(this.paymentId)
        .then(response => {
          this.paymentStatus = response.data.status;
        })
        .catch(error => {
          this.error = error.response?.data?.error || 'Failed to check payment status';
        })
        .finally(() => {
          this.loading = false;
        });
    },
    
    startStatusPolling() {
      if (this.statusPoller) {
        this.statusPoller.stop();
      }
      
      this.statusPoller = PaymentService.pollPaymentStatus(
        this.paymentId,
        (error, status, data) => {
          if (error) {
            this.error = 'Failed to update payment status';
            return;
          }
          
          this.paymentStatus = status;
        }
      );
    },
    
    stopStatusPolling() {
      if (this.statusPoller) {
        this.statusPoller.stop();
        this.statusPoller = null;
      }
    },
    
    retryPayment() {
      this.error = null;
      this.initializePayment();
    },
    
    goToDashboard() {
      this.$router.push('/dashboard');
    },
    
    copyToClipboard(text) {
      navigator.clipboard.writeText(text)
        .then(() => {
          // Show a temporary success message
          this.$emit('copied', 'Address copied to clipboard');
        })
        .catch(err => {
          console.error('Failed to copy: ', err);
        });
    }
  },
  mounted() {
    // If we have an order ID, initialize the payment automatically
    if (this.orderId) {
      this.initializePayment();
    }
  },
  beforeDestroy() {
    this.stopStatusPolling();
  }
};
</script>

<style scoped>
.payment-form {
  max-width: 600px;
  margin: 0 auto;
  padding: 20px;
  background-color: #fff;
  border-radius: 8px;
  box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
}

.payment-loading,
.payment-error,
.payment-success,
.payment-processing,
.payment-gateway,
.payment-init {
  text-align: center;
  padding: 20px;
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

.success-icon,
.error-icon {
  font-size: 48px;
  margin-bottom: 20px;
}

.payment-details {
  margin-top: 20px;
}

.payment-info {
  margin-bottom: 20px;
  text-align: left;
}

.crypto-payment {
  margin-top: 20px;
}

.qr-code {
  margin-bottom: 20px;
}

.qr-code img {
  max-width: 200px;
  border: 1px solid #ddd;
}

.copy-address {
  display: flex;
  margin-top: 10px;
}

.copy-address input {
  flex: 1;
  padding: 8px;
  border: 1px solid #ddd;
  border-radius: 4px 0 0 4px;
}

.copy-address button {
  border-radius: 0 4px 4px 0;
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

.btn-sm {
  padding: 5px 10px;
  font-size: 0.8em;
}
</style>