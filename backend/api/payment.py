import requests
import json
import hmac
import hashlib
import time
from django.conf import settings

# Payment Gateway Configuration
PAYMENT_API_KEY = "D1ZPEYK-T39M3ZC-P2VQMC6-KP27CVC"
PAYMENT_PUBLIC_KEY = "804fba77-f2d5-4883-b6e9-ebe9149dd9c7"
PAYMENT_IPN_SECRET = "F1NpY7wLsiAQaIXCNwmEn4g7gq8Oca/B"
PAYMENT_API_URL = "https://api.nowpayments.io/v1"

class PaymentGateway:
    @staticmethod
    def create_payment(order, return_url=None, cancel_url=None):
        """
        Create a payment for an order
        """
        headers = {
            "x-api-key": PAYMENT_API_KEY,
            "Content-Type": "application/json"
        }
        
        payload = {
            "price_amount": float(order.total),
            "price_currency": order.currency,
            "order_id": order.order_number,
            "order_description": f"Payment for order {order.order_number}",
            "ipn_callback_url": f"{settings.SITE_URL}/api/payment/ipn/",
            "success_url": return_url or f"{settings.SITE_URL}/payment/success/",
            "cancel_url": cancel_url or f"{settings.SITE_URL}/payment/cancel/"
        }
        
        try:
            response = requests.post(
                f"{PAYMENT_API_URL}/payment", 
                headers=headers,
                data=json.dumps(payload)
            )
            
            if response.status_code == 200:
                return response.json()
            else:
                return {"error": response.text}
        except Exception as e:
            return {"error": str(e)}
    
    @staticmethod
    def verify_ipn_request(request_data, ipn_signature):
        """
        Verify the IPN request signature
        """
        sorted_data = json.dumps(request_data, separators=(',', ':'), sort_keys=True)
        hmac_obj = hmac.new(
            PAYMENT_IPN_SECRET.encode('utf-8'),
            sorted_data.encode('utf-8'),
            hashlib.sha512
        )
        calculated_signature = hmac_obj.hexdigest()
        
        return calculated_signature == ipn_signature
    
    @staticmethod
    def get_payment_status(payment_id):
        """
        Get the status of a payment
        """
        headers = {
            "x-api-key": PAYMENT_API_KEY
        }
        
        try:
            response = requests.get(
                f"{PAYMENT_API_URL}/payment/{payment_id}", 
                headers=headers
            )
            
            if response.status_code == 200:
                return response.json()
            else:
                return {"error": response.text}
        except Exception as e:
            return {"error": str(e)}