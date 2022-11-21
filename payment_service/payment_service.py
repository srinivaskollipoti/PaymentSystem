import json
import logging
from exceptions.payee_exception import PayeeNotFoundException
from exceptions.payment_exceptions import PaymentRequestException
from exceptions.payment_method_exception import PaymentMethodException
from typing import Dict

from flask import Flask, Response, jsonify, make_response, request

from message_queue.message_queue_service import MessageQueue, publish_payload
from repository.payees_repository import PayeesRepository
from repository.payment_methods_repository import PaymentMethodsRepository
from validation.payment_validaton_service import Payment

PERMITTED_TYPES = ["application/json"]

app = Flask(__name__)


@app.route("/v1/payments", methods=["POST"])
def create_payment() -> Dict:
    """
    Validates incoming request body, create a new payment
    payload and publish the message to payment_queue

    Parameters
    ----------
    Data: Dict

    Returns
    -------
    Dict
        Succes/Exception message with response code tied as json
    """

    logging.info("Processing Payment")
    try:
        if request.headers.get("CONTENT_TYPE") not in PERMITTED_TYPES:
            raise PaymentRequestException("Content type not permitted")

        amount = request.json.get("amount")
        currency = request.json.get("currency")
        userId = request.json.get("userId")
        payeeId = request.json.get("payeeId")
        paymentMethodId = request.json.get("paymentMethodId")

        payment = Payment(userId, payeeId, paymentMethodId, amount, currency)

        if not payment.is_valid_payload(payment):
            logging.error(f"Invalid payload to process {payment.__dict__}")
            raise PaymentRequestException("Bad request")

        serialized_payload = json.dumps(payment.__dict__)

        publish_payload(serialized_payload)

        logging.info("Payment added to the queue")
        return make_response(
            jsonify(
                {
                    "message": "Your payment has been successfully added to our payment processing unit. Thank you for the payment"
                }
            ),
            200,
        )

    except PaymentRequestException as e:
        logging.error(e)
        return Response(response=str(format(e)), status=400)

    except Exception as e:
        logging.error(f"Error while processing payment {e}")
        return Response(response=str(format(e)), status=500)


@app.route("/v1/payment-methods", methods=["GET"])
def getPaymentMethods() -> Dict:
    """
    Provides list of user's payment-methods

    Parameters
    ----------
    userId : (Query Parameter) User Id

    Returns
    -------
    List
        A list of valid payment methods along with Succes/Exception message with response code tied as json
    """
    logging.info("Payment methods requested")

    userId = request.args.get("userId")

    try:
        payment_methods_data = payment_methods.retrieve(userId)
        if not payment_methods_data:
            raise PaymentMethodException(
                "No payment method found. Please add a payment method."
            )

    except PaymentMethodException as e:
        logging.error(e)
        return Response(response=str(format(e)), status=204)

    except Exception as e:
        message = "Unable to retrive Payment methods."
        logging.error(message + str(e))
        return make_response(
            jsonify(message),
            500,
        )
    logging.info("Payment methods sent.")
    return make_response(
        jsonify(payment_methods_data),
        200,
    )


@app.route("/v1/payees", methods=["GET"])
def getPayees() -> Dict:
    """
    Provides list of payees

    Parameters
    ----------
    firstName : (Query Parameter) First Name of payee
    lastName : (Query Parameter) Last Name of payee

    Returns
    -------
    list
        A list of dict of valid payees along with Succes/Exception message with response code
    """

    logging.info("Requested for existing Payee's details")

    fname = request.args.get("firstName")
    lname = request.args.get("lastName")

    try:
        payees_data = payees.retrieve(fname, lname)
        if not payees_data:
            raise PayeeNotFoundException("No payee details found")

    except PayeeNotFoundException as e:
        logging.error(e)
        return Response(response=jsonify(str(format(e))), status=204)

    except Exception as e:
        message = "Unable to retrive Payee's details."
        logging.error(message + str(e))
        return make_response(
            jsonify(message),
            500,
        )

    logging.info("Payee details sent.")
    return make_response(
        jsonify(payees_data),
        200,
    )


if __name__ == "__main__":
    messageQueue = MessageQueue()

    payment_methods = PaymentMethodsRepository()
    payees = PayeesRepository()

    app.run(debug=True, host="0.0.0.0")
