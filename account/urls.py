from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView

from .views import SendOTPView, VerifyOTPView, send_otp_view, verify_otp_view

app_name = 'account'
urlpatterns = [
    path('send-otp/', SendOTPView.as_view(), name='send-otp'),
    path('verify-otp/', VerifyOTPView.as_view(), name='verify-otp'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token-refresh'),

    path('login/', send_otp_view, name='otp-login'),
    path('verify/<str:phone>/', verify_otp_view, name='otp-login-verify'),
]
