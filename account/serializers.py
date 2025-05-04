from rest_framework import serializers
from .models import OTP
from django.contrib.auth import get_user_model

User = get_user_model()


class PhoneSerializer(serializers.Serializer):
    phone_number = serializers.CharField()

    def create(self, validated_data):
        code = OTP.generate_code()
        otp = OTP.objects.create(phone_number=validated_data['phone_number'], code=code)
        return otp


class OTPVerifySerializer(serializers.Serializer):
    phone_number = serializers.CharField()
    code = serializers.CharField()

    def validate(self, data):
        phone = data['phone_number']
        code = data['code']
        try:
            otp = OTP.objects.filter(phone_number=phone, code=code, is_verified=False).latest('created_at')
        except OTP.DoesNotExist:
            raise serializers.ValidationError("کد اشتباه است یا منقضی شده")

        if otp.is_expired():
            raise serializers.ValidationError("کد منقضی شده")

        otp.is_verified = True
        otp.save()

        user, created = User.objects.get_or_create(username=phone)
        data['user'] = user
        return data
