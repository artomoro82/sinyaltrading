from django.contrib import admin
from .models import (
    ProductCategory, Product, ProductSubscriptionPlan, SignalDetail, BotDetail,
    BotFile, UserBotConfiguration, BotLicense, BotDownloadActivationLog,
    ProductReview, ProductBundle, ProductBundleItem, DigitalInventory,
    Order, OrderItem, UserSubscription, Payment, PaymentLog,
    Page, Report, Notification
)

# Product related admin
@admin.register(ProductCategory)
class ProductCategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug', 'parent', 'is_active', 'order_index')
    list_filter = ('is_active',)
    search_fields = ('name', 'slug')
    prepopulated_fields = {'slug': ('name',)}


class ProductSubscriptionPlanInline(admin.TabularInline):
    model = ProductSubscriptionPlan
    extra = 1


class SignalDetailInline(admin.StackedInline):
    model = SignalDetail
    can_delete = False


class BotDetailInline(admin.StackedInline):
    model = BotDetail
    can_delete = False


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'category', 'price', 'product_type', 'is_active', 'is_featured')
    list_filter = ('is_active', 'is_featured', 'product_type', 'category')
    search_fields = ('name', 'slug', 'description')
    prepopulated_fields = {'slug': ('name',)}
    inlines = [ProductSubscriptionPlanInline, SignalDetailInline, BotDetailInline]


@admin.register(ProductSubscriptionPlan)
class ProductSubscriptionPlanAdmin(admin.ModelAdmin):
    list_display = ('name', 'product', 'price', 'billing_cycle', 'is_active')
    list_filter = ('is_active', 'billing_cycle')
    search_fields = ('name', 'product__name')


@admin.register(BotFile)
class BotFileAdmin(admin.ModelAdmin):
    list_display = ('file_name', 'bot_detail', 'version', 'file_type', 'is_active')
    list_filter = ('is_active', 'file_type')
    search_fields = ('file_name', 'bot_detail__product__name')


@admin.register(UserBotConfiguration)
class UserBotConfigurationAdmin(admin.ModelAdmin):
    list_display = ('configuration_name', 'user', 'bot_product', 'is_default')
    list_filter = ('is_default',)
    search_fields = ('configuration_name', 'user__email', 'bot_product__name')


@admin.register(BotLicense)
class BotLicenseAdmin(admin.ModelAdmin):
    list_display = ('license_key', 'user', 'product', 'status', 'activation_count', 'expiry_date')
    list_filter = ('status',)
    search_fields = ('license_key', 'user__email', 'product__name')


@admin.register(BotDownloadActivationLog)
class BotDownloadActivationLogAdmin(admin.ModelAdmin):
    list_display = ('user', 'action_type', 'bot_license', 'ip_address', 'log_timestamp')
    list_filter = ('action_type',)
    search_fields = ('user__email', 'bot_license__license_key', 'ip_address')
    readonly_fields = ('log_timestamp',)


@admin.register(ProductReview)
class ProductReviewAdmin(admin.ModelAdmin):
    list_display = ('product', 'user', 'rating', 'is_verified_purchase', 'is_approved', 'created_at')
    list_filter = ('is_verified_purchase', 'is_approved', 'rating')
    search_fields = ('product__name', 'user__email', 'title', 'content')
    readonly_fields = ('created_at',)


@admin.register(ProductBundle)
class ProductBundleAdmin(admin.ModelAdmin):
    list_display = ('name', 'price', 'is_active')
    list_filter = ('is_active',)
    search_fields = ('name', 'description')


@admin.register(DigitalInventory)
class DigitalInventoryAdmin(admin.ModelAdmin):
    list_display = ('product', 'total_stock', 'available_stock')
    search_fields = ('product__name',)


# Order related admin
class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 1


class PaymentInline(admin.TabularInline):
    model = Payment
    extra = 0
    readonly_fields = ('payment_id', 'created_at', 'updated_at')


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('order_number', 'user', 'status', 'payment_status', 'total', 'created_at')
    list_filter = ('status', 'payment_status')
    search_fields = ('order_number', 'user__email')
    readonly_fields = ('created_at', 'updated_at')
    inlines = [OrderItemInline, PaymentInline]


@admin.register(UserSubscription)
class UserSubscriptionAdmin(admin.ModelAdmin):
    list_display = ('user', 'subscription_plan', 'status', 'start_date', 'end_date', 'auto_renew')
    list_filter = ('status', 'auto_renew')
    search_fields = ('user__email', 'subscription_plan__name')


# Payment related admin
class PaymentLogInline(admin.TabularInline):
    model = PaymentLog
    extra = 0
    readonly_fields = ('created_at',)


@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    list_display = ('payment_id', 'order', 'payment_method', 'amount', 'status', 'created_at')
    list_filter = ('status', 'payment_method')
    search_fields = ('payment_id', 'order__order_number', 'transaction_id')
    readonly_fields = ('created_at', 'updated_at')
    inlines = [PaymentLogInline]


# Content management admin
@admin.register(Page)
class PageAdmin(admin.ModelAdmin):
    list_display = ('title', 'slug', 'is_published', 'published_at')
    list_filter = ('is_published',)
    search_fields = ('title', 'slug', 'content')
    prepopulated_fields = {'slug': ('title',)}


# Reporting admin
@admin.register(Report)
class ReportAdmin(admin.ModelAdmin):
    list_display = ('name', 'report_type', 'created_by', 'is_scheduled', 'last_run_at')
    list_filter = ('report_type', 'is_scheduled')
    search_fields = ('name', 'created_by__email')


# Notification admin
@admin.register(Notification)
class NotificationAdmin(admin.ModelAdmin):
    list_display = ('title', 'user', 'notification_type', 'is_read', 'created_at')
    list_filter = ('notification_type', 'is_read')
    search_fields = ('title', 'message', 'user__email')
    readonly_fields = ('created_at', 'read_at')
