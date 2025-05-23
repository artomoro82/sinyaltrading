<template>
  <div class="dashboard-home">
    <div class="welcome-banner">
      <div class="welcome-content">
        <h1>Welcome back, {{ userName }}!</h1>
        <p>Here's an overview of your trading activities and platform status.</p>
      </div>
    </div>
    
    <div class="stats-overview">
      <div class="stat-card">
        <div class="stat-icon">📈</div>
        <div class="stat-content">
          <h3>Active Signals</h3>
          <p class="stat-value">{{ stats.activeSignals }}</p>
          <p class="stat-change" :class="stats.signalsChange > 0 ? 'positive' : 'negative'">
            {{ stats.signalsChange > 0 ? '+' : '' }}{{ stats.signalsChange }}% from last week
          </p>
        </div>
      </div>
      
      <div class="stat-card">
        <div class="stat-icon">🤖</div>
        <div class="stat-content">
          <h3>Active Bots</h3>
          <p class="stat-value">{{ stats.activeBots }}</p>
          <p class="stat-change" :class="stats.botsChange > 0 ? 'positive' : 'negative'">
            {{ stats.botsChange > 0 ? '+' : '' }}{{ stats.botsChange }}% from last week
          </p>
        </div>
      </div>
      
      <div class="stat-card">
        <div class="stat-icon">💰</div>
        <div class="stat-content">
          <h3>Total Profit</h3>
          <p class="stat-value">${{ stats.totalProfit.toFixed(2) }}</p>
          <p class="stat-change" :class="stats.profitChange > 0 ? 'positive' : 'negative'">
            {{ stats.profitChange > 0 ? '+' : '' }}{{ stats.profitChange }}% from last month
          </p>
        </div>
      </div>
      
      <div class="stat-card">
        <div class="stat-icon">🎯</div>
        <div class="stat-content">
          <h3>Win Rate</h3>
          <p class="stat-value">{{ stats.winRate }}%</p>
          <p class="stat-change" :class="stats.winRateChange > 0 ? 'positive' : 'negative'">
            {{ stats.winRateChange > 0 ? '+' : '' }}{{ stats.winRateChange }}% from last month
          </p>
        </div>
      </div>
    </div>
    
    <div class="dashboard-grid">
      <div class="dashboard-card recent-signals">
        <div class="card-header">
          <h2>Recent Signals</h2>
          <router-link to="/dashboard/products?type=signal" class="view-all">View All</router-link>
        </div>
        <div class="card-content">
          <table class="data-table">
            <thead>
              <tr>
                <th>Asset</th>
                <th>Type</th>
                <th>Entry Price</th>
                <th>Current Price</th>
                <th>Profit/Loss</th>
                <th>Status</th>
              </tr>
            </thead>
            <tbody>
              <tr v-for="(signal, index) in recentSignals" :key="index">
                <td>{{ signal.asset }}</td>
                <td>{{ signal.type }}</td>
                <td>${{ signal.entryPrice.toFixed(2) }}</td>
                <td>${{ signal.currentPrice.toFixed(2) }}</td>
                <td :class="signal.profitLoss > 0 ? 'positive' : 'negative'">
                  {{ signal.profitLoss > 0 ? '+' : '' }}{{ signal.profitLoss.toFixed(2) }}%
                </td>
                <td>
                  <span class="status-badge" :class="signal.status.toLowerCase()">
                    {{ signal.status }}
                  </span>
                </td>
              </tr>
            </tbody>
          </table>
        </div>
      </div>
      
      <div class="dashboard-card bot-performance">
        <div class="card-header">
          <h2>Bot Performance</h2>
          <router-link to="/dashboard/products?type=bot" class="view-all">View All</router-link>
        </div>
        <div class="card-content">
          <table class="data-table">
            <thead>
              <tr>
                <th>Bot Name</th>
                <th>Trades</th>
                <th>Win Rate</th>
                <th>Profit/Loss</th>
                <th>Status</th>
              </tr>
            </thead>
            <tbody>
              <tr v-for="(bot, index) in botPerformance" :key="index">
                <td>{{ bot.name }}</td>
                <td>{{ bot.trades }}</td>
                <td>{{ bot.winRate }}%</td>
                <td :class="bot.profitLoss > 0 ? 'positive' : 'negative'">
                  {{ bot.profitLoss > 0 ? '+' : '' }}{{ bot.profitLoss.toFixed(2) }}%
                </td>
                <td>
                  <span class="status-badge" :class="bot.status.toLowerCase()">
                    {{ bot.status }}
                  </span>
                </td>
              </tr>
            </tbody>
          </table>
        </div>
      </div>
      
      <div class="dashboard-card market-overview">
        <div class="card-header">
          <h2>Market Overview</h2>
          <div class="time-filter">
            <button 
              v-for="period in ['1D', '1W', '1M', '3M', 'YTD']" 
              :key="period"
              :class="{ active: selectedPeriod === period }"
              @click="selectedPeriod = period"
            >
              {{ period }}
            </button>
          </div>
        </div>
        <div class="card-content">
          <div class="chart-container">
            <div class="chart-placeholder">
              <!-- Chart would be rendered here with a charting library -->
              <div class="placeholder-text">Market Chart ({{ selectedPeriod }})</div>
            </div>
          </div>
          <div class="market-indicators">
            <div class="indicator" v-for="(indicator, index) in marketIndicators" :key="index">
              <div class="indicator-name">{{ indicator.name }}</div>
              <div class="indicator-value" :class="indicator.change > 0 ? 'positive' : 'negative'">
                {{ indicator.value }}
                <span class="indicator-change">
                  {{ indicator.change > 0 ? '↑' : '↓' }} {{ Math.abs(indicator.change) }}%
                </span>
              </div>
            </div>
          </div>
        </div>
      </div>
      
      <div class="dashboard-card recent-activity">
        <div class="card-header">
          <h2>Recent Activity</h2>
          <router-link to="/dashboard/activity" class="view-all">View All</router-link>
        </div>
        <div class="card-content">
          <div class="activity-list">
            <div class="activity-item" v-for="(activity, index) in recentActivity" :key="index">
              <div class="activity-icon" :class="activity.type">
                {{ activityIcon(activity.type) }}
              </div>
              <div class="activity-content">
                <p class="activity-message">{{ activity.message }}</p>
                <p class="activity-time">{{ activity.time }}</p>
              </div>
            </div>
          </div>
        </div>
      </div>
      
      <div class="dashboard-card upcoming-events">
        <div class="card-header">
          <h2>Upcoming Events</h2>
          <router-link to="/dashboard/events" class="view-all">View All</router-link>
        </div>
        <div class="card-content">
          <div class="events-list">
            <div class="event-item" v-for="(event, index) in upcomingEvents" :key="index">
              <div class="event-date">
                <div class="event-month">{{ event.month }}</div>
                <div class="event-day">{{ event.day }}</div>
              </div>
              <div class="event-content">
                <h3 class="event-title">{{ event.title }}</h3>
                <p class="event-description">{{ event.description }}</p>
                <div class="event-time">{{ event.time }}</div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { useAuthStore } from '@/store/auth'
import { mapState } from 'pinia'

export default {
  name: 'DashboardHomeView',
  data() {
    return {
      selectedPeriod: '1W',
      stats: {
        activeSignals: 12,
        signalsChange: 8.5,
        activeBots: 3,
        botsChange: -2.1,
        totalProfit: 1284.75,
        profitChange: 15.3,
        winRate: 68,
        winRateChange: 3.2
      },
      recentSignals: [
        { asset: 'BTC/USD', type: 'Long', entryPrice: 48250.00, currentPrice: 51320.50, profitLoss: 6.36, status: 'Active' },
        { asset: 'ETH/USD', type: 'Long', entryPrice: 3120.75, currentPrice: 3350.25, profitLoss: 7.35, status: 'Active' },
        { asset: 'XRP/USD', type: 'Short', entryPrice: 0.85, currentPrice: 0.79, profitLoss: 7.06, status: 'Active' },
        { asset: 'ADA/USD', type: 'Long', entryPrice: 1.25, currentPrice: 1.18, profitLoss: -5.60, status: 'Active' },
        { asset: 'SOL/USD', type: 'Long', entryPrice: 105.50, currentPrice: 112.75, profitLoss: 6.87, status: 'Active' }
      ],
      botPerformance: [
        { name: 'BTC Trend Follower', trades: 28, winRate: 71, profitLoss: 12.5, status: 'Running' },
        { name: 'ETH Scalper', trades: 156, winRate: 65, profitLoss: 8.3, status: 'Running' },
        { name: 'Multi-Asset Bot', trades: 42, winRate: 59, profitLoss: -2.1, status: 'Paused' }
      ],
      marketIndicators: [
        { name: 'BTC/USD', value: '$51,320.50', change: 2.1 },
        { name: 'ETH/USD', value: '$3,350.25', change: 1.8 },
        { name: 'S&P 500', value: '4,782.25', change: -0.3 },
        { name: 'Gold', value: '$1,876.40', change: 0.5 }
      ],
      recentActivity: [
        { type: 'signal', message: 'New signal: BTC/USD Long at $48,250.00', time: '2 hours ago' },
        { type: 'bot', message: 'ETH Scalper executed 5 trades with 80% win rate', time: '5 hours ago' },
        { type: 'system', message: 'Your subscription has been renewed successfully', time: '1 day ago' },
        { type: 'transaction', message: 'Withdrawal of $500 has been processed', time: '2 days ago' }
      ],
      upcomingEvents: [
        { month: 'May', day: '25', title: 'Crypto Market Webinar', description: 'Learn about the latest trends in cryptocurrency markets', time: '3:00 PM UTC' },
        { month: 'May', day: '28', title: 'Bot Strategy Workshop', description: 'Advanced strategies for automated trading', time: '5:00 PM UTC' },
        { month: 'Jun', day: '02', title: 'Platform Maintenance', description: 'Scheduled maintenance window, services may be unavailable', time: '1:00 AM - 3:00 AM UTC' }
      ]
    }
  },
  computed: {
    ...mapState(useAuthStore, ['userName'])
  },
  methods: {
    activityIcon(type) {
      switch(type) {
        case 'signal': return '📈'
        case 'bot': return '🤖'
        case 'system': return '⚙️'
        case 'transaction': return '💰'
        default: return '📋'
      }
    }
  },
  mounted() {
    document.title = 'Dashboard - Fintech Platform'
  }
}
</script>

<style scoped>
.dashboard-home {
  width: 100%;
}

.welcome-banner {
  background: linear-gradient(135deg, var(--primary-color) 0%, var(--secondary-color) 100%);
  color: white;
  border-radius: 10px;
  padding: 30px;
  margin-bottom: 30px;
}

.welcome-content h1 {
  font-size: 1.8rem;
  margin-bottom: 10px;
}

.welcome-content p {
  opacity: 0.9;
}

.stats-overview {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(240px, 1fr));
  gap: 20px;
  margin-bottom: 30px;
}

.stat-card {
  background-color: white;
  border-radius: 10px;
  padding: 20px;
  display: flex;
  align-items: center;
  box-shadow: 0 2px 10px rgba(0, 0, 0, 0.05);
}

.stat-icon {
  font-size: 2rem;
  margin-right: 15px;
  background-color: rgba(58, 134, 255, 0.1);
  width: 60px;
  height: 60px;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
}

.stat-content h3 {
  font-size: 0.9rem;
  color: #666;
  margin-bottom: 5px;
}

.stat-value {
  font-size: 1.5rem;
  font-weight: 700;
  margin-bottom: 5px;
}

.stat-change {
  font-size: 0.8rem;
}

.positive {
  color: var(--success-color);
}

.negative {
  color: var(--error-color);
}

.dashboard-grid {
  display: grid;
  grid-template-columns: repeat(2, 1fr);
  gap: 20px;
}

.dashboard-card {
  background-color: white;
  border-radius: 10px;
  box-shadow: 0 2px 10px rgba(0, 0, 0, 0.05);
  overflow: hidden;
  margin-bottom: 20px;
}

.recent-signals, .bot-performance, .market-overview {
  grid-column: span 2;
}

.card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 20px;
  border-bottom: 1px solid var(--border-color);
}

.card-header h2 {
  font-size: 1.2rem;
  font-weight: 600;
}

.view-all {
  color: var(--primary-color);
  font-size: 0.9rem;
  font-weight: 500;
}

.card-content {
  padding: 20px;
}

.data-table {
  width: 100%;
  border-collapse: collapse;
}

.data-table th, .data-table td {
  padding: 12px 15px;
  text-align: left;
}

.data-table th {
  background-color: var(--light-bg);
  font-weight: 600;
  font-size: 0.9rem;
}

.data-table tr {
  border-bottom: 1px solid var(--border-color);
}

.data-table tr:last-child {
  border-bottom: none;
}

.status-badge {
  display: inline-block;
  padding: 5px 10px;
  border-radius: 20px;
  font-size: 0.8rem;
  font-weight: 500;
}

.status-badge.active, .status-badge.running {
  background-color: rgba(6, 214, 160, 0.1);
  color: var(--success-color);
}

.status-badge.paused {
  background-color: rgba(255, 209, 102, 0.1);
  color: var(--warning-color);
}

.status-badge.stopped, .status-badge.failed {
  background-color: rgba(239, 71, 111, 0.1);
  color: var(--error-color);
}

.time-filter {
  display: flex;
  gap: 5px;
}

.time-filter button {
  background: none;
  border: 1px solid var(--border-color);
  border-radius: 5px;
  padding: 5px 10px;
  font-size: 0.8rem;
  cursor: pointer;
  transition: all 0.3s ease;
}

.time-filter button.active {
  background-color: var(--primary-color);
  color: white;
  border-color: var(--primary-color);
}

.chart-container {
  height: 300px;
  margin-bottom: 20px;
}

.chart-placeholder {
  width: 100%;
  height: 100%;
  background-color: var(--light-bg);
  border-radius: 5px;
  display: flex;
  align-items: center;
  justify-content: center;
}

.placeholder-text {
  color: #666;
  font-style: italic;
}

.market-indicators {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(150px, 1fr));
  gap: 15px;
}

.indicator {
  padding: 10px;
  border-radius: 5px;
  background-color: var(--light-bg);
}

.indicator-name {
  font-size: 0.9rem;
  margin-bottom: 5px;
  color: #666;
}

.indicator-value {
  font-size: 1.1rem;
  font-weight: 600;
}

.indicator-change {
  font-size: 0.8rem;
  margin-left: 5px;
}

.activity-list {
  display: flex;
  flex-direction: column;
  gap: 15px;
}

.activity-item {
  display: flex;
  gap: 15px;
  padding-bottom: 15px;
  border-bottom: 1px solid var(--border-color);
}

.activity-item:last-child {
  border-bottom: none;
  padding-bottom: 0;
}

.activity-icon {
  width: 40px;
  height: 40px;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 1.2rem;
}

.activity-icon.signal {
  background-color: rgba(58, 134, 255, 0.1);
  color: var(--primary-color);
}

.activity-icon.bot {
  background-color: rgba(131, 56, 236, 0.1);
  color: var(--secondary-color);
}

.activity-icon.system {
  background-color: rgba(255, 209, 102, 0.1);
  color: var(--warning-color);
}

.activity-icon.transaction {
  background-color: rgba(6, 214, 160, 0.1);
  color: var(--success-color);
}

.activity-message {
  margin-bottom: 5px;
}

.activity-time {
  font-size: 0.8rem;
  color: #666;
}

.events-list {
  display: flex;
  flex-direction: column;
  gap: 15px;
}

.event-item {
  display: flex;
  gap: 15px;
  padding-bottom: 15px;
  border-bottom: 1px solid var(--border-color);
}

.event-item:last-child {
  border-bottom: none;
  padding-bottom: 0;
}

.event-date {
  min-width: 50px;
  text-align: center;
  border-radius: 5px;
  overflow: hidden;
}

.event-month {
  background-color: var(--primary-color);
  color: white;
  padding: 3px 0;
  font-size: 0.8rem;
  text-transform: uppercase;
}

.event-day {
  background-color: white;
  border: 1px solid var(--primary-color);
  border-top: none;
  padding: 5px 0;
  font-size: 1.2rem;
  font-weight: 700;
}

.event-title {
  font-size: 1rem;
  font-weight: 600;
  margin-bottom: 5px;
}

.event-description {
  font-size: 0.9rem;
  color: #666;
  margin-bottom: 5px;
}

.event-time {
  font-size: 0.8rem;
  color: #666;
}

@media (max-width: 992px) {
  .dashboard-grid {
    grid-template-columns: 1fr;
  }
  
  .recent-signals, .bot-performance, .market-overview {
    grid-column: span 1;
  }
}

@media (max-width: 768px) {
  .stats-overview {
    grid-template-columns: repeat(2, 1fr);
  }
  
  .data-table {
    font-size: 0.9rem;
  }
}

@media (max-width: 576px) {
  .stats-overview {
    grid-template-columns: 1fr;
  }
  
  .data-table {
    display: block;
    overflow-x: auto;
  }
}
</style>
