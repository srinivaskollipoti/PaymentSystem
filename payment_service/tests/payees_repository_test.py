import pytest
from mock import patch

from payment_service.repository.payees_repository import PayeesRepository


@patch("payment_service.repository.payees_repository.DatabaseHandle")
class TestPayeesRepository:
    def test_object_creation(self, mocker):
        obj = PayeesRepository()
        assert obj is not None

    def test_db_retrieval_success(self, mocker):
        expected_res = [
            {"EMAIL_ID": "dummy1@gmail.com", "FIRST_NAME": "fn", "LAST_NAME": "ln"},
            {"EMAIL_ID": "dummy2@gmail.com", "FIRST_NAME": "fn", "LAST_NAME": "ln"},
        ]
        mock_instance_dbhandle = mocker.return_value
        mock_instance_dbhandle.client().cursor().fetchall.return_value = expected_res
        obj = PayeesRepository()
        res = obj.retrieve("test_first_name", "test_last_name")
        assert res == expected_res

    def test_db_retrieval_fail(self, mocker):
        mock_instance_dbhandle = mocker.return_value
        mock_instance_dbhandle.client().cursor().fetchall.side_effect = Exception(
            "mysql.connector.errors"
        )
        obj = PayeesRepository()
        with pytest.raises(Exception):
            obj.retrieve("test_first_name", "test_last_name")
