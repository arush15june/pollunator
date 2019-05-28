"""
    Notification Scheduler

    scheduler
    module to schedule subscription notiifcations.

    Notifications can be scheduled by the hour, default is 24 hours.
"""

from redis import Redis
from rq import Queue
from rq_scheduler import Scheduler
from datetime import datetime

from pusher import Pusher

class RedisConnectionError(Exception):
    pass

try:
    scheduler = Scheduler('pollunator_subscribers', connection=Redis())
except:
    raise RedisConnectionError()

def schedule_subscriber_hourly(subscriber, hours=24, *args, **kwargs):
    job_time = datetime.timedelta(hours=hours)

    if subscriber.notify_time > datetime.utcnow():
        job_time = subscriber.notify_time
    else:
        job_time += subscriber.notify_time
        
    notification_data = subscriber.notification_data

    scheduler.schedule(
        scheduled_time=job_time, # Time for first execution, in UTC timezone
        func=send_notification,                     # Function to be queued
        args=[subscriber],             # Arguments passed into function when executed
        kwargs=notification_data         # Keyword arguments passed into function when executed
        interval=60,                   # Time before the function is called again, in seconds
        repeat=None                   # Repeat this number of times (None means repeat forever)
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
        return True
    except:
        return False