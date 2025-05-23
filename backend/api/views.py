from rest_framework import generics, permissions, status
from rest_framework.response import Response
from rest_framework.views import APIView
from api.models import (
    ProductCategory, Product, ProductSubscriptionPlan, SignalDetail, BotDetail,
    ProductReview, ProductBundle, Order, OrderItem, UserSubscription
)
from api.serializers import (
    ProductCategorySerializer, ProductSerializer, ProductBundleSerializer,
    OrderSerializer, OrderCreateSerializer, UserSubscriptionSerializer
)
from django.shortcuts import get_object_or_404

class CategoryListView(generics.ListAPIView):
    queryset = ProductCategory.objects.filter(is_active=True)
    serializer_class = ProductCategorySerializer
    permission_classes = [permissions.AllowAny]


class CategoryDetailView(generics.RetrieveAPIView):
    queryset = ProductCategory.objects.filter(is_active=True)
    serializer_class = ProductCategorySerializer
    permission_classes = [permissions.AllowAny]
    lookup_field = 'slug'


class ProductListView(generics.ListAPIView):
    serializer_class = ProductSerializer
    permission_classes = [permissions.AllowAny]
    
    def get_queryset(self):
        queryset = Product.objects.filter(is_active=True)
        
        # Filter by category
        category_slug = self.request.query_params.get('category', None)
        if category_slug:
            queryset = queryset.filter(category__slug=category_slug)
        
        # Filter by product type
        product_type = self.request.query_params.get('type', None)
        if product_type:
            queryset = queryset.filter(product_type=product_type)
        
        # Filter by featured
        featured = self.request.query_params.get('featured', None)
        if featured and featured.lower() == 'true':
            queryset = queryset.filter(is_featured=True)
        
        # Search by name or description
        search = self.request.query_params.get('search', None)
        if search:
            queryset = queryset.filter(
                models.Q(name__icontains=search) | 
                models.Q(description__icontains=search) |
                models.Q(short_description__icontains=search)
            )
        
        return queryset


class ProductDetailView(generics.RetrieveAPIView):
    queryset = Product.objects.filter(is_active=True)
    serializer_class = ProductSerializer
    permission_classes = [permissions.AllowAny]
    lookup_field = 'slug'


class OrderListView(generics.ListAPIView):
    serializer_class = OrderSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        return Order.objects.filter(user=self.request.user).order_by('-created_at')


class OrderDetailView(generics.RetrieveAPIView):
    serializer_class = OrderSerializer
    permission_classes = [permissions.IsAuthenticated]
    lookup_field = 'order_number'
    
    def get_queryset(self):
        return Order.objects.filter(user=self.request.user)


class OrderCreateView(generics.CreateAPIView):
    serializer_class = OrderCreateSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
