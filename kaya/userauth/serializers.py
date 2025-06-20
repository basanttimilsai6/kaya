from rest_framework import serializers
from userauth.models import UserDevice
import re


def validate_phone(value):
    if not value.startswith("+977-"):
        raise serializers.ValidationError("Phone number must start with '+977-'.")
    if len(value) != 15:
        raise serializers.ValidationError("Phone number must be exactly 15 characters long.")
    # Optional: further regex check for digits after prefix
    pattern = r"^\+977-\d{10}$"
    if not re.match(pattern, value):
        raise serializers.ValidationError("Phone number format is invalid. Example: +977-XXXXXXXXXX")
    return value


class SendOTPSerializer(serializers.Serializer):
    phone = serializers.CharField(max_length=15, validators=[validate_phone])



class UserDeviceSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserDevice
        fields = ['device_id', 'fcm_token', 'device_type']


class VerifyOTPSerializer(serializers.Serializer):
    phone = serializers.CharField(max_length=15, validators=[validate_phone])
    otp = serializers.CharField(max_length=10)
    device = UserDeviceSerializer(required=False)  # Mark as optional if it can be omitted
