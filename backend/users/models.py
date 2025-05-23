from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager
from django.utils import timezone


class UserManager(BaseUserManager):
    def create_user(self, email, username, full_name, password=None, **extra_fields):
        if not email:
            raise ValueError('Users must have an email address')
        if not username:
            raise ValueError('Users must have a username')
        
        email = self.normalize_email(email)
        user = self.model(
            email=email,
            username=username,
            full_name=full_name,
            **extra_fields
        )
        user.set_password(password)
        user.save(using=self._db)
        return user
    
    def create_superuser(self, email, username, full_name, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('status', 'active')
        
        return self.create_user(email, username, full_name, password, **extra_fields)


class User(AbstractBaseUser, PermissionsMixin):
    STATUS_CHOICES = [
        ('active', 'Active'),
        ('inactive', 'Inactive'),
        ('suspended', 'Suspended'),
        ('pending_verification', 'Pending Verification'),
        ('kyc_pending', 'KYC Pending'),
        ('kyc_rejected', 'KYC Rejected'),
    ]
    
    username = models.CharField(max_length=150, unique=True)
    email = models.EmailField(unique=True)
    full_name = models.CharField(max_length=255)
    avatar_url = models.CharField(max_length=255, blank=True, null=True)
    email_verified_at = models.DateTimeField(null=True, blank=True)
    phone_number = models.CharField(max_length=20, blank=True, null=True)
    phone_verified_at = models.DateTimeField(null=True, blank=True)
    two_factor_secret = models.CharField(max_length=255, blank=True, null=True)
    two_factor_enabled = models.BooleanField(default=False)
    u2f_security_keys = models.JSONField(null=True, blank=True)
    referral_code = models.CharField(max_length=50, blank=True, null=True)
    referred_by_user = models.ForeignKey('self', on_delete=models.SET_NULL, null=True, blank=True, related_name='referrals')
    language_preference = models.CharField(max_length=10, default='en')
    timezone_preference = models.CharField(max_length=50, default='UTC')
    dashboard_theme_preference = models.CharField(max_length=50, default='light')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending_verification')
    last_login_at = models.DateTimeField(null=True, blank=True)
    last_login_ip = models.CharField(max_length=45, null=True, blank=True)
    
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    objects = UserManager()
    
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username', 'full_name']
    
    def __str__(self):
        return self.email


class Role(models.Model):
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.name


class Permission(models.Model):
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.name


class UserRole(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user_roles')
    role = models.ForeignKey(Role, on_delete=models.CASCADE, related_name='user_roles')
    
    class Meta:
        unique_together = ('user', 'role')
    
    def __str__(self):
        return f"{self.user.email} - {self.role.name}"


class RolePermission(models.Model):
    role = models.ForeignKey(Role, on_delete=models.CASCADE, related_name='role_permissions')
    permission = models.ForeignKey(Permission, on_delete=models.CASCADE, related_name='role_permissions')
    
    class Meta:
        unique_together = ('role', 'permission')
    
    def __str__(self):
        return f"{self.role.name} - {self.permission.name}"


class UserKYCDocument(models.Model):
    VERIFICATION_STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('approved', 'Approved'),
        ('rejected', 'Rejected'),
        ('resubmit_required', 'Resubmit Required'),
    ]
    
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='kyc_documents')
    document_type = models.CharField(max_length=100)
    document_number = models.CharField(max_length=100, blank=True, null=True)
    file_path = models.CharField(max_length=255)
    verification_status = models.CharField(max_length=20, choices=VERIFICATION_STATUS_CHOICES, default='pending')
    admin_notes = models.TextField(blank=True, null=True)
    submitted_at = models.DateTimeField(auto_now_add=True)
    verified_at = models.DateTimeField(blank=True, null=True)
    verified_by_admin = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='verified_documents')
    
    def __str__(self):
        return f"{self.user.email} - {self.document_type}"


class UserSession(models.Model):
    id = models.CharField(max_length=255, primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='sessions')
    ip_address = models.CharField(max_length=45)
    user_agent = models.TextField()
    last_activity = models.DateTimeField(default=timezone.now)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.user.email} - {self.ip_address}"
