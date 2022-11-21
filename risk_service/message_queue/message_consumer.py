import logging
import time

import pika


def rabbit_mq_heartbeat():
    while True:
        try:
            connection = pika.BlockingConnection(
                pika.ConnectionParameters(host="rabbitmq")
            )
            return connection
        except pika.exceptions.AMQPConnectionError:
            print("AMQPConnectionError trying again")
            time.sleep(5)
            continue


class MessageQueue:
    """
    Class to configure message queue.
    """

    def __init__(self) -> None:
        self.connection = rabbit_mq_heartbeat()
        self.consumerCallback = None

    def publish(self, payload):

        logging.info("Connected to rabbitmq server......")
        channel = self.connection.channel()
        channel.queue_declare(queue="payment_queue", durable=True)
        channel.basic_publish(
            exchange="",
            routing_key="payment_queue",
            body=payload,
            properties=pika.BasicProperties(
                delivery_mode=2,
            ),
        )
        self.connection.close()

    def recieve(self, callback):
        self.consumerCallback = callback
        sleepTime = 20
        logging.debug(" [*] Sleeping for ", sleepTime, " seconds.")
        time.sleep(sleepTime)

        logging.debug(" [*] Connecting to server ...")
        connection = pika.BlockingConnection(pika.ConnectionParameters(host="rabbitmq"))
        channel = connection.channel()
        channel.queue_declare(queue="payment_queue", durable=True)
        logging.debug(" [*] Waiting for messages.")
        channel.basic_qos(prefetch_count=1)
        channel.basic_consume(queue="payment_queue", on_message_callback=callback)
        channel.start_consuming()
