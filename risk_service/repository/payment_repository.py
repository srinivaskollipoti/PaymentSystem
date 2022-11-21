import logging
from typing import Dict

from mysql_client.mysql_client import DatabaseHandle


class PaymentRepository:
    """
    Class to insert payments in the database.
    """

    def __init__(self):
        self.__mysql_client = DatabaseHandle()

    def __make_sql_stmt(self):
        SQL_PAYMENT_STMNT = (
            "INSERT INTO PAYMENT (USER_ID ,PAYEE_ID, PAYMENT_METHOD_ID, AMOUNT, CURRENCY, RISK_SCORE, PAYMENT_STATUS)"
            "VALUES (%s, %s,%s,%s,%s,%s,%s)"
        )
        return SQL_PAYMENT_STMNT

    def save(self, payload: Dict) -> None:
        """
        Inserts payload received from risk_analyzer into Payments table
        """

        connection = self.__mysql_client.client()
        cursor = connection.cursor()
        SQL_PAYMENT_STMNT = self.__make_sql_stmt()

        logging.debug(SQL_PAYMENT_STMNT)

        print(payload.values())  # For the demo

        (uid, pid, pmid, cur, amt, rscore, status) = payload.values()

        try:
            logging.debug("Started inserting records into the Payments table")
            cursor.execute(
                SQL_PAYMENT_STMNT, (uid, pid, pmid, cur, amt, rscore, status)
            )
            connection.commit()
            self.__mysql_client.close()
        except Exception as e:
            logging.error("Unable to insert the record to database", str(e))
            raise e

        logging.debug(cursor.rowcount, "record inserted.")
