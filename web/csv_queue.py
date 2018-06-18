

#######################################################################################
# Standard Imports
#######################################################################################

import csv
import pika
import argparse
import json

#######################################################################################
# Global Variables
#######################################################################################

parser = argparse.ArgumentParser(description='Tool for reading a given CSV file and sending it to RabbitMQ')
parser.add_argument('csv_filename', help="path to csv file")
parser.add_argument('queue_name', help="name of RabbitMQ queue to send to")
parser.add_argument('--queue_ip', default="localhost", help="ip address of the message queue")

#######################################################################################
# Code and Classes
#######################################################################################

class CsvReader():
    '''Class for reading from an open csv file, serialising it and publishing it to the given queue'''

    def __init__(self, csvfile, queue_name, queue_ip):
        self.queue_name = queue_name
        self.queue_ip = queue_ip
        
        self.rows = csv.reader(csvfile)

    def send(self):
        connection = pika.BlockingConnection(pika.ConnectionParameters(self.queue_ip))
        channel = connection.channel()
        #declare the queue just in case it hasn't already been declared
        #won't do anything if it has
        channel.queue_declare(queue=self.queue_name, durable=True)
        for row in self.rows:
            channel.basic_publish(exchange='',
                routing_key=self.queue_name,
                body=json.dumps(row),
                properties=pika.BasicProperties(
                    delivery_mode=2 # persistent messages
                ))
        connection.close()

#######################################################################################
# Main
#######################################################################################

if __name__ == "__main__":
    args = parser.parse_args()
    with  open(args.csv_filename) as csvfile:
        reader = CsvReader(csvfile, args.queue_name, args.queue_ip)
        reader.send()