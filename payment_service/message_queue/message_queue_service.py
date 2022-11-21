import logging
import time
from typing import Dict

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


def publish_payload(payload: Dict) -> str:
    """
    Wrapper to RabbitMQ publish method to put the payload onto queue

    Parameters
    ----------
    payload : Dict

    Returns
    -------
    None
        for succesful publish of the message
    excexption
        throws exception if failed to push
    """
    try:
        logging.info("publishing message to processing queue")
        messageQueue = MessageQueue()
        messageQueue.publish(payload)
    except Exception as e:
        logging.error("Failed to publish message to queue" + str(e))


class MessageQueue:
    """
    Class to configure message queue
    """

    def __init__(self) -> None:
        self.connection = rabbit_mq_heartbeat()

    def publish(self, payload: Dict) -> Dict:
        logging.info("Connected to rabbitmq server......")
        channel = self.connection.channel()
        channel.queue_declare(queue="payment_queue", durable=True)
        channel.basic_publish(
            exchange="",
            routing_key="payment_queue",
            body=payload,
            properties=pika.BasicProperties(
                delivery_mode=2,  # make message persistent
            ),
        )
        self.connection.close()
