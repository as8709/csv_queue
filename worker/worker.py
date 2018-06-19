

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
    def __init__(self, queue_hostname, queue_name, db_name, db_hostname, db_username, db_password):
        self.queue_hostname = queue_hostname
        self.queue_name = queue_name

        self.conn = psycopg2.connect(
            database=db_name,
            host=db_hostname,
            user=db_username,
            password=db_password
            )

    def run(self):
        connection = pika.BlockingConnection(pika.ConnectionParameters(self.queue_hostname))
        channel = connection.channel()
        channel.queue_declare(queue=self.queue_name, durable=True)

        channel.basic_qos(prefetch_count=1)

        channel.basic_consume(self.callback, queue=self.queue_name)
        channel.start_consuming()

    def is_valid_entry(self, entry):
        '''
        Test that the given entry from RabbitMQ is suitable for placing in
        the database
        '''
        if len(entry) != 2:
            return False
        if (not isinstance(entry[0], str)) or (not isinstance(entry[1], str)):
            return False
        return True

    def callback(self, ch, method, properties, body):
        body = json.loads(body)

        if self.is_valid_entry(body):
            try:
                # starts a transaction if one hasn't already been started
                # as we commit or rollback after each insert this should always
                # be starting a new transaction
                with self.conn.cursor() as cur:
                    cur.execute("INSERT INTO emails VALUES(%s, %s)", (body[0], body[1]))
                    # commit the transaction, unlocking the table for other connections
                    self.conn.commit()
            except psycopg2.IntegrityError:
                # TODO what is expected behaviour on conflict?
                self.conn.rollback()
        else:
            # TODO error logging perhaps?
            pass

        ch.basic_ack(delivery_tag=method.delivery_tag)


#######################################################################################
# Main
#######################################################################################

if __name__ == "__main__":
    time.sleep(20)
    worker = Worker(
        os.getenv("QUEUE_IP"),
        os.getenv("QUEUE_NAME"),
        os.getenv("DB_NAME"),
        os.getenv("DB_HOSTNAME"),
        os.getenv("DB_USERNAME"),
        os.getenv("DB_PASSWORD"),
        )
    worker.run()
