<template>
  <div id="app">
    <header>
      <nav class="main-nav">
        <div class="container">
          <div class="logo">
            <router-link to="/">
              <img src="@/assets/logo.svg" alt="Fintech Platform Logo" />
            </router-link>
          </div>
          <div class="nav-links">
            <router-link to="/products">Products</router-link>
            <router-link to="/solutions">Solutions</router-link>
            <router-link to="/pricing">Pricing</router-link>
            <router-link to="/education">Education</router-link>
            <router-link to="/community">Community</router-link>
          </div>
          <div class="auth-links">
            <router-link to="/login" class="login-btn">Login</router-link>
            <router-link to="/register" class="register-btn">Sign Up Free</router-link>
          </div>
        </div>
      </nav>
    </header>

    <main>
      <router-view />
    </main>

    <footer>
      <div class="container">
        <div class="footer-grid">
          <div class="footer-column">
            <h3>Company</h3>
            <ul>
              <li><router-link to="/about">About Us</router-link></li>
              <li><router-link to="/careers">Careers</router-link></li>
              <li><router-link to="/press">Press</router-link></li>
              <li><router-link to="/contact">Contact</router-link></li>
            </ul>
          </div>
          <div class="footer-column">
            <h3>Legal</h3>
            <ul>
              <li><router-link to="/terms">Terms of Service</router-link></li>
              <li><router-link to="/privacy">Privacy Policy</router-link></li>
              <li><router-link to="/cookies">Cookie Policy</router-link></li>
              <li><router-link to="/disclaimer">Disclaimer</router-link></li>
            </ul>
          </div>
          <div class="footer-column">
            <h3>Resources</h3>
            <ul>
              <li><router-link to="/blog">Blog</router-link></li>
              <li><router-link to="/documentation">Documentation</router-link></li>
              <li><router-link to="/status">Status Page</router-link></li>
              <li><router-link to="/sitemap">Sitemap</router-link></li>
            </ul>
          </div>
          <div class="footer-column">
            <h3>Connect</h3>
            <div class="social-links">
              <a href="#" target="_blank"><i class="icon-twitter"></i></a>
              <a href="#" target="_blank"><i class="icon-facebook"></i></a>
              <a href="#" target="_blank"><i class="icon-linkedin"></i></a>
              <a href="#" target="_blank"><i class="icon-instagram"></i></a>
            </div>
            <div class="newsletter">
              <h4>Subscribe to our newsletter</h4>
              <form @submit.prevent="subscribeNewsletter">
                <input type="email" placeholder="Your email" v-model="newsletterEmail" required />
                <button type="submit">Subscribe</button>
              </form>
            </div>
          </div>
        </div>
        <div class="footer-bottom">
          <p>&copy; {{ new Date().getFullYear() }} Fintech Platform. All rights reserved.</p>
        </div>
      </div>
    </footer>
  </div>
</template>

<script>
export default {
  name: 'App',
  data() {
    return {
      newsletterEmail: ''
    }
  },
  methods: {
    subscribeNewsletter() {
      // TODO: Implement newsletter subscription
      console.log('Newsletter subscription for:', this.newsletterEmail);
      this.newsletterEmail = '';
      // Show success message
    }
  }
}
</script>

<style>
/* Global styles */
:root {
  --primary-color: #3a86ff;
  --secondary-color: #8338ec;
  --accent-color: #ff006e;
  --text-color: #333;
  --light-text: #fff;
  --dark-bg: #1a1a2e;
  --light-bg: #f8f9fa;
  --border-color: #e0e0e0;
  --success-color: #06d6a0;
  --warning-color: #ffd166;
  --error-color: #ef476f;
}

* {
  margin: 0;
  padding: 0;
  box-sizing: border-box;
}

body {
  font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Oxygen, Ubuntu, Cantarell, 'Open Sans', 'Helvetica Neue', sans-serif;
  color: var(--text-color);
  line-height: 1.6;
  font-size: 16px;
}

.container {
  width: 100%;
  max-width: 1200px;
  margin: 0 auto;
  padding: 0 20px;
}

a {
  text-decoration: none;
  color: var(--primary-color);
  transition: color 0.3s ease;
}

a:hover {
  color: var(--secondary-color);
}

/* Header styles */
header {
  background-color: #fff;
  box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
  position: sticky;
  top: 0;
  z-index: 100;
}

.main-nav {
  padding: 15px 0;
}

.main-nav .container {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.logo img {
  height: 40px;
}

.nav-links {
  display: flex;
  gap: 30px;
}

.nav-links a {
  color: var(--text-color);
  font-weight: 500;
}

.nav-links a:hover,
.nav-links a.router-link-active {
  color: var(--primary-color);
}

.auth-links {
  display: flex;
  gap: 15px;
  align-items: center;
}

.login-btn {
  color: var(--primary-color);
  font-weight: 600;
}

.register-btn {
  background-color: var(--primary-color);
  color: white;
  padding: 10px 20px;
  border-radius: 5px;
  font-weight: 600;
  transition: background-color 0.3s ease;
}

.register-btn:hover {
  background-color: var(--secondary-color);
  color: white;
}

/* Main content area */
main {
  min-height: calc(100vh - 200px);
}

/* Footer styles */
footer {
  background-color: var(--dark-bg);
  color: var(--light-text);
  padding: 60px 0 30px;
}

.footer-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
  gap: 40px;
  margin-bottom: 40px;
}

.footer-column h3 {
  font-size: 18px;
  margin-bottom: 20px;
  color: var(--light-text);
}

.footer-column ul {
  list-style: none;
}

.footer-column ul li {
  margin-bottom: 10px;
}

.footer-column ul li a {
  color: rgba(255, 255, 255, 0.7);
  transition: color 0.3s ease;
}

.footer-column ul li a:hover {
  color: var(--light-text);
}

.social-links {
  display: flex;
  gap: 15px;
  margin-bottom: 20px;
}

.social-links a {
  display: flex;
  align-items: center;
  justify-content: center;
  width: 40px;
  height: 40px;
  background-color: rgba(255, 255, 255, 0.1);
  border-radius: 50%;
  color: var(--light-text);
  transition: background-color 0.3s ease;
}

.social-links a:hover {
  background-color: var(--primary-color);
}

.newsletter h4 {
  font-size: 16px;
  margin-bottom: 15px;
}

.newsletter form {
  display: flex;
}

.newsletter input {
  flex: 1;
  padding: 10px 15px;
  border: none;
  border-radius: 5px 0 0 5px;
  outline: none;
}

.newsletter button {
  background-color: var(--primary-color);
  color: white;
  border: none;
  padding: 10px 15px;
  border-radius: 0 5px 5px 0;
  cursor: pointer;
  transition: background-color 0.3s ease;
}

.newsletter button:hover {
  background-color: var(--secondary-color);
}

.footer-bottom {
  text-align: center;
  padding-top: 30px;
  border-top: 1px solid rgba(255, 255, 255, 0.1);
  color: rgba(255, 255, 255, 0.5);
}

/* Responsive styles */
@media (max-width: 768px) {
  .main-nav .container {
    flex-direction: column;
    gap: 20px;
  }
  
  .nav-links {
    width: 100%;
    justify-content: space-between;
  }
  
  .auth-links {
    width: 100%;
    justify-content: space-between;
  }
  
  .footer-grid {
    grid-template-columns: 1fr 1fr;
  }
}

@media (max-width: 480px) {
  .nav-links {
    flex-direction: column;
    gap: 15px;
    align-items: center;
  }
  
  .footer-grid {
    grid-template-columns: 1fr;
  }
}
</style>
