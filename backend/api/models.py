from django.db import models
from django.utils import timezone
from users.models import User

class ProductCategory(models.Model):
    name = models.CharField(max_length=100)
    slug = models.SlugField(max_length=100, unique=True)
    description = models.TextField(blank=True, null=True)
    parent = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, related_name='children')
    image_url = models.CharField(max_length=255, blank=True, null=True)
    is_active = models.BooleanField(default=True)
    order_index = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.name


class Product(models.Model):
    PRODUCT_TYPE_CHOICES = [
        ('signal', 'Signal'),
        ('bot', 'Bot'),
        ('course', 'Course'),
        ('subscription', 'Subscription'),
        ('other', 'Other'),
    ]
    
    category = models.ForeignKey(ProductCategory, on_delete=models.CASCADE, related_name='products')
    vendor = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='products')
    name = models.CharField(max_length=255)
    slug = models.SlugField(max_length=255, unique=True)
    description = models.TextField()
    short_description = models.CharField(max_length=255, blank=True, null=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    sale_price = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    image_url = models.CharField(max_length=255, blank=True, null=True)
    additional_images = models.JSONField(blank=True, null=True)
    is_featured = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    product_type = models.CharField(max_length=20, choices=PRODUCT_TYPE_CHOICES)
    metadata = models.JSONField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.name


class ProductSubscriptionPlan(models.Model):
    BILLING_CYCLE_CHOICES = [
        ('monthly', 'Monthly'),
        ('quarterly', 'Quarterly'),
        ('biannually', 'Biannually'),
        ('annually', 'Annually'),
    ]
    
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='subscription_plans')
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True, null=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    billing_cycle = models.CharField(max_length=20, choices=BILLING_CYCLE_CHOICES)
    features = models.JSONField()
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"{self.product.name} - {self.name}"


class SignalDetail(models.Model):
    product = models.OneToOneField(Product, on_delete=models.CASCADE, related_name='signal_detail')
    asset_pairs = models.JSONField()
    timeframes = models.JSONField()
    success_rate = models.DecimalField(max_digits=5, decimal_places=2, blank=True, null=True)
    average_profit_percentage = models.DecimalField(max_digits=5, decimal_places=2, blank=True, null=True)
    signal_frequency = models.CharField(max_length=50, blank=True, null=True)
    release_schedule_info = models.TextField(blank=True, null=True)
    
    def __str__(self):
        return f"Signal Detail - {self.product.name}"


class BotDetail(models.Model):
    RISK_LEVEL_CHOICES = [
        ('low', 'Low'),
        ('medium', 'Medium'),
        ('high', 'High'),
    ]
    
    AUTOMATION_TYPE_CHOICES = [
        ('fully_automated', 'Fully Automated'),
        ('semi_automated', 'Semi Automated'),
    ]
    
    product = models.OneToOneField(Product, on_delete=models.CASCADE, related_name='bot_detail')
    supported_exchanges = models.JSONField()
    supported_assets = models.JSONField()
    min_capital_required = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    risk_level = models.CharField(max_length=10, choices=RISK_LEVEL_CHOICES)
    automation_type = models.CharField(max_length=20, choices=AUTOMATION_TYPE_CHOICES)
    backtest_results = models.JSONField(blank=True, null=True)
    version = models.CharField(max_length=20)
    
    def __str__(self):
        return f"Bot Detail - {self.product.name}"


class BotFile(models.Model):
    bot_detail = models.ForeignKey(BotDetail, on_delete=models.CASCADE, related_name='files')
    file_name = models.CharField(max_length=255)
    file_path = models.CharField(max_length=255)
    file_size = models.IntegerField()
    file_type = models.CharField(max_length=50)
    version = models.CharField(max_length=20)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.file_name


class UserBotConfiguration(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='bot_configurations')
    bot_product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='user_configurations')
    configuration_name = models.CharField(max_length=255)
    configuration_data = models.JSONField()
    is_default = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"{self.user.email} - {self.configuration_name}"


class BotLicense(models.Model):
    STATUS_CHOICES = [
        ('active', 'Active'),
        ('inactive', 'Inactive'),
        ('expired', 'Expired'),
        ('revoked', 'Revoked'),
    ]
    
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='bot_licenses')
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='licenses')
    license_key = models.CharField(max_length=100, unique=True)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='inactive')
    activation_limit = models.IntegerField(default=1)
    activation_count = models.IntegerField(default=0)
    expiry_date = models.DateTimeField(blank=True, null=True)
    user_bot_configuration = models.ForeignKey(UserBotConfiguration, on_delete=models.SET_NULL, blank=True, null=True, related_name='licenses')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"{self.user.email} - {self.product.name} - {self.license_key}"


class BotDownloadActivationLog(models.Model):
    ACTION_TYPE_CHOICES = [
        ('download', 'Download'),
        ('activation_attempt', 'Activation Attempt'),
        ('activation_success', 'Activation Success'),
        ('activation_failure', 'Activation Failure'),
    ]
    
    bot_license = models.ForeignKey(BotLicense, on_delete=models.CASCADE, related_name='activation_logs')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='bot_activation_logs')
    bot_file = models.ForeignKey(BotFile, on_delete=models.SET_NULL, blank=True, null=True, related_name='download_logs')
    action_type = models.CharField(max_length=20, choices=ACTION_TYPE_CHOICES)
    ip_address = models.CharField(max_length=45)
    device_info = models.TextField(blank=True, null=True)
    log_timestamp = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.user.email} - {self.action_type} - {self.log_timestamp}"


class ProductReview(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='reviews')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='product_reviews')
    rating = models.PositiveSmallIntegerField()
    title = models.CharField(max_length=255, blank=True, null=True)
    content = models.TextField(blank=True, null=True)
    is_verified_purchase = models.BooleanField(default=False)
    is_approved = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"{self.user.email} - {self.product.name} - {self.rating}"


class ProductBundle(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    products = models.ManyToManyField(Product, through='ProductBundleItem', related_name='bundles')
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.name


class ProductBundleItem(models.Model):
    bundle = models.ForeignKey(ProductBundle, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    
    class Meta:
        unique_together = ('bundle', 'product')
    
    def __str__(self):
        return f"{self.bundle.name} - {self.product.name}"


class DigitalInventory(models.Model):
    product = models.OneToOneField(Product, on_delete=models.CASCADE, primary_key=True, related_name='inventory')
    total_stock = models.IntegerField(blank=True, null=True)
    available_stock = models.IntegerField(blank=True, null=True)
    
    def __str__(self):
        return f"Inventory - {self.product.name}"


class Order(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('processing', 'Processing'),
        ('completed', 'Completed'),
        ('cancelled', 'Cancelled'),
        ('refunded', 'Refunded'),
    ]
    
    PAYMENT_STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('paid', 'Paid'),
        ('failed', 'Failed'),
        ('refunded', 'Refunded'),
    ]
    
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='orders')
    order_number = models.CharField(max_length=50, unique=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    subtotal = models.DecimalField(max_digits=10, decimal_places=2)
    tax = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    discount = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    total = models.DecimalField(max_digits=10, decimal_places=2)
    payment_method = models.CharField(max_length=50, blank=True, null=True)
    payment_status = models.CharField(max_length=10, choices=PAYMENT_STATUS_CHOICES, default='pending')
    currency = models.CharField(max_length=3, default='USD')
    notes = models.TextField(blank=True, null=True)
    billing_address_id = models.IntegerField(blank=True, null=True)
    ip_address = models.CharField(max_length=45, blank=True, null=True)
    user_agent = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.order_number


class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='items')
    product = models.ForeignKey(Product, on_delete=models.SET_NULL, blank=True, null=True, related_name='order_items')
    product_bundle = models.ForeignKey(ProductBundle, on_delete=models.SET_NULL, blank=True, null=True, related_name='order_items')
    quantity = models.IntegerField(default=1)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    subtotal = models.DecimalField(max_digits=10, decimal_places=2)
    metadata = models.JSONField(blank=True, null=True)
    
    def __str__(self):
        product_name = self.product.name if self.product else self.product_bundle.name
        return f"{self.order.order_number} - {product_name}"


class UserSubscription(models.Model):
    STATUS_CHOICES = [
        ('active', 'Active'),
        ('cancelled', 'Cancelled'),
        ('expired', 'Expired'),
        ('pending', 'Pending'),
    ]
    
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='subscriptions')
    subscription_plan = models.ForeignKey(ProductSubscriptionPlan, on_delete=models.CASCADE, related_name='user_subscriptions')
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='pending')
    start_date = models.DateTimeField()
    end_date = models.DateTimeField()
    auto_renew = models.BooleanField(default=True)
    last_payment_date = models.DateTimeField(blank=True, null=True)
    next_payment_date = models.DateTimeField(blank=True, null=True)
    payment_method_id = models.CharField(max_length=100, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"{self.user.email} - {self.subscription_plan.name}"


class Payment(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('processing', 'Processing'),
        ('completed', 'Completed'),
        ('failed', 'Failed'),
        ('refunded', 'Refunded'),
    ]
    
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='payments')
    payment_id = models.CharField(max_length=100, unique=True)
    payment_method = models.CharField(max_length=50)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    currency = models.CharField(max_length=3, default='USD')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    transaction_id = models.CharField(max_length=100, blank=True, null=True)
    payment_data = models.JSONField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"{self.order.order_number} - {self.payment_id}"


class PaymentLog(models.Model):
    payment = models.ForeignKey(Payment, on_delete=models.CASCADE, related_name='logs')
    action = models.CharField(max_length=50)
    status = models.CharField(max_length=50)
    data = models.JSONField(blank=True, null=True)
    ip_address = models.CharField(max_length=45, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.payment.payment_id} - {self.action}"


class Page(models.Model):
    title = models.CharField(max_length=255)
    slug = models.SlugField(max_length=255, unique=True)
    content = models.TextField()
    meta_title = models.CharField(max_length=255, blank=True, null=True)
    meta_description = models.TextField(blank=True, null=True)
    is_published = models.BooleanField(default=False)
    published_at = models.DateTimeField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.title
    
    def save(self, *args, **kwargs):
        if self.is_published and not self.published_at:
            self.published_at = timezone.now()
        super().save(*args, **kwargs)


class Report(models.Model):
    REPORT_TYPE_CHOICES = [
        ('sales', 'Sales Report'),
        ('user_activity', 'User Activity Report'),
        ('product_performance', 'Product Performance Report'),
        ('subscription', 'Subscription Report'),
        ('custom', 'Custom Report'),
    ]
    
    name = models.CharField(max_length=255)
    report_type = models.CharField(max_length=50, choices=REPORT_TYPE_CHOICES)
    parameters = models.JSONField(blank=True, null=True)
    result_data = models.JSONField(blank=True, null=True)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='reports')
    is_scheduled = models.BooleanField(default=False)
    schedule_frequency = models.CharField(max_length=50, blank=True, null=True)
    last_run_at = models.DateTimeField(blank=True, null=True)
    next_run_at = models.DateTimeField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"{self.name} - {self.report_type}"


class Notification(models.Model):
    NOTIFICATION_TYPE_CHOICES = [
        ('system', 'System Notification'),
        ('order', 'Order Notification'),
        ('payment', 'Payment Notification'),
        ('subscription', 'Subscription Notification'),
        ('product', 'Product Notification'),
    ]
    
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='notifications')
    title = models.CharField(max_length=255)
    message = models.TextField()
    notification_type = models.CharField(max_length=20, choices=NOTIFICATION_TYPE_CHOICES)
    is_read = models.BooleanField(default=False)
    read_at = models.DateTimeField(blank=True, null=True)
    data = models.JSONField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.user.email} - {self.title}"
    
    def mark_as_read(self):
        self.is_read = True
        self.read_at = timezone.now()
        self.save()
