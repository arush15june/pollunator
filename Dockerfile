FROM python:3.6-slim-stretch

COPY ./requirements.txt /deploy/app/
RUN pip install -r /deploy/app/requirements.txt
RUN pip install gunicorn

WORKDIR /deploy/app

CMD ["/bin/bash", "/deploy/app/entrypoint.sh"]
