<template>
  <div class="forgot-password-page">
    <div class="forgot-password-container">
      <div class="forgot-password-card">
        <div class="forgot-password-header">
          <h1>Forgot Password</h1>
          <p>Enter your email address and we'll send you a link to reset your password.</p>
        </div>
        
        <div v-if="error" class="alert alert-danger">
          {{ error }}
        </div>
        
        <div v-if="success" class="alert alert-success">
          {{ success }}
        </div>
        
        <form @submit.prevent="handleSubmit" class="forgot-password-form" v-if="!success">
          <div class="form-group">
            <label for="email">Email Address</label>
            <input 
              type="email" 
              id="email" 
              v-model="email" 
              required 
              placeholder="Enter your email"
              :disabled="loading"
            />
          </div>
          
          <button type="submit" class="btn-submit" :disabled="loading">
            {{ loading ? 'Processing...' : 'Reset Password' }}
          </button>
        </form>
        
        <div class="forgot-password-footer">
          <p>Remember your password? <router-link to="/login">Back to Login</router-link></p>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { useAuthStore } from '@/store/auth'
import { mapActions } from 'pinia'

export default {
  name: 'ForgotPasswordView',
  data() {
    return {
      email: '',
      loading: false,
      error: null,
      success: null
    }
  },
  methods: {
    ...mapActions(useAuthStore, ['requestPasswordReset']),
    
    async handleSubmit() {
      this.loading = true
      this.error = null
      this.success = null
      
      try {
        // Call the API to request password reset
        // This assumes you have a requestPasswordReset action in your auth store
        await this.requestPasswordReset({
          email: this.email
        })
        
        // Show success message
        this.success = 'Password reset link has been sent to your email address. Please check your inbox.'
        this.email = '' // Clear the form
      } catch (error) {
        this.error = error.response?.data?.error || 'Failed to process your request. Please try again later.'
        console.error('Password reset request error:', error)
      } finally {
        this.loading = false
      }
    }
  },
  mounted() {
    // Check if user is already logged in
    const authStore = useAuthStore()
    if (authStore.isAuthenticated) {
      this.$router.push('/dashboard')
    }
    
    document.title = 'Forgot Password - Fintech Platform'
  }
}
</script>

<style scoped>
.forgot-password-page {
  min-height: 100vh;
  display: flex;
  align-items: center;
  justify-content: center;
  background-color: var(--light-bg);
  padding: 40px 20px;
}

.forgot-password-container {
  width: 100%;
  max-width: 480px;
}

.forgot-password-card {
  background-color: white;
  border-radius: 10px;
  box-shadow: 0 5px 20px rgba(0, 0, 0, 0.1);
  padding: 40px;
}

.forgot-password-header {
  text-align: center;
  margin-bottom: 30px;
}

.forgot-password-header h1 {
  font-size: 2rem;
  font-weight: 700;
  margin-bottom: 10px;
  color: var(--text-color);
}

.forgot-password-header p {
  color: #666;
}

.alert {
  padding: 15px;
  border-radius: 5px;
  margin-bottom: 20px;
}

.alert-danger {
  background-color: rgba(239, 71, 111, 0.1);
  color: var(--error-color);
  border: 1px solid rgba(239, 71, 111, 0.2);
}

.alert-success {
  background-color: rgba(46, 204, 113, 0.1);
  color: #2ecc71;
  border: 1px solid rgba(46, 204, 113, 0.2);
}

.forgot-password-form {
  margin-bottom: 30px;
}

.form-group {
  margin-bottom: 20px;
}

.form-group label {
  display: block;
  margin-bottom: 8px;
  font-weight: 500;
}

.form-group input {
  width: 100%;
  padding: 12px 15px;
  border: 1px solid var(--border-color);
  border-radius: 5px;
  font-size: 1rem;
  transition: border-color 0.3s ease;
}

.form-group input:focus {
  outline: none;
  border-color: var(--primary-color);
}

.btn-submit {
  width: 100%;
  padding: 14px;
  background-color: var(--primary-color);
  color: white;
  border: none;
  border-radius: 5px;
  font-size: 1rem;
  font-weight: 600;
  cursor: pointer;
  transition: background-color 0.3s ease;
}

.btn-submit:hover {
  background-color: var(--secondary-color);
}

.btn-submit:disabled {
  background-color: #ccc;
  cursor: not-allowed;
}

.forgot-password-footer {
  text-align: center;
}

.forgot-password-footer a {
  color: var(--primary-color);
  font-weight: 600;
}

@media (max-width: 480px) {
  .forgot-password-card {
    padding: 30px 20px;
  }
}
</style>
