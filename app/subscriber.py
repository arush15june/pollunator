import dateutil.parser
import datetime

from models import Subscriber
from database import init_db, db_session

from pusher import Pusher

def get_susbcriber(*args, **kwargs):
    return Subscriber.query.filter_by(**kwargs)

def add_subscriber(*args, **kwargs):
    """
        add subscriber to datbase and job queue
    """
    subscriber_dict = {
        'email': kwargs.get('email'),
        'endpoint': kwargs.get('endpoint'),
        'p256dh': kwargs.get('p256dh'),
        'auth': kwargs.get('auth')
    }

    notify_time_str = kwargs.get('notify_time')
    notify_time = dateutil.parser.parse(notify_time_str)
    subscriber_dict = datetime.time('')

    subscriber = Subscriber(**subscriber_dict)
    db_session.add(subscriber)
    db_session.commit()

    self.set_notification_job(subscriber)

    return subscriber

def set_notification_job(subscriber):
    """
        :param models.Subscriber subscriber: models.Subscriber instance
    """
    pass


def send_notification(subscriber, *args, **kwargs):
    """
        :param models.Subscriber subscriber: models.Subscriber instance
        kwargs
            :param str title: title for notification
            :param str body: body for notification
    """
    subcription_info = subscriber.subscription_info

    try:
        Pusher.send_notification(subscription_info, **kwargs)
        return True
    except:
        return False