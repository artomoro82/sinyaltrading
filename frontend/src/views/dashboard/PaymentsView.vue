<template>
  <div class="payments-view">
    <div class="page-header">
      <h1>Payment History</h1>
      <p>View and manage your payment history</p>
    </div>
    
    <div class="filters-section">
      <div class="search-filter">
        <input 
          type="text" 
          v-model="searchQuery" 
          placeholder="Search by payment ID or order number" 
          @input="applyFilters"
        />
      </div>
      
      <div class="status-filter">
        <select v-model="statusFilter" @change="applyFilters">
          <option value="">All Statuses</option>
          <option value="pending">Pending</option>
          <option value="processing">Processing</option>
          <option value="completed">Completed</option>
          <option value="failed">Failed</option>
          <option value="refunded">Refunded</option>
        </select>
      </div>
      
      <div class="date-filter">
        <div class="date-range">
          <label>From:</label>
          <input type="date" v-model="dateFrom" @change="applyFilters" />
        </div>
        <div class="date-range">
          <label>To:</label>
          <input type="date" v-model="dateTo" @change="applyFilters" />
        </div>
      </div>
    </div>
    
    <div v-if="loading" class="loading-container">
      <div class="spinner"></div>
      <p>Loading payments...</p>
    </div>
    
    <div v-else-if="error" class="error-container">
      <div class="error-icon">❌</div>
      <h3>Error Loading Payments</h3>
      <p>{{ error }}</p>
      <button @click="fetchPayments" class="btn btn-primary">Try Again</button>
    </div>
    
    <div v-else-if="filteredPayments.length === 0" class="empty-state">
      <div class="empty-icon">💸</div>
      <h3>No Payments Found</h3>
      <p v-if="hasFilters">No payments match your current filters. Try adjusting your search criteria.</p>
      <p v-else>You haven't made any payments yet. Payments will appear here once you make a purchase.</p>
      <router-link to="/products" class="btn btn-primary">Browse Products</router-link>
    </div>
    
    <div v-else class="payments-table-container">
      <table class="payments-table">
        <thead>
          <tr>
            <th @click="sortBy('payment_id')" class="sortable">
              Payment ID
              <span v-if="sortKey === 'payment_id'" class="sort-icon">
                {{ sortOrder === 'asc' ? '▲' : '▼' }}
              </span>
            </th>
            <th @click="sortBy('created_at')" class="sortable">
              Date
              <span v-if="sortKey === 'created_at'" class="sort-icon">
                {{ sortOrder === 'asc' ? '▲' : '▼' }}
              </span>
            </th>
            <th>Order</th>
            <th @click="sortBy('amount')" class="sortable">
              Amount
              <span v-if="sortKey === 'amount'" class="sort-icon">
                {{ sortOrder === 'asc' ? '▲' : '▼' }}
              </span>
            </th>
            <th>Method</th>
            <th @click="sortBy('status')" class="sortable">
              Status
              <span v-if="sortKey === 'status'" class="sort-icon">
                {{ sortOrder === 'asc' ? '▲' : '▼' }}
              </span>
            </th>
            <th>Actions</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="payment in paginatedPayments" :key="payment.payment_id">
            <td>{{ payment.payment_id }}</td>
            <td>{{ formatDate(payment.created_at) }}</td>
            <td>
              <router-link :to="{ name: 'order-detail', params: { id: payment.order.order_number } }">
                {{ payment.order.order_number }}
              </router-link>
            </td>
            <td>{{ formatCurrency(payment.amount, payment.currency) }}</td>
            <td>{{ formatPaymentMethod(payment.payment_method) }}</td>
            <td>
              <span class="status-badge" :class="'status-' + payment.status">
                {{ formatStatus(payment.status) }}
              </span>
            </td>
            <td class="actions-cell">
              <router-link 
                :to="{ name: 'payment-status', params: { paymentId: payment.payment_id } }" 
                class="btn btn-sm btn-primary"
              >
                View
              </router-link>
              <button 
                v-if="payment.status === 'pending'" 
                @click="retryPayment(payment.payment_id)" 
                class="btn btn-sm btn-secondary"
              >
                Retry
              </button>
            </td>
          </tr>
        </tbody>
      </table>
      
      <div class="pagination">
        <button 
          @click="currentPage--" 
          :disabled="currentPage === 1" 
          class="pagination-btn"
        >
          Previous
        </button>
        <span class="page-info">
          Page {{ currentPage }} of {{ totalPages }}
        </span>
        <button 
          @click="currentPage++" 
          :disabled="currentPage === totalPages" 
          class="pagination-btn"
        >
          Next
        </button>
      </div>
    </div>
  </div>
</template>

<script>
import axios from 'axios';
import { API_URL } from '@/config';
import authHeader from '@/services/auth-header';

export default {
  name: 'PaymentsView',
  data() {
    return {
      payments: [],
      loading: true,
      error: null,
      searchQuery: '',
      statusFilter: '',
      dateFrom: '',
      dateTo: '',
      sortKey: 'created_at',
      sortOrder: 'desc',
      currentPage: 1,
      itemsPerPage: 10
    };
  },
  computed: {
    filteredPayments() {
      let result = [...this.payments];
      
      // Apply search filter
      if (this.searchQuery) {
        const query = this.searchQuery.toLowerCase();
        result = result.filter(payment => 
          payment.payment_id.toLowerCase().includes(query) || 
          payment.order.order_number.toLowerCase().includes(query)
        );
      }
      
      // Apply status filter
      if (this.statusFilter) {
        result = result.filter(payment => payment.status === this.statusFilter);
      }
      
      // Apply date filters
      if (this.dateFrom) {
        const fromDate = new Date(this.dateFrom);
        result = result.filter(payment => new Date(payment.created_at) >= fromDate);
      }
      
      if (this.dateTo) {
        const toDate = new Date(this.dateTo);
        toDate.setHours(23, 59, 59, 999); // End of the day
        result = result.filter(payment => new Date(payment.created_at) <= toDate);
      }
      
      // Apply sorting
      result.sort((a, b) => {
        let valueA = a[this.sortKey];
        let valueB = b[this.sortKey];
        
        // Handle nested properties for sorting
        if (this.sortKey.includes('.')) {
          const keys = this.sortKey.split('.');
          valueA = keys.reduce((obj, key) => obj[key], a);
          valueB = keys.reduce((obj, key) => obj[key], b);
        }
        
        // Handle date sorting
        if (this.sortKey === 'created_at') {
          valueA = new Date(valueA);
          valueB = new Date(valueB);
        }
        
        // Handle string sorting
        if (typeof valueA === 'string' && typeof valueB === 'string') {
          if (this.sortOrder === 'asc') {
            return valueA.localeCompare(valueB);
          } else {
            return valueB.localeCompare(valueA);
          }
        }
        
        // Handle number and date sorting
        if (this.sortOrder === 'asc') {
          return valueA - valueB;
        } else {
          return valueB - valueA;
        }
      });
      
      return result;
    },
    paginatedPayments() {
      const start = (this.currentPage - 1) * this.itemsPerPage;
      const end = start + this.itemsPerPage;
      return this.filteredPayments.slice(start, end);
    },
    totalPages() {
      return Math.ceil(this.filteredPayments.length / this.itemsPerPage);
    },
    hasFilters() {
      return this.searchQuery || this.statusFilter || this.dateFrom || this.dateTo;
    }
  },
  methods: {
    fetchPayments() {
      this.loading = true;
      this.error = null;
      
      axios.get(`${API_URL}/payments/`, { headers: authHeader() })
        .then(response => {
          this.payments = response.data;
          this.loading = false;
        })
        .catch(error => {
          this.loading = false;
          this.error = error.response?.data?.error || 'Failed to load payments. Please try again.';
          console.error('Error fetching payments:', error);
        });
    },
    applyFilters() {
      this.currentPage = 1; // Reset to first page when filters change
    },
    sortBy(key) {
      if (this.sortKey === key) {
        this.sortOrder = this.sortOrder === 'asc' ? 'desc' : 'asc';
      } else {
        this.sortKey = key;
        this.sortOrder = 'asc';
      }
    },
    retryPayment(paymentId) {
      this.loading = true;
      
      axios.post(`${API_URL}/payments/${paymentId}/retry/`, {}, { headers: authHeader() })
        .then(response => {
          // Redirect to payment status page
          this.$router.push({ 
            name: 'payment-status', 
            params: { paymentId: response.data.payment_id } 
          });
        })
        .catch(error => {
          this.loading = false;
          this.$toast.error(error.response?.data?.error || 'Failed to retry payment. Please try again.');
          console.error('Error retrying payment:', error);
        });
    },
    formatDate(dateString) {
      if (!dateString) return '';
      
      const date = new Date(dateString);
      return date.toLocaleDateString() + ' ' + date.toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' });
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
    }
  },
  created() {
    this.fetchPayments();
    
    // Set page title
    document.title = 'Payment History - Fintech Platform';
  },
  watch: {
    // Reset to page 1 when items per page changes
    itemsPerPage() {
      this.currentPage = 1;
    }
  }
};
</script>

<style scoped>
.payments-view {
  padding: 2rem;
}

.page-header {
  margin-bottom: 2rem;
}

.page-header h1 {
  font-size: 2rem;
  margin-bottom: 0.5rem;
}

.page-header p {
  color: #666;
}

.filters-section {
  display: flex;
  flex-wrap: wrap;
  gap: 1rem;
  margin-bottom: 2rem;
  padding: 1.5rem;
  background-color: #f8f9fa;
  border-radius: 8px;
}

.search-filter {
  flex: 1 1 300px;
}

.search-filter input {
  width: 100%;
  padding: 0.75rem;
  border: 1px solid #ddd;
  border-radius: 4px;
  font-size: 1rem;
}

.status-filter {
  flex: 0 0 200px;
}

.status-filter select {
  width: 100%;
  padding: 0.75rem;
  border: 1px solid #ddd;
  border-radius: 4px;
  font-size: 1rem;
  background-color: white;
}

.date-filter {
  display: flex;
  gap: 1rem;
  flex: 1 1 300px;
}

.date-range {
  flex: 1;
  display: flex;
  flex-direction: column;
}

.date-range label {
  margin-bottom: 0.5rem;
  font-size: 0.9rem;
  color: #666;
}

.date-range input {
  padding: 0.75rem;
  border: 1px solid #ddd;
  border-radius: 4px;
  font-size: 1rem;
}

.loading-container,
.error-container,
.empty-state {
  text-align: center;
  padding: 3rem;
  background-color: white;
  border-radius: 8px;
  box-shadow: 0 2px 10px rgba(0, 0, 0, 0.05);
}

.spinner {
  display: inline-block;
  width: 50px;
  height: 50px;
  border: 3px solid rgba(0, 0, 0, 0.1);
  border-radius: 50%;
  border-top-color: #3498db;
  animation: spin 1s ease-in-out infinite;
  margin-bottom: 1rem;
}

@keyframes spin {
  to { transform: rotate(360deg); }
}

.error-icon,
.empty-icon {
  font-size: 3rem;
  margin-bottom: 1rem;
}

.error-icon {
  color: #e74c3c;
}

.empty-icon {
  color: #95a5a6;
}

.payments-table-container {
  background-color: white;
  border-radius: 8px;
  box-shadow: 0 2px 10px rgba(0, 0, 0, 0.05);
  overflow: hidden;
}

.payments-table {
  width: 100%;
  border-collapse: collapse;
}

.payments-table th,
.payments-table td {
  padding: 1rem;
  text-align: left;
  border-bottom: 1px solid #eee;
}

.payments-table th {
  background-color: #f8f9fa;
  font-weight: 600;
}

.sortable {
  cursor: pointer;
  position: relative;
}

.sort-icon {
  margin-left: 0.5rem;
  font-size: 0.8rem;
}

.status-badge {
  display: inline-block;
  padding: 0.25rem 0.75rem;
  border-radius: 50px;
  font-size: 0.85rem;
  font-weight: 500;
}

.status-pending {
  background-color: #fff3cd;
  color: #856404;
}

.status-processing {
  background-color: #cce5ff;
  color: #004085;
}

.status-completed {
  background-color: #d4edda;
  color: #155724;
}

.status-failed {
  background-color: #f8d7da;
  color: #721c24;
}

.status-refunded {
  background-color: #e2e3e5;
  color: #383d41;
}

.actions-cell {
  white-space: nowrap;
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
  background-color: #95a5a6;
  color: white;
  margin-left: 0.5rem;
}

.btn-secondary:hover {
  background-color: #7f8c8d;
}

.btn-sm {
  padding: 0.25rem 0.5rem;
  font-size: 0.875rem;
}

.pagination {
  display: flex;
  justify-content: center;
  align-items: center;
  padding: 1rem;
  border-top: 1px solid #eee;
}

.pagination-btn {
  padding: 0.5rem 1rem;
  background-color: #f8f9fa;
  border: 1px solid #ddd;
  border-radius: 4px;
  cursor: pointer;
}

.pagination-btn:disabled {
  opacity: 0.5;
  cursor: not-allowed;
}

.page-info {
  margin: 0 1rem;
  color: #666;
}

@media (max-width: 768px) {
  .payments-view {
    padding: 1rem;
  }
  
  .filters-section {
    flex-direction: column;
    gap: 1rem;
  }
  
  .date-filter {
    flex-direction: column;
  }
  
  .payments-table {
    display: block;
    overflow-x: auto;
  }
}
</style>