import axios from 'axios';
import authHeader from './auth-header';
import { API_URL } from './config';

class PaymentService {
  /**
   * Create a payment for an order
   * @param {string} orderId - The order ID
   * @returns {Promise} - The payment data
   */
  createPayment(orderId) {
    return axios.post(
      `${API_URL}/payments/create/`,
      { order_id: orderId },
      { headers: authHeader() }
    );
  }

  /**
   * Get the status of a payment
   * @param {string} paymentId - The payment ID
   * @returns {Promise} - The payment status
   */
  getPaymentStatus(paymentId) {
    return axios.get(
      `${API_URL}/payments/${paymentId}/status/`,
      { headers: authHeader() }
    );
  }

  /**
   * Process a payment using the payment gateway
   * @param {Object} paymentData - The payment data from the backend
   * @returns {Promise} - A promise that resolves when the payment is complete
   */
  processPayment(paymentData) {
    // This function will handle the redirect to the payment gateway
    // or display a payment form depending on the gateway's requirements
    
    if (paymentData && paymentData.gateway_data) {
      const { gateway_data } = paymentData;
      
      // If the gateway provides a payment URL, redirect to it
      if (gateway_data.invoice_url) {
        window.location.href = gateway_data.invoice_url;
        return Promise.resolve();
      }
      
      // If the gateway provides a payment form, return the data
      return Promise.resolve(gateway_data);
    }
    
    return Promise.reject(new Error('Invalid payment data'));
  }

  /**
   * Poll for payment status updates
   * @param {string} paymentId - The payment ID
   * @param {function} callback - Callback function to handle status updates
   * @param {number} interval - Polling interval in milliseconds
   * @returns {Object} - An object with a stop method to stop polling
   */
  pollPaymentStatus(paymentId, callback, interval = 5000) {
    const poll = setInterval(() => {
      this.getPaymentStatus(paymentId)
        .then(response => {
          const status = response.data.status;
          callback(null, status, response.data);
          
          // If the payment is complete or failed, stop polling
          if (['completed', 'failed', 'refunded'].includes(status)) {
            clearInterval(poll);
          }
        })
        .catch(error => {
          callback(error);
        });
    }, interval);
    
    return {
      stop: () => clearInterval(poll)
    };
  }
}

export default new PaymentService();