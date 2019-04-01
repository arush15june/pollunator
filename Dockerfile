FROM python:3.7-alpine

COPY ./requirements.txt /deploy/app/
RUN pip3 install -r /deploy/app/requirements.txt
RUN pip3 install gunicorn

COPY app /deploy/app

WORKDIR /deploy/app

CMD ["/bin/bash", "/deploy/app/entrypoint.sh"]