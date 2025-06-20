import firebase_admin
from firebase_admin import credentials, messaging
from kaya.settings import cred_path
import os

cred_path = cred_path
# Initialize Firebase app only once
firebase_app = None

def initialize_firebase():
    global firebase_app
    if not firebase_admin._apps:
        cred = credentials.Certificate(cred_path)
        firebase_app = firebase_admin.initialize_app(cred)

def send_push_notification(token, title, body, data=None):
    """
    Send push notification to a device via FCM.
    """
    initialize_firebase()

    message = messaging.Message(
        notification=messaging.Notification(
            title=title,
            body=body,
        ),
        token=token,
        data=data or {},
    )

    response = messaging.send(message)
    return response
