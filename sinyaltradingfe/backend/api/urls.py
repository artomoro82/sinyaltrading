from django.urls import path
from api.views import (
    ProductListView, ProductDetailView, 
    CategoryListView, CategoryDetailView,
    OrderCreateView, OrderListView, OrderDetailView
)

urlpatterns = [
    path('products/', ProductListView.as_view(), name='product-list'),
    path('products/<slug:slug>/', ProductDetailView.as_view(), name='product-detail'),
    path('categories/', CategoryListView.as_view(), name='category-list'),
    path('categories/<slug:slug>/', CategoryDetailView.as_view(), name='category-detail'),
    path('orders/', OrderListView.as_view(), name='order-list'),
    path('orders/create/', OrderCreateView.as_view(), name='order-create'),
    path('orders/<str:order_number>/', OrderDetailView.as_view(), name='order-detail'),
]
