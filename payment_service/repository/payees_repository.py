import logging
from typing import Dict

from mysql_client.mysql_client import DatabaseHandle


class PayeesRepository:
    """
    Class to connect to user's table.
    """

    def __init__(self):
        self.__mysql_client = DatabaseHandle()

    def __make_select_statement(self, fname, lname):
        SQL_STMT = f"SELECT FIRST_NAME,LAST_NAME,EMAIL_ID FROM USER WHERE FIRST_NAME='{fname}'and LAST_NAME='{lname}';"
        return SQL_STMT

    def retrieve(self, fname, lname) -> Dict:

        logging.debug("All Payees listing requested")

        try:
            cursor = self.__mysql_client.client().cursor(dictionary=True)
            cursor.execute(self.__make_select_statement(fname, lname))
            payment_methods = cursor.fetchall()
            self.__mysql_client.close()

        except Exception as e:
            logging.error(
                "Unable to retrieve list of payees from the USER table", str(e)
            )
            raise e
        logging.debug(
            cursor.rowcount, "Successfully retrieved current available Payees."
        )
        return payment_methods
