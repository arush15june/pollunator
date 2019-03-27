python /deploy/app/populate.py
gunicorn -w 4 -b 0.0.0.0:8000 application:app