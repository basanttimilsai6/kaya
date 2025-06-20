import redis
import json
import bcrypt
import random
from core.bcrypt_text import *
from kaya.settings import ENVIRONMENT, DEFAULT_DEV_OTP, OTP_EXPIRATION_SECONDS

redis_client = redis.Redis(host='redis', port=6379, db=0)

def set_cache(key, data, ttl=600):
    json_data = json.dumps(data)
    redis_client.setex(key, ttl, json_data)  # set with expiry (TTL)

def get_cache(key):
    value = redis_client.get(key)
    if value is None:
        return None
    return json.loads(value)

def delete_cache(key):
    redis_client.delete(key)

def validate_otp(phone, input_otp):
    key = f"otp_for_{phone}"
    hashed_otp = get_cache(key)
    if not hashed_otp:
        return False
    if check_hash(input_otp, hashed_otp):
        delete_cache(key)
        return True
    return False