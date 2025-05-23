import os
import json
import uuid
import hmac
import hashlib
import requests
import logging
from decimal import Decimal
from django.conf import settings

logger = logging.getLogger(__name__)

class PaymentGatewayService:
    """
    Service for interacting with the payment gateway (NowPayments)
    """
    
    def __init__(self):
        # Get API credentials from environment variables or settings
        self.api_key = os.environ.get('NOWPAYMENTS_API_KEY', 'K-XXXXXXXX-XXXXXXXX-XXXXXXXX-XXXXXXXX')
        self.api_secret = os.environ.get('NOWPAYMENTS_API_SECRET', 'S-XXXXXXXX-XXXXXXXX-XXXXXXXX-XXXXXXXX')
        self.ipn_secret = os.environ.get('NOWPAYMENTS_IPN_SECRET', 'IPN-XXXXXXXX-XXXXXXXX-XXXXXXXX-XXXXXXXX')
        self.base_url = 'https://api.nowpayments.io/v1'
        
        # Set to True for production
        self.is_production = os.environ.get('NOWPAYMENTS_PRODUCTION', 'false').lower() == 'true'
        
        if not self.is_production:
            # Use sandbox URL for testing
            self.base_url = 'https://api-sandbox.nowpayments.io/v1'
    
    def create_payment(self, payment_id, amount, currency='USD', order_id=None, customer_email=None):
        """
        Create a payment with the payment gateway
        
        Args:
            payment_id (str): Unique payment ID
            amount (float): Payment amount
            currency (str): Currency code (default: USD)
            order_id (str): Order ID (optional)
            customer_email (str): Customer email (optional)
            
        Returns:
            dict: Payment gateway response
        """
        endpoint = f"{self.base_url}/payment"
        
        # Prepare payment data
        payment_data = {
            'price_amount': amount,
            'price_currency': currency,
            'pay_currency': 'BTC',  # Default to Bitcoin, can be changed
            'ipn_callback_url': f"{settings.SITE_URL}/api/payments/ipn/",
            'order_id': order_id or payment_id,
            'order_description': f"Payment for order {order_id or payment_id}",
            'success_url': f"{settings.SITE_URL}/dashboard/payment/{payment_id}/success",
            'cancel_url': f"{settings.SITE_URL}/dashboard/payment/{payment_id}/cancel",
        }
        
        if customer_email:
            payment_data['payer_email'] = customer_email
        
        # Add custom payment ID to identify the payment
        payment_data['custom_payment_id'] = payment_id
        
        headers = {
            'x-api-key': self.api_key,
            'Content-Type': 'application/json'
        }
        
        try:
            response = requests.post(endpoint, json=payment_data, headers=headers)
            response.raise_for_status()
            
            return response.json()
        except requests.exceptions.RequestException as e:
            logger.error(f"Payment gateway error: {str(e)}")
            if hasattr(e, 'response') and e.response:
                logger.error(f"Response: {e.response.text}")
            raise
    
    def check_payment_status(self, payment_id):
        """
        Check the status of a payment with the payment gateway
        
        Args:
            payment_id (str): Payment ID
            
        Returns:
            dict: Payment status
        """
        endpoint = f"{self.base_url}/payment/{payment_id}"
        
        headers = {
            'x-api-key': self.api_key,
            'Content-Type': 'application/json'
        }
        
        try:
            response = requests.get(endpoint, headers=headers)
            response.raise_for_status()
            
            payment_data = response.json()
            
            # Map gateway status to our status
            status_mapping = {
                'waiting': 'pending',
                'confirming': 'processing',
                'confirmed': 'completed',
                'sending': 'processing',
                'partially_paid': 'processing',
                'finished': 'completed',
                'failed': 'failed',
                'refunded': 'refunded',
                'expired': 'failed'
            }
            
            return {
                'payment_status': status_mapping.get(payment_data.get('payment_status'), 'pending'),
                'transaction_id': payment_data.get('pay_address'),
                'amount': payment_data.get('price_amount'),
                'currency': payment_data.get('price_currency'),
                'gateway_data': payment_data
            }
        except requests.exceptions.RequestException as e:
            logger.error(f"Payment gateway error: {str(e)}")
            if hasattr(e, 'response') and e.response:
                logger.error(f"Response: {e.response.text}")
            raise
    
    def verify_ipn_signature(self, request_data, signature):
        """
        Verify the signature of an IPN request
        
        Args:
            request_data (str): Raw request data
            signature (str): Signature from the request header
            
        Returns:
            bool: True if signature is valid, False otherwise
        """
        if not self.ipn_secret:
            logger.warning("IPN secret not configured, skipping signature verification")
            return True
        
        # Create HMAC signature
        hmac_obj = hmac.new(
            self.ipn_secret.encode('utf-8'),
            request_data.encode('utf-8'),
            hashlib.sha512
        )
        calculated_signature = hmac_obj.hexdigest()
        
        return hmac.compare_digest(calculated_signature, signature)