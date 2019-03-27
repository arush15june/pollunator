FROM python:3.7.2

COPY ./requirements.txt /deploy/app/
RUN pip3 install -r /deploy/app/requirements.txt
RUN pip3 install gunicorn

COPY app /deploy/app

WORKDIR /deploy/app

ENTRYPOINT ["/deploy/app/entrypoint.sh"]