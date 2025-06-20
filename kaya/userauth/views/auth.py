from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken

from userauth.services.auth import UserAuthLogic as ual
from userauth.serializers import SendOTPSerializer, VerifyOTPSerializer, UserDeviceSerializer

from rest_framework.views import APIView
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken
from core.response import MyResponse


class SendOTPView(APIView):
    serializer_class = SendOTPSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)

        phone = serializer.validated_data['phone']
        ual.send_otp_to_phone(phone)

        return MyResponse.success(message="OTP sent successfully.")


class VerifyOTPView(APIView):
    serializer_class = VerifyOTPSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)

        phone = serializer.validated_data['phone']
        otp = serializer.validated_data['otp']
        device_data = serializer.validated_data.get('device')

        user = ual.verify_otp_and_get_user(phone, otp)
        if not user:
            return MyResponse.failure(message="Invalid OTP or expired.", status_code=status.HTTP_400_BAD_REQUEST)

        if device_data:
            device_serializer = UserDeviceSerializer(data=device_data)
            if device_serializer.is_valid():
                ual.create_or_update_user_device(user, **device_serializer.validated_data)

        refresh = RefreshToken.for_user(user)

        return MyResponse.success(
            data={"refresh": str(refresh),"access": str(refresh.access_token)},message="Login successful.")
