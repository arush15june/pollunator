FROM python:3.6.7-alpine3.9

COPY ./requirements.txt /deploy/app/
RUN pip3 install -r /deploy/app/requirements.txt
RUN pip3 install gunicorn

COPY app /deploy/app

WORKDIR /deploy/app

CMD ["/bin/bash", "/deploy/app/entrypoint.sh"]