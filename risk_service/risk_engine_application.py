import json
import logging

from message_queue.message_consumer import MessageQueue
from repository.payment_repository import PaymentRepository
from risk_analyzer.risk_analysis import risk_analysis


def callback(channel, method, properties, payload) -> None:
    try:
        logging.debug(" [x] Received %s" % payload)

        payload = json.loads(payload.decode())

        logging.info("Analyzing risk score for the payment")

        payload_with_risk = risk_analysis(payload)

        paymentRepository.save(payload_with_risk)

        logging.info("Record creation with risk analysis completed")

        channel.basic_ack(delivery_tag=method.delivery_tag)

        logging.debug("Message processed from the payment_queue")

    except Exception as e:
        logging.error("Unable to process the message from queue")


if __name__ == "__main__":
    messageQueue = MessageQueue()

    paymentRepository = PaymentRepository()

    messageQueue.recieve(callback)
