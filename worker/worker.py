

#######################################################################################
# Standard Imports
#######################################################################################
import json
import os
import time

#######################################################################################
# Package Imports
#######################################################################################
import pika
import psycopg2

#######################################################################################
# Global Variables
#######################################################################################

## NONE ##

#######################################################################################
# Code and Classes
#######################################################################################

class Worker():
    def __init__(self, queue_hostname, queue_name):
        self.queue_hostname = queue_hostname
        self.queue_name = queue_name
    def run(self):
        connection = pika.BlockingConnection(pika.ConnectionParameters(self.queue_hostname))
        channel = connection.channel()
        channel.queue_declare(queue=self.queue_name, durable=True)

        channel.basic_qos(prefetch_count=1)

        channel.basic_consume(self.callback, queue=self.queue_name)
        channel.start_consuming()


    def callback(self, ch, method, properties, body):
        body = json.loads(body)
        print(body)
        ch.basic_ack(delivery_tag = method.delivery_tag)


#######################################################################################
# Main
#######################################################################################
if __name__ == "__main__":
    time.sleep(20)
    worker = Worker(os.getenv("QUEUE_IP"), os.getenv("QUEUE_NAME"))
    worker.run()
