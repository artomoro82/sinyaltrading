from rest_framework import viewsets, status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from django.db import transaction
from django.utils import timezone
from .models import Order, Payment, PaymentLog
from .payment import PaymentGateway
import uuid
import json

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def create_payment(request):
    """
    Create a payment for an order
    """
    order_id = request.data.get('order_id')
    if not order_id:
        return Response({'error': 'Order ID is required'}, status=status.HTTP_400_BAD_REQUEST)
    
    order = get_object_or_404(Order, id=order_id, user=request.user)
    
    # Check if order is already paid
    if order.payment_status == 'paid':
        return Response({'error': 'Order is already paid'}, status=status.HTTP_400_BAD_REQUEST)
    
    # Generate a unique payment ID
    payment_id = str(uuid.uuid4())
    
    # Create payment record
    payment = Payment.objects.create(
        order=order,
        payment_id=payment_id,
        payment_method='crypto',
        amount=order.total,
        currency=order.currency,
        status='pending'
    )
    
    # Log the payment creation
    PaymentLog.objects.create(
        payment=payment,
        action='create',
        status='pending',
        data=request.data,
        ip_address=request.META.get('REMOTE_ADDR')
    )
    
    # Create payment in payment gateway
    payment_result = PaymentGateway.create_payment(order)
    
    if 'error' in payment_result:
        payment.status = 'failed'
        payment.save()
        
        PaymentLog.objects.create(
            payment=payment,
            action='gateway_error',
            status='failed',
            data=payment_result,
            ip_address=request.META.get('REMOTE_ADDR')
        )
        
        return Response({'error': payment_result['error']}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
    # Update payment with gateway data
    payment.payment_data = payment_result
    payment.transaction_id = payment_result.get('payment_id')
    payment.status = 'processing'
    payment.save()
    
    PaymentLog.objects.create(
        payment=payment,
        action='gateway_created',
        status='processing',
        data=payment_result,
        ip_address=request.META.get('REMOTE_ADDR')
    )
    
    return Response({
        'payment_id': payment.payment_id,
        'gateway_data': payment_result
    })


@api_view(['POST'])
@permission_classes([AllowAny])
def payment_ipn(request):
    """
    Handle Instant Payment Notification (IPN) from payment gateway
    """
    # Verify the IPN signature
    ipn_signature = request.headers.get('x-nowpayments-sig')
    if not ipn_signature:
        return Response({'error': 'Missing signature'}, status=status.HTTP_400_BAD_REQUEST)
    
    # Parse the request body
    try:
        request_data = json.loads(request.body)
    except json.JSONDecodeError:
        return Response({'error': 'Invalid JSON'}, status=status.HTTP_400_BAD_REQUEST)
    
    # Verify the signature
    if not PaymentGateway.verify_ipn_request(request_data, ipn_signature):
        return Response({'error': 'Invalid signature'}, status=status.HTTP_400_BAD_REQUEST)
    
    # Get the order from the request data
    order_id = request_data.get('order_id')
    if not order_id:
        return Response({'error': 'Missing order ID'}, status=status.HTTP_400_BAD_REQUEST)
    
    # Find the order
    try:
        order = Order.objects.get(order_number=order_id)
    except Order.DoesNotExist:
        return Response({'error': 'Order not found'}, status=status.HTTP_404_NOT_FOUND)
    
    # Find the payment
    try:
        payment = Payment.objects.get(order=order, transaction_id=request_data.get('payment_id'))
    except Payment.DoesNotExist:
        return Response({'error': 'Payment not found'}, status=status.HTTP_404_NOT_FOUND)
    
    # Update payment status based on IPN data
    payment_status = request_data.get('payment_status')
    
    with transaction.atomic():
        # Log the IPN
        PaymentLog.objects.create(
            payment=payment,
            action='ipn_received',
            status=payment_status,
            data=request_data,
            ip_address=request.META.get('REMOTE_ADDR')
        )
        
        # Update payment and order status
        if payment_status == 'confirmed' or payment_status == 'finished':
            payment.status = 'completed'
            payment.save()
            
            order.payment_status = 'paid'
            order.status = 'completed'
            order.save()
        elif payment_status == 'failed':
            payment.status = 'failed'
            payment.save()
            
            order.payment_status = 'failed'
            order.save()
        elif payment_status == 'refunded':
            payment.status = 'refunded'
            payment.save()
            
            order.payment_status = 'refunded'
            order.status = 'refunded'
            order.save()
    
    return Response({'status': 'success'})


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def payment_status(request, payment_id):
    """
    Get the status of a payment
    """
    payment = get_object_or_404(Payment, payment_id=payment_id)
    
    # Check if the user owns the payment
    if payment.order.user != request.user:
        return Response({'error': 'Unauthorized'}, status=status.HTTP_403_FORBIDDEN)
    
    # Get the payment status from the gateway
    if payment.transaction_id:
        gateway_status = PaymentGateway.get_payment_status(payment.transaction_id)
        
        if 'error' not in gateway_status:
            # Update the payment status if needed
            gateway_payment_status = gateway_status.get('payment_status')
            
            if gateway_payment_status == 'confirmed' or gateway_payment_status == 'finished':
                if payment.status != 'completed':
                    with transaction.atomic():
                        payment.status = 'completed'
                        payment.save()
                        
                        payment.order.payment_status = 'paid'
                        payment.order.status = 'completed'
                        payment.order.save()
                        
                        PaymentLog.objects.create(
                            payment=payment,
                            action='status_check',
                            status='completed',
                            data=gateway_status,
                            ip_address=request.META.get('REMOTE_ADDR')
                        )
            elif gateway_payment_status == 'failed':
                if payment.status != 'failed':
                    with transaction.atomic():
                        payment.status = 'failed'
                        payment.save()
                        
                        payment.order.payment_status = 'failed'
                        payment.order.save()
                        
                        PaymentLog.objects.create(
                            payment=payment,
                            action='status_check',
                            status='failed',
                            data=gateway_status,
                            ip_address=request.META.get('REMOTE_ADDR')
                        )
    
    return Response({
        'payment_id': payment.payment_id,
        'status': payment.status,
        'amount': payment.amount,
        'currency': payment.currency,
        'created_at': payment.created_at,
        'updated_at': payment.updated_at
    })