python3 /deploy/app/populate.py
rqscheduler --host ${REDIS_HOST:-redis} &
gunicorn -w 4 -b 0.0.0.0:8000 application:app