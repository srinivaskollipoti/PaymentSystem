from repository.payment_methods_repository import PaymentMethodsRepository
from utils.currency import CURRENCY_TYPES


class Payment:
    def __init__(
        self,
        userId: str,
        payeeId: str,
        paymentMethodId: str,
        amount: float,
        currency: str,
    ) -> None:
        self.userId = userId
        self.payeeId = payeeId
        self.paymentMethodId = paymentMethodId
        self.amount = amount
        self.currency = currency

    def is_valid_input(self) -> bool:

        if (
            self.userId
            and self.payeeId
            and self.paymentMethodId
            and self.currency
            and isinstance(self.amount, float) is not None
        ):
            return True
        return False

    def is_currency_valid(self) -> bool:
        for ct in CURRENCY_TYPES:
            if self.currency.casefold() == ct.casefold():
                return True
        return False

    def is_amount_valid(self) -> bool:
        return False if self.amount < 0 else True

    def is_payment_method_valid(self) -> bool:
        """
        Validate the paymentMethod available for the user.

        ASSUMPTION: User added set of PAYMENT methods to his/her account
                    which are available in the USER_PAYMENT_METHOD table.
                    When a User makes a request for a new payment, this function is
                    validating if payment method id is valid.

        Parameters
        ----------
        data : Payment object

        Returns
        -------
        bool
            Confirms the paymentMethodId is available/ or not in USER_PAYMENT_METHODS
        """
        pr = PaymentMethodsRepository()
        payment_methods = pr.retrieve(self.userId)
        for pm in payment_methods:
            if self.paymentMethodId in pm.values():
                return True
        return False

    def is_valid_payload(self, data) -> bool:
        """
        Validate the payment data by checking valid string and float values.

        Parameters
        ----------
        data : Payment object

        Returns
        -------
        bool
            Confirms the validity of data
        """
        return (
            data.is_valid_input()
            and data.is_currency_valid()
            and data.is_amount_valid()
            and data.is_payment_method_valid()
        )
