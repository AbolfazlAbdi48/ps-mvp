from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import PhoneSerializer, OTPVerifySerializer
from rest_framework_simplejwt.tokens import RefreshToken


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
