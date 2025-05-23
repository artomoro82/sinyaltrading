<template>
  <div class="register-page">
    <div class="register-container">
      <div class="register-card">
        <div class="register-header">
          <h1>Create Your Account</h1>
          <p>Join our platform and start your trading journey today.</p>
        </div>
        
        <div v-if="error" class="alert alert-danger">
          {{ error }}
        </div>
        
        <form @submit.prevent="handleRegister" class="register-form">
          <div class="form-group">
            <label for="username">Username</label>
            <input 
              type="text" 
              id="username" 
              v-model="username" 
              required 
              placeholder="Choose a username"
              :disabled="loading"
            />
          </div>
          
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
            <label for="fullName">Full Name</label>
            <input 
              type="text" 
              id="fullName" 
              v-model="fullName" 
              required 
              placeholder="Enter your full name"
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
                placeholder="Create a password"
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
            <div class="password-strength" v-if="password">
              <div class="strength-meter">
                <div 
                  class="strength-value" 
                  :style="{ width: passwordStrength + '%', backgroundColor: strengthColor }"
                ></div>
              </div>
              <span>{{ strengthText }}</span>
            </div>
          </div>
          
          <div class="form-group">
            <label for="confirmPassword">Confirm Password</label>
            <input 
              :type="showConfirmPassword ? 'text' : 'password'" 
              id="confirmPassword" 
              v-model="confirmPassword" 
              required 
              placeholder="Confirm your password"
              :disabled="loading"
            />
            <button 
              type="button" 
              class="toggle-password" 
              @click="showConfirmPassword = !showConfirmPassword"
            >
              {{ showConfirmPassword ? 'Hide' : 'Show' }}
            </button>
            <div v-if="password && confirmPassword && password !== confirmPassword" class="password-mismatch">
              Passwords do not match
            </div>
          </div>
          
          <div class="form-group terms">
            <input type="checkbox" id="terms" v-model="agreeToTerms" required />
            <label for="terms">I agree to the <router-link to="/terms">Terms of Service</router-link> and <router-link to="/privacy">Privacy Policy</router-link></label>
          </div>
          
          <button 
            type="submit" 
            class="btn-register" 
            :disabled="loading || !agreeToTerms || (password !== confirmPassword) || !isPasswordStrong"
          >
            {{ loading ? 'Creating Account...' : 'Create Account' }}
          </button>
        </form>
        
        <div class="social-register">
          <p>Or sign up with</p>
          <div class="social-buttons">
            <button class="btn-social btn-google" @click="socialRegister('google')">
              <span class="icon">G</span>
              Google
            </button>
            <button class="btn-social btn-facebook" @click="socialRegister('facebook')">
              <span class="icon">f</span>
              Facebook
            </button>
          </div>
        </div>
        
        <div class="register-footer">
          <p>Already have an account? <router-link to="/login">Login</router-link></p>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { useAuthStore } from '@/store/auth'
import { mapActions } from 'pinia'

export default {
  name: 'RegisterView',
  data() {
    return {
      username: '',
      email: '',
      fullName: '',
      password: '',
      confirmPassword: '',
      showPassword: false,
      showConfirmPassword: false,
      agreeToTerms: false,
      loading: false,
      error: null
    }
  },
  computed: {
    passwordStrength() {
      if (!this.password) return 0
      
      let strength = 0
      
      // Length check
      if (this.password.length >= 8) strength += 25
      
      // Contains lowercase
      if (/[a-z]/.test(this.password)) strength += 25
      
      // Contains uppercase
      if (/[A-Z]/.test(this.password)) strength += 25
      
      // Contains number or special char
      if (/[0-9!@#$%^&*(),.?":{}|<>]/.test(this.password)) strength += 25
      
      return strength
    },
    strengthColor() {
      if (this.passwordStrength < 50) return '#ef476f'
      if (this.passwordStrength < 75) return '#ffd166'
      return '#06d6a0'
    },
    strengthText() {
      if (this.passwordStrength < 50) return 'Weak'
      if (this.passwordStrength < 75) return 'Medium'
      return 'Strong'
    },
    isPasswordStrong() {
      return this.passwordStrength >= 75
    }
  },
  methods: {
    ...mapActions(useAuthStore, ['register']),
    
    async handleRegister() {
      if (this.password !== this.confirmPassword) {
        this.error = 'Passwords do not match'
        return
      }
      
      if (!this.isPasswordStrong) {
        this.error = 'Please use a stronger password'
        return
      }
      
      this.loading = true
      this.error = null
      
      try {
        await this.register({
          username: this.username,
          email: this.email,
          full_name: this.fullName,
          password: this.password,
          password_confirm: this.confirmPassword
        })
        
        // Redirect to dashboard
        this.$router.push('/dashboard')
      } catch (error) {
        this.error = error.response?.data || 'Registration failed. Please try again.'
        console.error('Registration error:', error)
      } finally {
        this.loading = false
      }
    },
    
    socialRegister(provider) {
      // This would typically redirect to OAuth provider
      alert(`${provider} registration is not implemented in this demo.`)
    }
  },
  mounted() {
    // Check if user is already logged in
    const authStore = useAuthStore()
    if (authStore.isAuthenticated) {
      this.$router.push('/dashboard')
    }
    
    document.title = 'Register - Fintech Platform'
  }
}
</script>

<style scoped>
.register-page {
  min-height: 100vh;
  display: flex;
  align-items: center;
  justify-content: center;
  background-color: var(--light-bg);
  padding: 40px 20px;
}

.register-container {
  width: 100%;
  max-width: 580px;
}

.register-card {
  background-color: white;
  border-radius: 10px;
  box-shadow: 0 5px 20px rgba(0, 0, 0, 0.1);
  padding: 40px;
}

.register-header {
  text-align: center;
  margin-bottom: 30px;
}

.register-header h1 {
  font-size: 2rem;
  font-weight: 700;
  margin-bottom: 10px;
  color: var(--text-color);
}

.register-header p {
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

.register-form {
  margin-bottom: 30px;
}

.form-group {
  margin-bottom: 20px;
  position: relative;
}

.form-group label {
  display: block;
  margin-bottom: 8px;
  font-weight: 500;
}

.form-group input[type="text"],
.form-group input[type="email"],
.form-group input[type="password"] {
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

.password-strength {
  margin-top: 10px;
}

.strength-meter {
  height: 5px;
  background-color: #eee;
  border-radius: 3px;
  margin-bottom: 5px;
}

.strength-value {
  height: 100%;
  border-radius: 3px;
  transition: width 0.3s ease, background-color 0.3s ease;
}

.password-mismatch {
  color: var(--error-color);
  font-size: 0.9rem;
  margin-top: 5px;
}

.terms {
  display: flex;
  align-items: flex-start;
}

.terms input {
  margin-right: 10px;
  margin-top: 5px;
}

.terms label {
  font-size: 0.9rem;
  line-height: 1.4;
}

.btn-register {
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

.btn-register:hover:not(:disabled) {
  background-color: var(--secondary-color);
}

.btn-register:disabled {
  background-color: #ccc;
  cursor: not-allowed;
}

.social-register {
  text-align: center;
  margin-bottom: 30px;
}

.social-register p {
  position: relative;
  margin-bottom: 20px;
  color: #666;
}

.social-register p:before,
.social-register p:after {
  content: '';
  position: absolute;
  top: 50%;
  width: 30%;
  height: 1px;
  background-color: var(--border-color);
}

.social-register p:before {
  left: 0;
}

.social-register p:after {
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

.register-footer {
  text-align: center;
}

.register-footer a {
  color: var(--primary-color);
  font-weight: 600;
}

@media (max-width: 480px) {
  .register-card {
    padding: 30px 20px;
  }
  
  .social-buttons {
    flex-direction: column;
  }
}
</style>
