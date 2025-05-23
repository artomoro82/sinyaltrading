from django.urls import path
from api.views import (
    ProductListView, ProductDetailView, 
    CategoryListView, CategoryDetailView,
    OrderCreateView, OrderListView, OrderDetailView
)
from api.views.payment_views import (
    CreatePaymentView, PaymentStatusView, PaymentWebhookView
)

urlpatterns = [
    # Product and Category endpoints
    path('products/', ProductListView.as_view(), name='product-list'),
    path('products/<slug:slug>/', ProductDetailView.as_view(), name='product-detail'),
    path('categories/', CategoryListView.as_view(), name='category-list'),
    path('categories/<slug:slug>/', CategoryDetailView.as_view(), name='category-detail'),
    
    # Order endpoints
    path('orders/', OrderListView.as_view(), name='order-list'),
    path('orders/create/', OrderCreateView.as_view(), name='order-create'),
    path('orders/<str:order_number>/', OrderDetailView.as_view(), name='order-detail'),
    
    # Payment endpoints
    path('payments/create/', CreatePaymentView.as_view(), name='create-payment'),
    path('payments/ipn/', PaymentWebhookView.as_view(), name='payment-ipn'),
    path('payments/<str:payment_id>/status/', PaymentStatusView.as_view(), name='payment-status'),
]
