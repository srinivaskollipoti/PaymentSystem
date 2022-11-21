import pytest
from mock import patch

from payment_service.repository.payment_methods_repository import (
    PaymentMethodsRepository,
)


@patch("payment_service.repository.payment_methods_repository.DatabaseHandle")
class TestPaymentMethodsRepository:
    def test_object_creation(self, mocker):
        obj = PaymentMethodsRepository()
        assert obj is not None

    def test_db_retrieval_success(self, mocker):
        expected_res = [
            {
                "PAYMENT_METHOD_ID": 1,
                "PAYMENT_TYPE": "CREDIT",
                "PAYMENT_TYPE_ID": "8e28af1b4",
                "USER_ID": "1234Test",
            },
            {
                "PAYMENT_METHOD_ID": 2,
                "PAYMENT_TYPE": "CREDIT",
                "PAYMENT_TYPE_ID": "8e28af1b6",
                "USER_ID": "1234Test",
            },
        ]
        mock_instance_dbhandle = mocker.return_value
        mock_instance_dbhandle.client().cursor().fetchall.return_value = expected_res
        obj = PaymentMethodsRepository()
        res = obj.retrieve("1234Test")
        assert res == expected_res

    def test_db_retrieval_fail(self, mocker):
        mock_instance_dbhandle = mocker.return_value
        mock_instance_dbhandle.client().cursor().fetchall.side_effect = Exception(
            "mysql.connector.errors"
        )
        obj = PaymentMethodsRepository()
        with pytest.raises(Exception):
            obj.retrieve("1234Test")
