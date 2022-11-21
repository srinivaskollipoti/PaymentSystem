from typing import Any

import mysql.connector


class DatabaseHandle:
    """
    Class to configure to mysql connector.
    """

    def __init__(self) -> None:
        self.connection = None

    def client(self) -> Any:
        self.connection = mysql.connector.connect(
            user="root", password="root", host="mysql", port="3306", database="db"
        )
        return self.connection

    def close(self) -> Any:
        self.connection.close()
