FROM python:3.6.5-slim

WORKDIR /app

ADD . /app

RUN pip install --trusted-host pypi.python.org -r requirements.txt

ENV QUEUE_NAME csv
ENV QUEUE_IP rabbitmq

ENV DB_NAME csv_db
ENV DB_HOSTNAME db
ENV DB_USERNAME csv
ENV DB_PASSWORD csv_pw


CMD ["python", "worker.py"]