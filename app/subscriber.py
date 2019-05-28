import dateutil.parser
from datetime import datetime

from models import Subscriber
from database import init_db, db_session

from scheduler import schedule_subscriber_hourly

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

    set_notification_job(subscriber)

    return subscriber

def set_notification_job(subscriber):
    """
        :param models.Subscriber subscriber: models.Subscriber instance
    """
    pass