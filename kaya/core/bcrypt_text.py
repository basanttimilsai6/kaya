import bcrypt
import random


def convert_to_hash(text):
    encode = text.encode()
    salt = bcrypt.gensalt()
    hashed_text = bcrypt.hashpw(encode, salt)
    return hashed_text.decode()

def check_hash(user_input, hashed_data):
    user_input_bytes = user_input.encode()
    hashed_bytes = hashed_data.encode()  # convert DB string to bytes
    return bcrypt.checkpw(user_input_bytes, hashed_bytes)
    
def generate_otp():
    return str(random.randint(100000,999999))