from rest_framework import serializers
from django.contrib.auth import get_user_model
from api.models import (
    ProductCategory, Product, ProductSubscriptionPlan, SignalDetail, BotDetail,
    BotFile, UserBotConfiguration, BotLicense, BotDownloadActivationLog,
    ProductReview, ProductBundle, ProductBundleItem, DigitalInventory,
    Order, OrderItem, UserSubscription, Payment, PaymentLog,
    Page, Report, Notification
)

User = get_user_model()

class ProductCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductCategory
        fields = ['id', 'name', 'slug', 'description', 'parent', 'image_url', 'is_active', 'order_index']


class SignalDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = SignalDetail
        fields = ['asset_pairs', 'timeframes', 'success_rate', 'average_profit_percentage', 
                  'signal_frequency', 'release_schedule_info']


class BotDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = BotDetail
        fields = ['supported_exchanges', 'supported_assets', 'min_capital_required', 
                  'risk_level', 'automation_type', 'backtest_results', 'version']


class ProductReviewSerializer(serializers.ModelSerializer):
    user_name = serializers.SerializerMethodField()
    
    class Meta:
        model = ProductReview
        fields = ['id', 'user', 'user_name', 'rating', 'title', 'content', 
                  'is_verified_purchase', 'created_at']
    
    def get_user_name(self, obj):
        return obj.user.full_name


class ProductSubscriptionPlanSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductSubscriptionPlan
        fields = ['id', 'name', 'description', 'price', 'billing_cycle', 'features', 'is_active']


class ProductSerializer(serializers.ModelSerializer):
    category_name = serializers.SerializerMethodField()
    signal_detail = SignalDetailSerializer(read_only=True)
    bot_detail = BotDetailSerializer(read_only=True)
    reviews = ProductReviewSerializer(many=True, read_only=True)
    subscription_plans = ProductSubscriptionPlanSerializer(many=True, read_only=True)
    
    class Meta:
        model = Product
        fields = ['id', 'name', 'slug', 'category', 'category_name', 'description', 
                  'short_description', 'price', 'sale_price', 'image_url', 
                  'additional_images', 'is_featured', 'is_active', 'product_type', 
                  'signal_detail', 'bot_detail', 'reviews', 'subscription_plans', 
                  'created_at', 'updated_at']
    
    def get_category_name(self, obj):
        return obj.category.name


class ProductBundleSerializer(serializers.ModelSerializer):
    products = ProductSerializer(many=True, read_only=True)
    
    class Meta:
        model = ProductBundle
        fields = ['id', 'name', 'description', 'price', 'products', 'is_active']


class OrderItemSerializer(serializers.ModelSerializer):
    product_name = serializers.SerializerMethodField()
    product_bundle_name = serializers.SerializerMethodField()
    
    class Meta:
        model = OrderItem
        fields = ['id', 'product', 'product_name', 'product_bundle', 'product_bundle_name', 
                  'quantity', 'price', 'subtotal']
    
    def get_product_name(self, obj):
        return obj.product.name if obj.product else None
    
    def get_product_bundle_name(self, obj):
        return obj.product_bundle.name if obj.product_bundle else None


class OrderSerializer(serializers.ModelSerializer):
    items = OrderItemSerializer(many=True, read_only=True)
    
    class Meta:
        model = Order
        fields = ['id', 'order_number', 'user', 'status', 'subtotal', 'tax', 
                  'discount', 'total', 'payment_method', 'payment_status', 
                  'currency', 'notes', 'items', 'created_at', 'updated_at']
        read_only_fields = ['id', 'order_number', 'created_at', 'updated_at']


class OrderCreateSerializer(serializers.ModelSerializer):
    items = serializers.ListField(write_only=True)
    
    class Meta:
        model = Order
        fields = ['payment_method', 'currency', 'notes', 'items']
    
    def create(self, validated_data):
        items_data = validated_data.pop('items')
        user = self.context['request'].user
        
        # Generate order number
        import uuid
        order_number = f"ORD-{uuid.uuid4().hex[:8].upper()}"
        
        # Calculate totals
        subtotal = 0
        for item in items_data:
            if 'product_id' in item:
                product = Product.objects.get(id=item['product_id'])
                price = product.sale_price if product.sale_price else product.price
                item_subtotal = price * item['quantity']
                subtotal += item_subtotal
            elif 'product_bundle_id' in item:
                bundle = ProductBundle.objects.get(id=item['product_bundle_id'])
                item_subtotal = bundle.price * item['quantity']
                subtotal += item_subtotal
        
        # Apply tax (example: 10%)
        tax = subtotal * 0.1
        total = subtotal + tax
        
        # Create order
        order = Order.objects.create(
            user=user,
            order_number=order_number,
            subtotal=subtotal,
            tax=tax,
            total=total,
            **validated_data
        )
        
        # Create order items
        for item in items_data:
            if 'product_id' in item:
                product = Product.objects.get(id=item['product_id'])
                price = product.sale_price if product.sale_price else product.price
                OrderItem.objects.create(
                    order=order,
                    product=product,
                    quantity=item['quantity'],
                    price=price,
                    subtotal=price * item['quantity']
                )
            elif 'product_bundle_id' in item:
                bundle = ProductBundle.objects.get(id=item['product_bundle_id'])
                OrderItem.objects.create(
                    order=order,
                    product_bundle=bundle,
                    quantity=item['quantity'],
                    price=bundle.price,
                    subtotal=bundle.price * item['quantity']
                )
        
        return order


class UserSubscriptionSerializer(serializers.ModelSerializer):
    subscription_plan_name = serializers.SerializerMethodField()
    product_name = serializers.SerializerMethodField()
    
    class Meta:
        model = UserSubscription
        fields = ['id', 'subscription_plan', 'subscription_plan_name', 'product_name',
                  'status', 'start_date', 'end_date', 'auto_renew', 
                  'last_payment_date', 'next_payment_date']
    
    def get_subscription_plan_name(self, obj):
        return obj.subscription_plan.name
    
    def get_product_name(self, obj):
        return obj.subscription_plan.product.name


class PaymentLogSerializer(serializers.ModelSerializer):
    class Meta:
        model = PaymentLog
        fields = ['id', 'payment', 'action', 'status', 'data', 'ip_address', 'created_at']


class PaymentSerializer(serializers.ModelSerializer):
    logs = PaymentLogSerializer(many=True, read_only=True)
    
    class Meta:
        model = Payment
        fields = [
            'id', 'payment_id', 'order', 'payment_method', 'amount', 'currency',
            'status', 'transaction_id', 'payment_data', 'logs', 'created_at', 'updated_at'
        ]


class PageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Page
        fields = [
            'id', 'title', 'slug', 'content', 'meta_title', 'meta_description',
            'is_published', 'published_at', 'created_at', 'updated_at'
        ]


class ReportSerializer(serializers.ModelSerializer):
    class Meta:
        model = Report
        fields = [
            'id', 'name', 'report_type', 'parameters', 'result_data', 'created_by',
            'is_scheduled', 'schedule_frequency', 'last_run_at', 'next_run_at',
            'created_at', 'updated_at'
        ]


class NotificationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Notification
        fields = [
            'id', 'user', 'title', 'message', 'notification_type',
            'is_read', 'read_at', 'data', 'created_at'
        ]
