import logging
from typing import Dict

from mysql_client.mysql_client import DatabaseHandle


class PaymentMethodsRepository:
    """
    PaymentMethodsRepository connects to mysql to fetch payment methods available for user
    """

    def __init__(self):
        self.__mysql_client = DatabaseHandle()

    def __make_select_statement(self, userId):
        SQL_STMT = f"select * from USER_PAYMENT_METHOD where USER_ID='{userId}';"
        return SQL_STMT

    def retrieve(self, userId):
        logging.debug("All Payment methods listing requested")
        SQL_STMT = self.__make_select_statement(userId)
        try:
            cursor = self.__mysql_client.client().cursor(dictionary=True)
            cursor.execute(SQL_STMT)
            payment_methods = cursor.fetchall()
            self.__mysql_client.close()

        except Exception as e:
            logging.error(
                "Unable to retrieve payment methods from the Payments table", str(e)
            )
            raise e
        logging.debug(
            cursor.rowcount, "Successfully retrieved current available Payment Methods."
        )
        return payment_methods
