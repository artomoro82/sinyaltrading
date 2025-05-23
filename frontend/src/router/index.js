import { createRouter, createWebHistory } from 'vue-router'
import HomeView from '../views/HomeView.vue'

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/',
      name: 'home',
      component: HomeView
    },
    {
      path: '/products',
      name: 'products',
      component: () => import('../views/ProductsView.vue')
    },
    {
      path: '/solutions',
      name: 'solutions',
      component: () => import('../views/solutions/SolutionsView.vue')
    },
    {
      path: '/pricing',
      name: 'pricing',
      component: () => import('../views/pricing/PricingView.vue')
    },
    {
      path: '/education',
      name: 'education',
      component: () => import('../views/education/EducationView.vue')
    },
    {
      path: '/community',
      name: 'community',
      component: () => import('../views/community/CommunityView.vue')
    },
    {
      path: '/about',
      name: 'about',
      component: () => import('../views/about/AboutView.vue')
    },
    {
      path: '/login',
      name: 'login',
      component: () => import('../views/LoginView.vue')
    },
    {
      path: '/register',
      name: 'register',
      component: () => import('../views/RegisterView.vue')
    },
    {
      path: '/forgot-password',
      name: 'forgot-password',
      component: () => import('../views/ForgotPasswordView.vue')
    },
    {
      path: '/dashboard',
      name: 'dashboard',
      component: () => import('../views/dashboard/DashboardView.vue'),
      meta: { requiresAuth: true },
      children: [
        {
          path: '',
          name: 'dashboard-home',
          component: () => import('../views/dashboard/DashboardHomeView.vue')
        }
      ]
    }
  ]
})

// Navigation guards
router.beforeEach((to, from, next) => {
  const isAuthenticated = localStorage.getItem('token') ? true : false
  const userRole = localStorage.getItem('userRole')

  if (to.matched.some(record => record.meta.requiresAuth) && !isAuthenticated) {
    next({ name: 'login', query: { redirect: to.fullPath } })
  } else if (to.matched.some(record => record.meta.requiresAdmin) && userRole !== 'admin') {
    next({ name: 'dashboard' })
  } else {
    next()
  }
})

export default router
