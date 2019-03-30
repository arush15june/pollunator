import os
import json
from pywebpush import webpush, WebPushException

"""
    pusher
    module to handle WebPush subscriptions

    Generate private and public keys via py_vapid,
    install py-vapid (pypi),
    vapid --gen
    generates private and public keys,
    vapid --applicationServerKey
    generates application server key for frontend
"""

DEFAULT_APP_SERVER_KEY = 'BCj6Yxzs5j-zKTzHIrWAAczNCyc_iHht8u_p4Rqw53nOVIebj6a_rIDRBC7Zkj6WpOsr8s8yj8Gg60jjWOu8UqM'
DEFAULT_PRIVATE_KEY_PATH = './private_key.pem'
DEFAULT_PUBLIC_KEY_PATH = './public_key.pem'
DEFAULT_PUSH_CLAIMS_EMAIL = 'ahujaarush@gmail.com'

DEFAULT_NOTIF_TILE = 'Test Notification'
DEFAULT_NOTIF_BODY = 'Test Data 123 0xdeadbeef'

class Pusher(object):
    """
        Push notifications via WebPush.
    """

    APP_SERVER_KEY = os.getenv('APP_SERVER_KEY', DEFAULT_APP_SERVER_KEY)
    PRIVATE_KEY_PATH = os.getenv('PRIVATE_KEY_PATH', DEFAULT_PRIVATE_KEY_PATH)
    PUBLIC_KEY_PATH = os.getenv('PUBLIC_KEY_PATH', DEFAULT_PUBLIC_KEY_PATH)
    PUSH_CLAIMS_EMAIL = os.getenv('PUSH_CLAIMS_EMAIL', DEFAULT_PUSH_CLAIMS_EMAIL)
    CLAIMS_SUB_STRING = f'mailto:{PUSH_CLAIMS_EMAIL}'
    
    def _create_notification_dict(self, *args, **kwargs):
        title = kwargs.pop('title', self.NOTIF_TITLE)
        body = kwargs.pop('body', self.NOTIF_BODY)

        notif_dict = {
            'title': title,
            'options': {
                'body': body
            }
        }

        # Add notification options from kwargs
        notif_dict['options'].update(
            kwargs
        )

    @staticmethod
    def _serialize(data):
        return json.dumps(data)

    def _send_payload(self, subscription_info, serialized_payload):
        """
        send a serialized payload to a subscriber

        :param dict subscription_info: subscription dict from frontend susbcripiton 
                    { "endpoint": "...", "keys": {"p256dh": "..", "auth": ".."} }
        :param str serialized_payload: payload to send via push message, serialize data  
        """
        content_type = 'aes128gcm'
        webpush(
            subscription_info,
            data=serialized_payload,
            vapid_private_key=self.PRIVATE_KEY_PATH,
            content_type=content_type,
            vapid_claims={
                'sub': self.CLAIMS_SUB_STRING
            }
        )

    def send_notification(subscription_info, *args, **kwargs):
        """
            send a notification to subscriber via subscription_info

            :param dict subscription_info: subscription dict from frontend susbcripiton 
                    { "endpoint": "...", "keys": {"p256dh": "..", "auth": ".."} 
            :param str title: title for notification.

        """
        notification_dict = self._create_notification_dict(**kwargs)
        payload = self._serialize(notification_dict)

        self._send_payload(notification_dict, payload)