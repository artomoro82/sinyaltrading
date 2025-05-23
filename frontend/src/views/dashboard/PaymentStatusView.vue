<template>
  <div class="payment-status-view">
    <div class="page-header">
      <h1>Payment Details</h1>
      <router-link :to="{ name: 'payments' }" class="back-link">
        <i class="fas fa-arrow-left"></i> Back to Payments
      </router-link>
    </div>
    
    <payment-status :paymentId="paymentId" />
  </div>
</template>

<script>
import PaymentStatus from '@/components/payment/PaymentStatus.vue';

export default {
  name: 'PaymentStatusView',
  components: {
    PaymentStatus
  },
  props: {
    paymentId: {
      type: String,
      required: true
    }
  },
  created() {
    // Set page title
    document.title = 'Payment Details - Fintech Platform';
  }
};
</script>

<style scoped>
.payment-status-view {
  padding: 2rem;
}

.page-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 2rem;
}

.page-header h1 {
  font-size: 2rem;
  margin: 0;
}

.back-link {
  display: inline-flex;
  align-items: center;
  color: #3498db;
  text-decoration: none;
  font-size: 1rem;
}

.back-link i {
  margin-right: 0.5rem;
}

.back-link:hover {
  text-decoration: underline;
}

@media (max-width: 768px) {
  .payment-status-view {
    padding: 1rem;
  }
  
  .page-header {
    flex-direction: column;
    align-items: flex-start;
    gap: 1rem;
  }
}
</style>