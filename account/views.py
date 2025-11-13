from django.contrib import messages
from django.contrib.auth import login
from django.db import models
from django.shortcuts import redirect, render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from extensions.sms import send_verification_code
from .forms import OTPVerifyForm, PhoneForm
from .models import OTP, User, Profile
from .serializers import PhoneSerializer, OTPVerifySerializer
from rest_framework_simplejwt.tokens import RefreshToken

from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from django.contrib.auth.decorators import login_required
import json


class SendOTPView(APIView):
    def post(self, request):
        serializer = PhoneSerializer(data=request.data)
        if serializer.is_valid():
            otp = serializer.save()
            return Response({
                "message": "کد ارسال شد (در حالت تست داخل پیام)",
                # "code": otp.code
            }, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class VerifyOTPView(APIView):
    def post(self, request):
        serializer = OTPVerifySerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.validated_data['user']
            refresh = RefreshToken.for_user(user)
            return Response({
                "access": str(refresh.access_token),
                "refresh": str(refresh),
                "message": "ورود با موفقیت انجام شد"
            })
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


def send_otp_view(request):
    if request.method == 'POST':
        form = PhoneForm(request.POST)
        if form.is_valid():
            phone_number = form.cleaned_data['phone_number']

            code = OTP.generate_code()
            OTP.objects.create(phone_number=phone_number, code=code)

            send_verification_code(code, phone_number)

            return redirect('account:otp-login-verify', phone=phone_number)
    else:
        form = PhoneForm()

    return render(request, 'account/send_otp.html', {'form': form})


def verify_otp_view(request, phone):
    if request.method == 'POST':
        form = OTPVerifyForm(request.POST)
        if form.is_valid():
            code = form.cleaned_data['code']

            try:
                otp = OTP.objects.filter(
                    phone_number=phone,
                    code=code,
                    is_verified=False
                ).latest('created_at')

                if otp.is_expired():
                    messages.error(request, 'کد منقضی شده است.')
                else:
                    otp.is_verified = True
                    otp.save()

                    user, created = User.objects.get_or_create(username=phone)

                    login(request, user)

                    messages.success(request, 'ورود با موفقیت انجام شد.')
                    return redirect('game:game-play')  # ریدایرکت به داشبورد
            except OTP.DoesNotExist:
                messages.error(request, 'کد اشتباه است یا قبلاً استفاده شده است.')

    else:
        form = OTPVerifyForm()

    return render(request, 'account/verify_otp.html', {'form': form, 'phone': phone})


def profile_view(request):
    all_profiles = Profile.objects.all().order_by("-total_score", "updated_at")

    # اگر کاربر لاگین کرده، رتبه‌اش را پیدا کن
    user_rank = None
    if request.user.is_authenticated:
        try:
            user_profile = Profile.objects.get(user=request.user)
            # پیدا کردن رتبه کاربر در لیست کامل
            user_rank = all_profiles.filter(
                models.Q(total_score__gt=user_profile.total_score) |
                models.Q(total_score=user_profile.total_score, updated_at__lt=user_profile.updated_at)
            ).count() + 1
        except Profile.DoesNotExist:
            user_rank = None

    context = {
        'user_rank': user_rank
    }
    return render(request, "account/profile.html", context)


def privacy_view(request):
    return render(request, "account/privacy.html")


@login_required
@csrf_exempt
@require_http_methods(["POST"])
def update_nickname(request):
    try:
        data = json.loads(request.body)
        username = data.get('username')

        if not username:
            return JsonResponse({
                'success': False,
                'error': 'Username is required'
            }, status=400)

        # آپدیت nickname کاربر
        request.user.nickname = username
        request.user.save()

        return JsonResponse({
            'success': True,
            'message': 'Nickname updated successfully',
            'new_nickname': username
        })

    except Exception as e:
        return JsonResponse({
            'success': False,
            'error': str(e)
        }, status=500)
