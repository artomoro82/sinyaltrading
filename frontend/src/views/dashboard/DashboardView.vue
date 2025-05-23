<template>
  <div class="dashboard-layout">
    <aside class="sidebar" :class="{ 'sidebar-collapsed': sidebarCollapsed }">
      <div class="sidebar-header">
        <div class="logo">
          <img src="@/assets/logo.svg" alt="Fintech Platform Logo" />
          <span v-if="!sidebarCollapsed">Fintech Platform</span>
        </div>
        <button class="toggle-sidebar" @click="toggleSidebar">
          <span class="toggle-icon">≡</span>
        </button>
      </div>
      
      <div class="user-profile">
        <div class="avatar">
          <img :src="userAvatar" alt="User Avatar" />
        </div>
        <div class="user-info" v-if="!sidebarCollapsed">
          <h3>{{ userName }}</h3>
          <p>{{ userRole }}</p>
        </div>
      </div>
      
      <nav class="sidebar-nav">
        <ul>
          <li>
            <router-link to="/dashboard" exact>
              <span class="nav-icon">📊</span>
              <span class="nav-text" v-if="!sidebarCollapsed">Dashboard</span>
            </router-link>
          </li>
          <li>
            <router-link to="/dashboard/products">
              <span class="nav-icon">🛒</span>
              <span class="nav-text" v-if="!sidebarCollapsed">Products</span>
            </router-link>
          </li>
          <li>
            <router-link to="/dashboard/finance">
              <span class="nav-icon">💰</span>
              <span class="nav-text" v-if="!sidebarCollapsed">Finance</span>
            </router-link>
          </li>
          <li>
            <router-link to="/dashboard/referrals">
              <span class="nav-icon">👥</span>
              <span class="nav-text" v-if="!sidebarCollapsed">Referrals</span>
            </router-link>
          </li>
          <li>
            <router-link to="/dashboard/analytics">
              <span class="nav-icon">📈</span>
              <span class="nav-text" v-if="!sidebarCollapsed">Analytics</span>
            </router-link>
          </li>
          <li>
            <router-link to="/dashboard/academy">
              <span class="nav-icon">🎓</span>
              <span class="nav-text" v-if="!sidebarCollapsed">Academy</span>
            </router-link>
          </li>
          <li>
            <router-link to="/dashboard/community">
              <span class="nav-icon">🌐</span>
              <span class="nav-text" v-if="!sidebarCollapsed">Community</span>
            </router-link>
          </li>
          <li>
            <router-link to="/dashboard/support">
              <span class="nav-icon">🔧</span>
              <span class="nav-text" v-if="!sidebarCollapsed">Support</span>
            </router-link>
          </li>
          <li>
            <router-link to="/dashboard/settings">
              <span class="nav-icon">⚙️</span>
              <span class="nav-text" v-if="!sidebarCollapsed">Settings</span>
            </router-link>
          </li>
        </ul>
      </nav>
      
      <div class="sidebar-footer">
        <button class="logout-btn" @click="logout">
          <span class="nav-icon">🚪</span>
          <span class="nav-text" v-if="!sidebarCollapsed">Logout</span>
        </button>
      </div>
    </aside>
    
    <div class="main-content">
      <header class="dashboard-header">
        <div class="search-bar">
          <input type="text" placeholder="Search..." />
          <button class="search-btn">🔍</button>
        </div>
        
        <div class="header-actions">
          <div class="notifications">
            <button class="notification-btn" @click="toggleNotifications">
              🔔
              <span class="notification-badge" v-if="notificationCount > 0">{{ notificationCount }}</span>
            </button>
            <div class="notification-dropdown" v-if="showNotifications">
              <div class="notification-header">
                <h3>Notifications</h3>
                <button @click="markAllAsRead">Mark all as read</button>
              </div>
              <div class="notification-list">
                <div v-if="notifications.length === 0" class="empty-notifications">
                  No new notifications
                </div>
                <div v-for="(notification, index) in notifications" :key="index" class="notification-item" :class="{ 'unread': !notification.read }">
                  <div class="notification-icon" :class="notification.type">
                    {{ notificationIcon(notification.type) }}
                  </div>
                  <div class="notification-content">
                    <p>{{ notification.message }}</p>
                    <span class="notification-time">{{ notification.time }}</span>
                  </div>
                </div>
              </div>
              <div class="notification-footer">
                <router-link to="/dashboard/notifications">View all notifications</router-link>
              </div>
            </div>
          </div>
          
          <div class="user-menu">
            <button class="user-menu-btn" @click="toggleUserMenu">
              <img :src="userAvatar" alt="User Avatar" />
              <span v-if="!isMobile">{{ userName }}</span>
            </button>
            <div class="user-dropdown" v-if="showUserMenu">
              <ul>
                <li>
                  <router-link to="/dashboard/profile">
                    <span class="dropdown-icon">👤</span>
                    My Profile
                  </router-link>
                </li>
                <li>
                  <router-link to="/dashboard/settings">
                    <span class="dropdown-icon">⚙️</span>
                    Settings
                  </router-link>
                </li>
                <li>
                  <router-link to="/dashboard/support">
                    <span class="dropdown-icon">🔧</span>
                    Support
                  </router-link>
                </li>
                <li>
                  <button @click="logout">
                    <span class="dropdown-icon">🚪</span>
                    Logout
                  </button>
                </li>
              </ul>
            </div>
          </div>
        </div>
      </header>
      
      <main class="dashboard-main">
        <router-view />
      </main>
    </div>
  </div>
</template>

<script>
import { useAuthStore } from '@/store/auth'
import { mapActions, mapState } from 'pinia'

export default {
  name: 'DashboardView',
  data() {
    return {
      sidebarCollapsed: false,
      showNotifications: false,
      showUserMenu: false,
      isMobile: window.innerWidth < 768,
      notifications: [
        {
          type: 'info',
          message: 'Welcome to your dashboard! Get started by exploring our products.',
          time: '2 hours ago',
          read: false
        },
        {
          type: 'success',
          message: 'Your account has been successfully verified.',
          time: '1 day ago',
          read: false
        },
        {
          type: 'warning',
          message: 'Your subscription will expire in 7 days. Renew now to avoid interruption.',
          time: '3 days ago',
          read: true
        }
      ],
      userAvatar: 'https://ui-avatars.com/api/?name=User&background=3a86ff&color=fff'
    }
  },
  computed: {
    ...mapState(useAuthStore, ['userName', 'userRole']),
    
    notificationCount() {
      return this.notifications.filter(n => !n.read).length
    }
  },
  methods: {
    ...mapActions(useAuthStore, ['logout']),
    
    toggleSidebar() {
      this.sidebarCollapsed = !this.sidebarCollapsed
    },
    
    toggleNotifications() {
      this.showNotifications = !this.showNotifications
      this.showUserMenu = false
    },
    
    toggleUserMenu() {
      this.showUserMenu = !this.showUserMenu
      this.showNotifications = false
    },
    
    markAllAsRead() {
      this.notifications.forEach(notification => {
        notification.read = true
      })
    },
    
    notificationIcon(type) {
      switch(type) {
        case 'info': return 'ℹ️'
        case 'success': return '✅'
        case 'warning': return '⚠️'
        case 'error': return '❌'
        default: return '📢'
      }
    },
    
    handleResize() {
      this.isMobile = window.innerWidth < 768
      if (this.isMobile) {
        this.sidebarCollapsed = true
      }
    },
    
    handleClickOutside(event) {
      const notificationDropdown = document.querySelector('.notification-dropdown')
      const notificationBtn = document.querySelector('.notification-btn')
      const userDropdown = document.querySelector('.user-dropdown')
      const userMenuBtn = document.querySelector('.user-menu-btn')
      
      if (this.showNotifications && 
          notificationDropdown && 
          !notificationDropdown.contains(event.target) && 
          !notificationBtn.contains(event.target)) {
        this.showNotifications = false
      }
      
      if (this.showUserMenu && 
          userDropdown && 
          !userDropdown.contains(event.target) && 
          !userMenuBtn.contains(event.target)) {
        this.showUserMenu = false
      }
    }
  },
  mounted() {
    // Check if user is authenticated
    const authStore = useAuthStore()
    if (!authStore.isAuthenticated) {
      this.$router.push('/login')
      return
    }
    
    // Fetch user profile if needed
    if (!authStore.user) {
      authStore.fetchUserProfile()
    }
    
    // Set up event listeners
    window.addEventListener('resize', this.handleResize)
    document.addEventListener('click', this.handleClickOutside)
    
    // Initial check for mobile
    this.handleResize()
    
    document.title = 'Dashboard - Fintech Platform'
  },
  beforeUnmount() {
    window.removeEventListener('resize', this.handleResize)
    document.removeEventListener('click', this.handleClickOutside)
  }
}
</script>

<style scoped>
.dashboard-layout {
  display: flex;
  min-height: 100vh;
}

/* Sidebar Styles */
.sidebar {
  width: 260px;
  background-color: var(--dark-bg);
  color: var(--light-text);
  transition: width 0.3s ease;
  display: flex;
  flex-direction: column;
  position: fixed;
  height: 100vh;
  z-index: 100;
}

.sidebar-collapsed {
  width: 80px;
}

.sidebar-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 20px;
  border-bottom: 1px solid rgba(255, 255, 255, 0.1);
}

.logo {
  display: flex;
  align-items: center;
  gap: 10px;
}

.logo img {
  width: 30px;
  height: 30px;
}

.toggle-sidebar {
  background: none;
  border: none;
  color: var(--light-text);
  cursor: pointer;
  font-size: 1.5rem;
}

.user-profile {
  display: flex;
  align-items: center;
  gap: 15px;
  padding: 20px;
  border-bottom: 1px solid rgba(255, 255, 255, 0.1);
}

.avatar img {
  width: 40px;
  height: 40px;
  border-radius: 50%;
  object-fit: cover;
}

.user-info h3 {
  font-size: 1rem;
  margin-bottom: 5px;
}

.user-info p {
  font-size: 0.8rem;
  opacity: 0.7;
}

.sidebar-nav {
  flex: 1;
  overflow-y: auto;
  padding: 20px 0;
}

.sidebar-nav ul {
  list-style: none;
}

.sidebar-nav li {
  margin-bottom: 5px;
}

.sidebar-nav a {
  display: flex;
  align-items: center;
  gap: 15px;
  padding: 12px 20px;
  color: rgba(255, 255, 255, 0.7);
  transition: all 0.3s ease;
  border-left: 3px solid transparent;
}

.sidebar-nav a:hover,
.sidebar-nav a.router-link-active {
  background-color: rgba(255, 255, 255, 0.1);
  color: var(--light-text);
  border-left-color: var(--primary-color);
}

.nav-icon {
  font-size: 1.2rem;
  min-width: 24px;
  text-align: center;
}

.sidebar-footer {
  padding: 20px;
  border-top: 1px solid rgba(255, 255, 255, 0.1);
}

.logout-btn {
  display: flex;
  align-items: center;
  gap: 15px;
  width: 100%;
  padding: 12px;
  background: none;
  border: none;
  color: rgba(255, 255, 255, 0.7);
  cursor: pointer;
  transition: color 0.3s ease;
  text-align: left;
}

.logout-btn:hover {
  color: var(--light-text);
}

/* Main Content Styles */
.main-content {
  flex: 1;
  margin-left: 260px;
  transition: margin-left 0.3s ease;
}

.sidebar-collapsed + .main-content {
  margin-left: 80px;
}

.dashboard-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 15px 30px;
  background-color: white;
  box-shadow: 0 2px 10px rgba(0, 0, 0, 0.05);
  position: sticky;
  top: 0;
  z-index: 90;
}

.search-bar {
  display: flex;
  align-items: center;
  background-color: var(--light-bg);
  border-radius: 5px;
  padding: 8px 15px;
  width: 300px;
}

.search-bar input {
  flex: 1;
  border: none;
  background: none;
  outline: none;
  font-size: 0.9rem;
}

.search-btn {
  background: none;
  border: none;
  cursor: pointer;
}

.header-actions {
  display: flex;
  align-items: center;
  gap: 20px;
}

.notifications {
  position: relative;
}

.notification-btn {
  background: none;
  border: none;
  font-size: 1.2rem;
  cursor: pointer;
  position: relative;
}

.notification-badge {
  position: absolute;
  top: -5px;
  right: -5px;
  background-color: var(--error-color);
  color: white;
  font-size: 0.7rem;
  width: 18px;
  height: 18px;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
}

.notification-dropdown {
  position: absolute;
  top: 100%;
  right: 0;
  width: 320px;
  background-color: white;
  border-radius: 5px;
  box-shadow: 0 5px 15px rgba(0, 0, 0, 0.1);
  margin-top: 10px;
  z-index: 100;
}

.notification-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 15px;
  border-bottom: 1px solid var(--border-color);
}

.notification-header h3 {
  font-size: 1rem;
}

.notification-header button {
  background: none;
  border: none;
  color: var(--primary-color);
  font-size: 0.8rem;
  cursor: pointer;
}

.notification-list {
  max-height: 300px;
  overflow-y: auto;
}

.empty-notifications {
  padding: 20px;
  text-align: center;
  color: #666;
}

.notification-item {
  display: flex;
  gap: 15px;
  padding: 15px;
  border-bottom: 1px solid var(--border-color);
  transition: background-color 0.3s ease;
}

.notification-item:hover {
  background-color: var(--light-bg);
}

.notification-item.unread {
  background-color: rgba(58, 134, 255, 0.05);
}

.notification-icon {
  width: 40px;
  height: 40px;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 1.2rem;
}

.notification-icon.info {
  background-color: rgba(58, 134, 255, 0.1);
  color: var(--primary-color);
}

.notification-icon.success {
  background-color: rgba(6, 214, 160, 0.1);
  color: var(--success-color);
}

.notification-icon.warning {
  background-color: rgba(255, 209, 102, 0.1);
  color: var(--warning-color);
}

.notification-icon.error {
  background-color: rgba(239, 71, 111, 0.1);
  color: var(--error-color);
}

.notification-content p {
  margin-bottom: 5px;
  font-size: 0.9rem;
}

.notification-time {
  font-size: 0.8rem;
  color: #666;
}

.notification-footer {
  padding: 15px;
  text-align: center;
  border-top: 1px solid var(--border-color);
}

.notification-footer a {
  color: var(--primary-color);
  font-size: 0.9rem;
}

.user-menu {
  position: relative;
}

.user-menu-btn {
  display: flex;
  align-items: center;
  gap: 10px;
  background: none;
  border: none;
  cursor: pointer;
}

.user-menu-btn img {
  width: 35px;
  height: 35px;
  border-radius: 50%;
  object-fit: cover;
}

.user-dropdown {
  position: absolute;
  top: 100%;
  right: 0;
  width: 200px;
  background-color: white;
  border-radius: 5px;
  box-shadow: 0 5px 15px rgba(0, 0, 0, 0.1);
  margin-top: 10px;
  z-index: 100;
}

.user-dropdown ul {
  list-style: none;
}

.user-dropdown li {
  border-bottom: 1px solid var(--border-color);
}

.user-dropdown li:last-child {
  border-bottom: none;
}

.user-dropdown a,
.user-dropdown button {
  display: flex;
  align-items: center;
  gap: 10px;
  padding: 12px 15px;
  width: 100%;
  text-align: left;
  background: none;
  border: none;
  color: var(--text-color);
  cursor: pointer;
  transition: background-color 0.3s ease;
}

.user-dropdown a:hover,
.user-dropdown button:hover {
  background-color: var(--light-bg);
}

.dropdown-icon {
  font-size: 1.1rem;
}

.dashboard-main {
  padding: 30px;
  background-color: var(--light-bg);
  min-height: calc(100vh - 70px);
}

/* Responsive Styles */
@media (max-width: 992px) {
  .search-bar {
    width: 200px;
  }
}

@media (max-width: 768px) {
  .sidebar {
    width: 80px;
  }
  
  .main-content {
    margin-left: 80px;
  }
  
  .search-bar {
    width: 150px;
  }
  
  .user-menu-btn span {
    display: none;
  }
}

@media (max-width: 576px) {
  .sidebar {
    width: 0;
    transform: translateX(-100%);
  }
  
  .sidebar-collapsed {
    width: 80px;
    transform: translateX(0);
  }
  
  .main-content {
    margin-left: 0;
  }
  
  .sidebar-collapsed + .main-content {
    margin-left: 80px;
  }
  
  .dashboard-header {
    padding: 15px;
  }
  
  .search-bar {
    display: none;
  }
  
  .notification-dropdown,
  .user-dropdown {
    width: 280px;
    right: -100px;
  }
}
</style>
