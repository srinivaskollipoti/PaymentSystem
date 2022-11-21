import pytest
from mock import patch

from risk_service.repository.payment_repository import PaymentRepository


@patch("risk_service.repository.payment_repository.DatabaseHandle")
class TestPaymentRepository:
    def test_object_creation(self, mocker):
        obj = PaymentRepository()
        assert obj is not None

    def test_db_commit_success(self, mocker):
        obj = PaymentRepository()
        input = {
            "amount": 200.0,
            "currency": "USD",
            "userId": "test123",
            "payeeId": "test456",
            "paymentMethodId": "test789",
            "risk_score": "6",
            "payment_status": "success",
        }
        res = obj.save(input)
        assert res is None

    def test_db_retrieval_fail(self, mocker):
        mock_instance_dbhandle = mocker.return_value
        mock_instance_dbhandle.client().commit.side_effect = Exception(
            "mysql.connector.errors"
        )
        obj = PaymentRepository()
        with pytest.raises(Exception):
            obj.save({})
