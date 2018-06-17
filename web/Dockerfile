FROM python:3.6.5-slim

WORKDIR /app

ADD . /app

RUN pip install --trusted-host pypi.python.org -r requirements.txt

EXPOSE 80

ENV QUEUE_NAME csv
ENV QUEUE_IP rabbitmq


CMD ["python", "app.py"]