<template>
  <div class="profile-view">
    <h1>My Profile</h1>
    
    <div v-if="loading" class="loading-container">
      <div class="spinner"></div>
      <p>Loading profile...</p>
    </div>
    
    <div v-else-if="error" class="error-container">
      <p class="error-message">{{ error }}</p>
      <button @click="fetchProfile" class="btn btn-primary">Try Again</button>
    </div>
    
    <div v-else class="profile-container">
      <div class="profile-header">
        <div class="profile-avatar">
          <img :src="user.avatar_url || '/img/default-avatar.png'" alt="Profile Avatar" />
          <button class="change-avatar-btn">Change</button>
        </div>
        <div class="profile-info">
          <h2>{{ user.full_name }}</h2>
          <p>{{ user.email }}</p>
          <p v-if="user.phone_number">{{ user.phone_number }}</p>
          <p class="status" :class="'status-' + user.status">{{ formatStatus(user.status) }}</p>
        </div>
      </div>
      
      <div class="profile-tabs">
        <button 
          :class="{ active: activeTab === 'personal' }" 
          @click="activeTab = 'personal'"
        >
          Personal Information
        </button>
        <button 
          :class="{ active: activeTab === 'security' }" 
          @click="activeTab = 'security'"
        >
          Security
        </button>
        <button 
          :class="{ active: activeTab === 'preferences' }" 
          @click="activeTab = 'preferences'"
        >
          Preferences
        </button>
      </div>
      
      <div class="profile-content">
        <!-- Personal Information Tab -->
        <div v-if="activeTab === 'personal'" class="tab-content">
          <form @submit.prevent="updatePersonalInfo" class="profile-form">
            <div class="form-group">
              <label for="full_name">Full Name</label>
              <input 
                type="text" 
                id="full_name" 
                v-model="personalInfo.full_name" 
                required
              />
            </div>
            
            <div class="form-group">
              <label for="username">Username</label>
              <input 
                type="text" 
                id="username" 
                v-model="personalInfo.username" 
                required
              />
            </div>
            
            <div class="form-group">
              <label for="email">Email</label>
              <input 
                type="email" 
                id="email" 
                v-model="personalInfo.email" 
                required
                disabled
              />
              <small v-if="user.email_verified_at">Verified</small>
              <small v-else class="not-verified">
                Not verified 
                <button type="button" class="btn-link">Resend verification</button>
              </small>
            </div>
            
            <div class="form-group">
              <label for="phone_number">Phone Number</label>
              <input 
                type="tel" 
                id="phone_number" 
                v-model="personalInfo.phone_number"
              />
              <small v-if="user.phone_verified_at">Verified</small>
              <small v-else class="not-verified">
                Not verified 
                <button type="button" class="btn-link">Verify phone</button>
              </small>
            </div>
            
            <div class="form-actions">
              <button type="submit" class="btn btn-primary" :disabled="personalInfoLoading">
                {{ personalInfoLoading ? 'Saving...' : 'Save Changes' }}
              </button>
            </div>
          </form>
        </div>
        
        <!-- Security Tab -->
        <div v-if="activeTab === 'security'" class="tab-content">
          <form @submit.prevent="updatePassword" class="profile-form">
            <div class="form-group">
              <label for="current_password">Current Password</label>
              <input 
                type="password" 
                id="current_password" 
                v-model="securityInfo.current_password" 
                required
              />
            </div>
            
            <div class="form-group">
              <label for="new_password">New Password</label>
              <input 
                type="password" 
                id="new_password" 
                v-model="securityInfo.new_password" 
                required
              />
            </div>
            
            <div class="form-group">
              <label for="confirm_password">Confirm New Password</label>
              <input 
                type="password" 
                id="confirm_password" 
                v-model="securityInfo.confirm_password" 
                required
              />
            </div>
            
            <div class="form-actions">
              <button type="submit" class="btn btn-primary" :disabled="securityInfoLoading">
                {{ securityInfoLoading ? 'Updating...' : 'Update Password' }}
              </button>
            </div>
          </form>
          
          <div class="two-factor-section">
            <h3>Two-Factor Authentication</h3>
            <p>Enhance your account security by enabling two-factor authentication.</p>
            
            <div v-if="user.two_factor_enabled" class="two-factor-enabled">
              <p>Two-factor authentication is enabled.</p>
              <button @click="disableTwoFactor" class="btn btn-danger">Disable</button>
            </div>
            <div v-else class="two-factor-disabled">
              <p>Two-factor authentication is not enabled.</p>
              <button @click="enableTwoFactor" class="btn btn-primary">Enable</button>
            </div>
          </div>
        </div>
        
        <!-- Preferences Tab -->
        <div v-if="activeTab === 'preferences'" class="tab-content">
          <form @submit.prevent="updatePreferences" class="profile-form">
            <div class="form-group">
              <label for="language">Language</label>
              <select id="language" v-model="preferences.language">
                <option value="en">English</option>
                <option value="es">Spanish</option>
                <option value="fr">French</option>
                <option value="de">German</option>
                <option value="id">Indonesian</option>
              </select>
            </div>
            
            <div class="form-group">
              <label for="timezone">Timezone</label>
              <select id="timezone" v-model="preferences.timezone">
                <option value="UTC">UTC</option>
                <option value="America/New_York">Eastern Time (ET)</option>
                <option value="America/Chicago">Central Time (CT)</option>
                <option value="America/Denver">Mountain Time (MT)</option>
                <option value="America/Los_Angeles">Pacific Time (PT)</option>
                <option value="Asia/Jakarta">Western Indonesian Time (WIB)</option>
                <option value="Asia/Singapore">Singapore Time (SGT)</option>
              </select>
            </div>
            
            <div class="form-group">
              <label for="theme">Dashboard Theme</label>
              <select id="theme" v-model="preferences.theme">
                <option value="light">Light</option>
                <option value="dark">Dark</option>
                <option value="system">System Default</option>
              </select>
            </div>
            
            <div class="form-actions">
              <button type="submit" class="btn btn-primary" :disabled="preferencesLoading">
                {{ preferencesLoading ? 'Saving...' : 'Save Preferences' }}
              </button>
            </div>
          </form>
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
  name: 'ProfileView',
  data() {
    return {
      user: {},
      loading: true,
      error: null,
      activeTab: 'personal',
      
      personalInfo: {
        full_name: '',
        username: '',
        email: '',
        phone_number: ''
      },
      personalInfoLoading: false,
      
      securityInfo: {
        current_password: '',
        new_password: '',
        confirm_password: ''
      },
      securityInfoLoading: false,
      
      preferences: {
        language: 'en',
        timezone: 'UTC',
        theme: 'light'
      },
      preferencesLoading: false
    };
  },
  methods: {
    fetchProfile() {
      this.loading = true;
      this.error = null;
      
      axios.get(`${API_URL}/users/me/`, { headers: authHeader() })
        .then(response => {
          this.user = response.data;
          
          // Initialize form data
          this.personalInfo = {
            full_name: this.user.full_name,
            username: this.user.username,
            email: this.user.email,
            phone_number: this.user.phone_number || ''
          };
          
          this.preferences = {
            language: this.user.language_preference || 'en',
            timezone: this.user.timezone_preference || 'UTC',
            theme: this.user.dashboard_theme_preference || 'light'
          };
        })
        .catch(error => {
          this.error = error.response?.data?.error || 'Failed to load profile';
        })
        .finally(() => {
          this.loading = false;
        });
    },
    
    updatePersonalInfo() {
      this.personalInfoLoading = true;
      
      axios.patch(
        `${API_URL}/users/me/`, 
        {
          full_name: this.personalInfo.full_name,
          username: this.personalInfo.username,
          phone_number: this.personalInfo.phone_number
        },
        { headers: authHeader() }
      )
        .then(response => {
          this.user = response.data;
          this.$emit('success', 'Personal information updated successfully');
        })
        .catch(error => {
          this.$emit('error', error.response?.data?.error || 'Failed to update personal information');
        })
        .finally(() => {
          this.personalInfoLoading = false;
        });
    },
    
    updatePassword() {
      if (this.securityInfo.new_password !== this.securityInfo.confirm_password) {
        this.$emit('error', 'Passwords do not match');
        return;
      }
      
      this.securityInfoLoading = true;
      
      axios.post(
        `${API_URL}/users/change-password/`, 
        {
          current_password: this.securityInfo.current_password,
          new_password: this.securityInfo.new_password
        },
        { headers: authHeader() }
      )
        .then(() => {
          this.$emit('success', 'Password updated successfully');
          this.securityInfo = {
            current_password: '',
            new_password: '',
            confirm_password: ''
          };
        })
        .catch(error => {
          this.$emit('error', error.response?.data?.error || 'Failed to update password');
        })
        .finally(() => {
          this.securityInfoLoading = false;
        });
    },
    
    updatePreferences() {
      this.preferencesLoading = true;
      
      axios.patch(
        `${API_URL}/users/preferences/`, 
        {
          language_preference: this.preferences.language,
          timezone_preference: this.preferences.timezone,
          dashboard_theme_preference: this.preferences.theme
        },
        { headers: authHeader() }
      )
        .then(response => {
          this.user = response.data;
          this.$emit('success', 'Preferences updated successfully');
        })
        .catch(error => {
          this.$emit('error', error.response?.data?.error || 'Failed to update preferences');
        })
        .finally(() => {
          this.preferencesLoading = false;
        });
    },
    
    enableTwoFactor() {
      // This would typically open a modal with QR code and setup instructions
      this.$emit('info', 'Two-factor authentication setup will be implemented in a future update');
    },
    
    disableTwoFactor() {
      // This would typically require password confirmation
      this.$emit('info', 'Two-factor authentication removal will be implemented in a future update');
    },
    
    formatStatus(status) {
      return status.replace(/_/g, ' ').replace(/\b\w/g, l => l.toUpperCase());
    }
  },
  mounted() {
    this.fetchProfile();
  }
};
</script>

<style scoped>
.profile-view {
  padding: 20px;
}

.loading-container,
.error-container {
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

.profile-container {
  background-color: #fff;
  border-radius: 8px;
  box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
  overflow: hidden;
}

.profile-header {
  display: flex;
  padding: 20px;
  background-color: #f8f9fa;
  border-bottom: 1px solid #eee;
}

.profile-avatar {
  position: relative;
  margin-right: 20px;
}

.profile-avatar img {
  width: 100px;
  height: 100px;
  border-radius: 50%;
  object-fit: cover;
  border: 3px solid #fff;
  box-shadow: 0 2px 5px rgba(0, 0, 0, 0.1);
}

.change-avatar-btn {
  position: absolute;
  bottom: 0;
  right: 0;
  background-color: #3498db;
  color: white;
  border: none;
  border-radius: 4px;
  padding: 5px 10px;
  font-size: 0.8em;
  cursor: pointer;
}

.profile-info h2 {
  margin-top: 0;
  margin-bottom: 5px;
}

.profile-info p {
  margin: 5px 0;
}

.status {
  display: inline-block;
  padding: 3px 8px;
  border-radius: 4px;
  font-size: 0.8em;
  font-weight: bold;
}

.status-active {
  background-color: #2ecc71;
  color: white;
}

.status-inactive {
  background-color: #95a5a6;
  color: white;
}

.status-suspended {
  background-color: #e74c3c;
  color: white;
}

.status-pending_verification,
.status-kyc_pending {
  background-color: #f39c12;
  color: white;
}

.status-kyc_rejected {
  background-color: #e67e22;
  color: white;
}

.profile-tabs {
  display: flex;
  border-bottom: 1px solid #eee;
}

.profile-tabs button {
  flex: 1;
  padding: 15px;
  background-color: transparent;
  border: none;
  cursor: pointer;
  font-weight: bold;
  transition: background-color 0.3s;
}

.profile-tabs button.active {
  border-bottom: 2px solid #3498db;
  color: #3498db;
}

.profile-tabs button:hover {
  background-color: #f8f9fa;
}

.tab-content {
  padding: 20px;
}

.profile-form {
  max-width: 600px;
}

.form-group {
  margin-bottom: 20px;
}

.form-group label {
  display: block;
  margin-bottom: 5px;
  font-weight: bold;
}

.form-group input,
.form-group select {
  width: 100%;
  padding: 10px;
  border: 1px solid #ddd;
  border-radius: 4px;
}

.form-group small {
  display: block;
  margin-top: 5px;
  color: #7f8c8d;
}

.form-group small.not-verified {
  color: #e74c3c;
}

.btn-link {
  background: none;
  border: none;
  color: #3498db;
  text-decoration: underline;
  cursor: pointer;
  padding: 0;
  font-size: inherit;
}

.form-actions {
  margin-top: 30px;
}

.two-factor-section {
  margin-top: 40px;
  padding-top: 20px;
  border-top: 1px solid #eee;
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

.btn:disabled {
  opacity: 0.5;
  cursor: not-allowed;
}

@media (max-width: 768px) {
  .profile-header {
    flex-direction: column;
    align-items: center;
    text-align: center;
  }
  
  .profile-avatar {
    margin-right: 0;
    margin-bottom: 20px;
  }
  
  .profile-tabs {
    flex-direction: column;
  }
  
  .profile-tabs button {
    border-bottom: 1px solid #eee;
  }
  
  .profile-tabs button.active {
    border-bottom: 1px solid #eee;
    border-left: 2px solid #3498db;
  }
}
</style>