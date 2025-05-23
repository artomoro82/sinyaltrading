// API Configuration
export const API_URL = process.env.NODE_ENV === 'production' 
  ? '/api' 
  : 'http://localhost:8000/api';

// Payment Gateway Configuration
export const PAYMENT_CONFIG = {
  apiUrl: `${API_URL}/payments`,
  supportedCurrencies: ['BTC', 'ETH', 'LTC', 'USDT', 'USDC'],
  defaultCurrency: 'BTC'
};

// Application Configuration
export const APP_CONFIG = {
  name: 'Fintech Platform',
  version: '1.0.0',
  supportEmail: 'support@fintechplatform.com',
  socialLinks: {
    twitter: 'https://twitter.com/fintechplatform',
    facebook: 'https://facebook.com/fintechplatform',
    linkedin: 'https://linkedin.com/company/fintechplatform'
  }
};