from django.urls import path
from users.views import UserRegistrationView, UserLoginView, UserProfileView, UserPasswordChangeView, ForgotPasswordView

urlpatterns = [
    path('register/', UserRegistrationView.as_view(), name='user-register'),
    path('login/', UserLoginView.as_view(), name='user-login'),
    path('profile/', UserProfileView.as_view(), name='user-profile'),
    path('change-password/', UserPasswordChangeView.as_view(), name='user-change-password'),
    path('forgot-password/', ForgotPasswordView.as_view(), name='user-forgot-password'),
]
