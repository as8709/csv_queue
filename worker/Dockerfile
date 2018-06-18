FROM python:3.6.5-slim

WORKDIR /app

ADD . /app

RUN pip install --trusted-host pypi.python.org -r requirements.txt

ENV QUEUE_NAME csv
ENV QUEUE_IP rabbitmq


CMD ["python", "worker.py"]