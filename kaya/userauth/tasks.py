from celery import shared_task
import requests
import logging

logger = logging.getLogger(__name__)

@shared_task
def send_sms_otp(phone, otp):
    """
    Send OTP to user via Easy ServiceSMS or any SMS gateway.
    """
    try:
        message = f"Your verification code is {otp}"

        # Replace this with your actual Easy ServiceSMS API config
        response = requests.post("https://sms.easyservicesms.com/api/v1/sms", data={
            "apikey": "your-api-key-here",
            "to": phone,
            "message": message,
            # Add other required params like sender_id if needed
        })

        if response.status_code == 200:
            logger.info(f"OTP sent successfully to {phone}")
            return True
        else:
            logger.error(f"Failed to send OTP to {phone}: {response.text}")
            return False

    except Exception as e:
        logger.exception(f"Error sending OTP to {phone}: {str(e)}")
        return False
