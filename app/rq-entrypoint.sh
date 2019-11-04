rq worker --url redis://redis:6379 pollunator_subscribers &
rqscheduler --host ${REDIS_HOST:-redis} -i 5
