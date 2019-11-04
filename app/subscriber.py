import dateutil.parser
from datetime import datetime

from models import Subscriber, Station
from database import init_db, db_session
from scheduler import schedule_subscriber_hourly
from pusher import Pusher

NOTIFICATION_REPEAT_HOURS = 24
REGISTRATION_NOTIFICATION_BODY = 'You will receive daily notifications for your selected air quality monitoring station\n' 

push_instance = Push()

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

def generate_registration_notif_payload(subscriber):
    """ 
        Generate payload for registration WebPush notification.

        :param models.Subscriber subscriber: models.Subscriber instance
    """
    station = subscriber.get_station()
    notification_options = {
        'title': f'Registered for {station.station_name}',
        'body': REGISTRATION_NOTIFICATION_BODY
    }