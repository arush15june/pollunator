"""
    Notification Scheduler

    scheduler
    module to schedule subscription notiifcations.

    Notifications can be scheduled by the hour, default is 24 hours.
"""
import os

from redis import Redis
from rq import Queue
from rq_scheduler import Scheduler
from datetime import datetime, timedelta

from pusher import Pusher

REDIS_HOST = os.getenv('RQ_REDIS_HOST', 'redis')
REDIS_PORT = os.getenv('RQ_REDIS_HOST', 6379)

REGISTRATION_NOTIFICATION_BODY = 'You will receive daily notifications for your selected air quality monitoring station\n' 

class RedisConnectionError(Exception):
    pass

try:
    scheduler = Scheduler('pollunator_subscribers', connection=Redis(host=REDIS_HOST, port=REDIS_PORT))
except:
    raise RedisConnectionError()

def generate_registration_notification_payload(subscriber):
    """ 
        Generate payload for registration WebPush notification.

        :param models.Subscriber subscriber: models.Subscriber instance
    """
    station = subscriber.get_station()
    notification_options = {
        'title': f'Registered for {station.station_name}',
        'body': REGISTRATION_NOTIFICATION_BODY
    }

    return notification_options

def schedule_subscriber(subscriber, hours=24, *args, **kwargs):
    job_time = datetime.timedelta(hours=hours)

    if subscriber.notify_time > datetime.utcnow():
        job_time = subscriber.notify_time
    else:
        job_time += subscriber.notify_time
    
    notification_data = subscriber.notification_data()

    scheduler.schedule(
        scheduled_time=job_time, # Time for first execution, in UTC timezone
        func=send_notification,                     # Function to be queued
        args=[subscriber],             # Arguments passed into function when executed
        kwargs=notification_data,         # Keyword arguments passed into function when executed
        interval=hours*60*60,                   # Time before the function is called again, in seconds
        repeat=None                   # Repeat this number of times (None means repeat forever)
    )

def schedule_registration_notif(subscriber, *args, **kwargs):
    """ 
        Schedule to send a notification once.

        :param models.Subscriber subscriber: subscriber to send notification to.
        :kwargs seconds: seconds to enqueue notification in.
    """
    queue_time = kwargs.pop('seconds', 5)
    job_time = timedelta(seconds=queue_time)
    
    notification_data = generate_registration_notification_payload(subscriber)

    scheduler.enqueue_in(
        job_time,
        send_notification,                     
        subscriber,
        **notification_data,    
    )
    
def send_notification(subscriber, *args, **kwargs):
    """
        :param models.Subscriber subscriber: models.Subscriber instance
        kwargs
            :param str title: title for notification
            :param str body: body for notification
    """
    subscription_info = subscriber.subscription_info

    try:
        pusher = Pusher()
        pusher.send_notification(subscription_info, **kwargs)
    except:
        return False

        return True

def send_pollution_notification(subscriber):
    options = generate_notification_payload(subscriber)
    send_pollution_notification(subscriber, **options)