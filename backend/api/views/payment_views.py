import json
import uuid
import logging
from decimal import Decimal

from django.conf import settings
from django.http import Http404
from django.shortcuts import get_object_or_404
from django.utils import timezone

from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny

from api.models import Order, Payment, PaymentLog
from api.serializers import PaymentSerializer
from api.services.payment_gateway import PaymentGatewayService

logger = logging.getLogger(__name__)

class CreatePaymentView(APIView):
    """
    Create a new payment for an order
    """
    permission_classes = [IsAuthenticated]
    
    def post(self, request):
        order_id = request.data.get('order_id')
        
        if not order_id:
            return Response({'error': 'Order ID is required'}, status=status.HTTP_400_BAD_REQUEST)
        
        try:
            order = Order.objects.get(order_number=order_id, user=request.user)
        except Order.DoesNotExist:
            return Response({'error': 'Order not found'}, status=status.HTTP_404_NOT_FOUND)
        
        # Check if order is already paid
        if order.payment_status == 'paid':
            return Response({'error': 'Order is already paid'}, status=status.HTTP_400_BAD_REQUEST)
        
        # Generate a unique payment ID
        payment_id = f"PAY-{uuid.uuid4().hex[:12].upper()}"
        
        # Create payment record
        payment = Payment.objects.create(
            payment_id=payment_id,
            order=order,
            payment_method='crypto',
            amount=order.total,
            currency=order.currency,
            status='pending'
        )
        
        # Initialize payment with gateway
        payment_gateway = PaymentGatewayService()
        
        try:
            gateway_response = payment_gateway.create_payment(
                payment_id=payment_id,
                amount=float(order.total),
                currency=order.currency,
                order_id=order.order_number,
                customer_email=request.user.email
            )
            
            # Update payment with gateway data
            payment.payment_data = gateway_response
            payment.save()
            
            # Log the payment creation
            PaymentLog.objects.create(
                payment=payment,
                action='create',
                status='success',
                data=gateway_response,
                ip_address=self.get_client_ip(request)
            )
            
            # Return payment details
            serializer = PaymentSerializer(payment)
            return Response({
                'payment_id': payment.payment_id,
                'status': payment.status,
                'gateway_data': gateway_response
            }, status=status.HTTP_201_CREATED)
            
        except Exception as e:
            logger.error(f"Payment creation failed: {str(e)}")
            
            # Log the error
            PaymentLog.objects.create(
                payment=payment,
                action='create',
                status='error',
                data={'error': str(e)},
                ip_address=self.get_client_ip(request)
            )
            
            # Update payment status
            payment.status = 'failed'
            payment.save()
            
            return Response({'error': 'Payment creation failed'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
    def get_client_ip(self, request):
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            ip = x_forwarded_for.split(',')[0]
        else:
            ip = request.META.get('REMOTE_ADDR')
        return ip


class PaymentStatusView(APIView):
    """
    Get the status of a payment
    """
    permission_classes = [IsAuthenticated]
    
    def get(self, request, payment_id):
        try:
            payment = Payment.objects.get(payment_id=payment_id)
            
            # Check if user owns the payment
            if payment.order.user != request.user:
                return Response({'error': 'Unauthorized'}, status=status.HTTP_403_FORBIDDEN)
            
            # If payment is still pending, check with gateway
            if payment.status in ['pending', 'processing']:
                payment_gateway = PaymentGatewayService()
                
                try:
                    gateway_status = payment_gateway.check_payment_status(payment_id)
                    
                    # Update payment status based on gateway response
                    if gateway_status['payment_status'] != payment.status:
                        payment.status = gateway_status['payment_status']
                        payment.updated_at = timezone.now()
                        
                        if 'transaction_id' in gateway_status and gateway_status['transaction_id']:
                            payment.transaction_id = gateway_status['transaction_id']
                        
                        payment.save()
                        
                        # Update order payment status if payment is completed
                        if payment.status == 'completed':
                            order = payment.order
                            order.payment_status = 'paid'
                            order.status = 'processing'
                            order.save()
                        
                        # Log the status update
                        PaymentLog.objects.create(
                            payment=payment,
                            action='status_check',
                            status='success',
                            data=gateway_status,
                            ip_address=self.get_client_ip(request)
                        )
                    
                except Exception as e:
                    logger.error(f"Payment status check failed: {str(e)}")
                    
                    # Log the error
                    PaymentLog.objects.create(
                        payment=payment,
                        action='status_check',
                        status='error',
                        data={'error': str(e)},
                        ip_address=self.get_client_ip(request)
                    )
            
            # Return payment details
            serializer = PaymentSerializer(payment)
            return Response(serializer.data)
            
        except Payment.DoesNotExist:
            return Response({'error': 'Payment not found'}, status=status.HTTP_404_NOT_FOUND)
    
    def get_client_ip(self, request):
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            ip = x_forwarded_for.split(',')[0]
        else:
            ip = request.META.get('REMOTE_ADDR')
        return ip


class PaymentWebhookView(APIView):
    """
    Handle payment gateway webhooks (IPN)
    """
    permission_classes = [AllowAny]
    
    def post(self, request):
        # Get the raw request body
        try:
            payload = json.loads(request.body)
        except json.JSONDecodeError:
            return Response({'error': 'Invalid JSON'}, status=status.HTTP_400_BAD_REQUEST)
        
        # Verify the webhook signature if available
        # This depends on the payment gateway implementation
        
        # Extract payment ID from the payload
        payment_id = payload.get('payment_id')
        if not payment_id:
            return Response({'error': 'Payment ID not found in payload'}, status=status.HTTP_400_BAD_REQUEST)
        
        try:
            payment = Payment.objects.get(payment_id=payment_id)
        except Payment.DoesNotExist:
            return Response({'error': 'Payment not found'}, status=status.HTTP_404_NOT_FOUND)
        
        # Process the webhook based on the event type
        event_type = payload.get('event_type')
        
        if event_type == 'payment.completed':
            # Update payment status
            payment.status = 'completed'
            payment.transaction_id = payload.get('transaction_id')
            payment.updated_at = timezone.now()
            payment.save()
            
            # Update order payment status
            order = payment.order
            order.payment_status = 'paid'
            order.status = 'processing'
            order.save()
            
        elif event_type == 'payment.failed':
            # Update payment status
            payment.status = 'failed'
            payment.updated_at = timezone.now()
            payment.save()
            
        elif event_type == 'payment.refunded':
            # Update payment status
            payment.status = 'refunded'
            payment.updated_at = timezone.now()
            payment.save()
            
            # Update order payment status
            order = payment.order
            order.payment_status = 'refunded'
            order.save()
        
        # Log the webhook
        PaymentLog.objects.create(
            payment=payment,
            action='webhook',
            status='success',
            data=payload,
            ip_address=self.get_client_ip(request)
        )
        
        return Response({'status': 'success'})
    
    def get_client_ip(self, request):
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            ip = x_forwarded_for.split(',')[0]
        else:
            ip = request.META.get('REMOTE_ADDR')
        return ip