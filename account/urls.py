from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView

from .views import SendOTPView, VerifyOTPView

app_name = 'account'
urlpatterns = [
    path('send-otp/', SendOTPView.as_view(), name='send-otp'),
    path('verify-otp/', VerifyOTPView.as_view(), name='verify-otp'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token-refresh'),
]
