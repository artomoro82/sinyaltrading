<template>
  <div class="login-page">
    <div class="login-container">
      <div class="login-card">
        <div class="login-header">
          <h1>Login to Your Account</h1>
          <p>Welcome back! Please enter your credentials to continue.</p>
        </div>
        
        <div v-if="error" class="alert alert-danger">
          {{ error }}
        </div>
        
        <form @submit.prevent="handleLogin" class="login-form">
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
          
          <div class="form-group">
            <label for="password">Password</label>
            <div class="password-input">
              <input 
                :type="showPassword ? 'text' : 'password'" 
                id="password" 
                v-model="password" 
                required 
                placeholder="Enter your password"
                :disabled="loading"
              />
              <button 
                type="button" 
                class="toggle-password" 
                @click="showPassword = !showPassword"
              >
                {{ showPassword ? 'Hide' : 'Show' }}
              </button>
            </div>
          </div>
          
          <div class="form-options">
            <div class="remember-me">
              <input type="checkbox" id="remember" v-model="rememberMe" />
              <label for="remember">Remember me</label>
            </div>
            <router-link to="/forgot-password" class="forgot-password">Forgot password?</router-link>
          </div>
          
          <button type="submit" class="btn-login" :disabled="loading">
            {{ loading ? 'Logging in...' : 'Login' }}
          </button>
        </form>
        
        <div class="social-login">
          <p>Or login with</p>
          <div class="social-buttons">
            <button class="btn-social btn-google" @click="socialLogin('google')">
              <span class="icon">G</span>
              Google
            </button>
            <button class="btn-social btn-facebook" @click="socialLogin('facebook')">
              <span class="icon">f</span>
              Facebook
            </button>
          </div>
        </div>
        
        <div class="login-footer">
          <p>Don't have an account? <router-link to="/register">Sign up</router-link></p>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { useAuthStore } from '@/store/auth'
import { mapActions } from 'pinia'

export default {
  name: 'LoginView',
  data() {
    return {
      email: '',
      password: '',
      rememberMe: false,
      showPassword: false,
      loading: false,
      error: null
    }
  },
  methods: {
    ...mapActions(useAuthStore, ['login']),
    
    async handleLogin() {
      this.loading = true
      this.error = null
      
      try {
        await this.login({
          email: this.email,
          password: this.password
        })
        
        // Store remember me preference
        if (this.rememberMe) {
          localStorage.setItem('rememberMe', 'true')
        } else {
          localStorage.removeItem('rememberMe')
        }
        
        // Redirect to dashboard or intended page
        const redirectPath = this.$route.query.redirect || '/dashboard'
        this.$router.push(redirectPath)
      } catch (error) {
        this.error = error.response?.data?.error || 'Login failed. Please check your credentials and try again.'
        console.error('Login error:', error)
      } finally {
        this.loading = false
      }
    },
    
    socialLogin(provider) {
      // This would typically redirect to OAuth provider
      alert(`${provider} login is not implemented in this demo.`)
    }
  },
  mounted() {
    // Check if user is already logged in
    const authStore = useAuthStore()
    if (authStore.isAuthenticated) {
      this.$router.push('/dashboard')
    }
    
    // Check for remember me
    if (localStorage.getItem('rememberMe') === 'true') {
      this.rememberMe = true
    }
    
    document.title = 'Login - Fintech Platform'
  }
}
</script>

<style scoped>
.login-page {
  min-height: 100vh;
  display: flex;
  align-items: center;
  justify-content: center;
  background-color: var(--light-bg);
  padding: 40px 20px;
}

.login-container {
  width: 100%;
  max-width: 480px;
}

.login-card {
  background-color: white;
  border-radius: 10px;
  box-shadow: 0 5px 20px rgba(0, 0, 0, 0.1);
  padding: 40px;
}

.login-header {
  text-align: center;
  margin-bottom: 30px;
}

.login-header h1 {
  font-size: 2rem;
  font-weight: 700;
  margin-bottom: 10px;
  color: var(--text-color);
}

.login-header p {
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

.login-form {
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

.password-input {
  position: relative;
}

.toggle-password {
  position: absolute;
  right: 15px;
  top: 50%;
  transform: translateY(-50%);
  background: none;
  border: none;
  color: #666;
  cursor: pointer;
  font-size: 0.9rem;
}

.form-options {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 25px;
}

.remember-me {
  display: flex;
  align-items: center;
}

.remember-me input {
  margin-right: 8px;
}

.forgot-password {
  color: var(--primary-color);
  font-size: 0.9rem;
}

.btn-login {
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

.btn-login:hover {
  background-color: var(--secondary-color);
}

.btn-login:disabled {
  background-color: #ccc;
  cursor: not-allowed;
}

.social-login {
  text-align: center;
  margin-bottom: 30px;
}

.social-login p {
  position: relative;
  margin-bottom: 20px;
  color: #666;
}

.social-login p:before,
.social-login p:after {
  content: '';
  position: absolute;
  top: 50%;
  width: 30%;
  height: 1px;
  background-color: var(--border-color);
}

.social-login p:before {
  left: 0;
}

.social-login p:after {
  right: 0;
}

.social-buttons {
  display: flex;
  gap: 15px;
}

.btn-social {
  flex: 1;
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 12px;
  border: 1px solid var(--border-color);
  border-radius: 5px;
  background-color: white;
  cursor: pointer;
  transition: background-color 0.3s ease;
}

.btn-social:hover {
  background-color: var(--light-bg);
}

.btn-google .icon {
  color: #DB4437;
}

.btn-facebook .icon {
  color: #4267B2;
}

.icon {
  margin-right: 8px;
  font-weight: bold;
}

.login-footer {
  text-align: center;
}

.login-footer a {
  color: var(--primary-color);
  font-weight: 600;
}

@media (max-width: 480px) {
  .login-card {
    padding: 30px 20px;
  }
  
  .social-buttons {
    flex-direction: column;
  }
}
</style>
