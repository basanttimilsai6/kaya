from userauth.models import User, UserDevice
from core.cache import validate_otp, generate_otp,set_cache
from userauth.tasks import send_sms_otp
from kaya.settings import ENVIRONMENT,DEFAULT_DEV_OTP,OTP_EXPIRATION_SECONDS
from core.bcrypt_text import convert_to_hash

class UserAuthLogic:
    @staticmethod
    def send_otp_to_phone(phone):
        key = f"otp_for_{phone}"
        otp = generate_otp() if ENVIRONMENT != "dev" else DEFAULT_DEV_OTP
        set_cache(key, convert_to_hash(otp), OTP_EXPIRATION_SECONDS)

        if ENVIRONMENT != "dev":
            send_sms_otp.delay(phone, otp)
        
        return True

    @staticmethod
    def verify_otp_and_get_user(phone, otp):
        if not validate_otp(phone, otp):
            return None
        user, _ = User.objects.get_or_create(phone=phone)
        return user

    @staticmethod
    def create_or_update_user_device(user, device_id, fcm_token, device_type):
        try:
            UserDevice.objects.update_or_create(
                device_id=device_id,
                defaults={
                    'user': user,
                    'fcm_token': fcm_token,
                    'device_type': device_type
                }
            )
            return True
        except Exception:
            return False
