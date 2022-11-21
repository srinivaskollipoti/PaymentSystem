"""
Custom exception classes
"""


class PayeeNotFoundException(Exception):
    def __init__(self, *args: object) -> None:
        super().__init__(*args)
