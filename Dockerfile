FROM python:3.7.2

COPY ./requirements.txt /deploy/app/
RUN pip3 install -r /deploy/app/requirements.txt
RUN pip3 install gunicorn

COPY app /deploy/app
WORKDIR /deploy/app
# Start gunicorn
CMD ["gunicorn","-w", "4", "-b", "0.0.0.0:8000", "application:app"]