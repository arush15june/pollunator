import dateutil.parser
from datetime import datetime, timedelta

from models import Subscriber, Station
from database import init_db, db_session

import scheduler

NOTIFICATION_REPEAT_HOURS = 24

def get_subscriber(*args, **kwargs):
    return Subscriber.query.filter_by(**kwargs)

def transform_notify_time(notify_time):
    curr_time = datetime.utcnow()
    curr_time = curr_time.replace(
        hour=notify_time.hour,
        minute=notify_time.minute,
        second=notify_time.second
    )
    curr_time -= timedelta(hours=5, minutes=30)
    return curr_time

class InvalidSubscriberInputError(Exception):
    pass

def add_subscriber(*args, **kwargs):
    """
        add subscriber to datbase and job queue

        TODO: verify notify_time_str to be HH:MM.
    """
    subscriber_dict = {
        'email': kwargs.get('email'),
        'station_id': kwargs.get('station_id'),
        'endpoint': kwargs.get('endpoint'),
        'dh_param': kwargs.get('p256dh'),
        'auth': kwargs.get('auth')
    }

    notify_time_str = kwargs.get('notify_time')
    notify_time = dateutil.parser.parse(notify_time_str)
    notify_time = transform_notify_time(notify_time)

    subscriber_dict['notify_time'] = notify_time

    subscriber = Subscriber(**subscriber_dict)
    db_session.add(subscriber)

    # Commit to database, rollback if commit fails
    try:
        db_session.commit()
    except:
        db_session.rollback()
        raise InvalidSubscriberInputError()

    queue_registration_notification(subscriber)
    set_notification_job(subscriber)

    return subscriber

def set_notification_job(subscriber):
    """
        Queue the notification job for subscriber.

        :param models.Subscriber subscriber: models.Subscriber instance
    """
    scheduler.schedule_subscriber(subscriber, hours=NOTIFICATION_REPEAT_HOURS)

def queue_registration_notification(subscriber):
    scheduler.schedule_registration_notif(subscriber)