import pytest
from mock import Mock

import payment_service.payment_service as ps


class TestPaymentService:

    """Create Payment API test cases"""

    def test_create_payement_invalid_content_type(self):
        client = ps.app.test_client()
        response = client.post(
            "/v1/payments", json={}, headers={"CONTENT_TYPE": "application/dummy"}
        )

        assert response.status_code == 400

    def test_create_payment_empty_input(self):
        client = ps.app.test_client()
        input = {
            "amount": "",
            "currency": "",
            "userId": "",
            "payeeId": "",
            "paymentMethodId": "",
        }
        response = client.post("/v1/payments", json=input)

        assert response.status_code == 400

    def test_create_payment_invalid_currency(self):
        client = ps.app.test_client()
        input = {
            "amount": "50",
            "currency": "XYZ",
            "userId": "test",
            "payeeId": "123",
            "paymentMethodId": "123",
        }
        response = client.post("/v1/payments", json=input)

        assert response.status_code == 400

    def test_create_payment_invalid_payment_method_id(self):
        ps.PaymentMethodsRepository = Mock()
        ps.PaymentMethodsRepository.retrieve = Mock(return_value=[])

        client = ps.app.test_client()
        input = {
            "amount": "50",
            "currency": "XYZ",
            "userId": "test",
            "payeeId": "123",
            "paymentMethodId": "123",
        }
        response = client.post("/v1/payments", json=input)

        assert response.status_code == 400

    def test_create_payment_invalid_amount(self):
        ps.PaymentMethodsRepository = Mock()
        ps.PaymentMethodsRepository.retrieve = Mock(return_value=[])

        client = ps.app.test_client()
        input = {
            "amount": "-1",
            "currency": "XYZ",
            "userId": "test",
            "payeeId": "123",
            "paymentMethodId": "123",
        }
        response = client.post("/v1/payments", json=input)

        assert response.status_code == 400

    def test_create_payment_exception(self):
        ps.Payment = Mock()
        ps.Payment.is_valid_payload = Mock(return_value=True)
        ps.publish_payload = Mock(side_effect=Exception("queue.connection.error"))

        client = ps.app.test_client()
        input = {
            "amount": "50",
            "currency": "XYZ",
            "userId": "test",
            "payeeId": "123",
            "paymentMethodId": "123",
        }
        response = client.post("/v1/payments", json=input)

        assert response.status_code == 500

    """Get Payment Methods API test cases"""

    def test_get_payment_methods_validate_input(self):
        ps.payment_methods = Mock()
        ps.payment_methods.retrieve = Mock(return_value=1)

        client = ps.app.test_client()
        userId_input = "1234"
        client.get(f"/v1/payment-methods?userId={userId_input}", json={})
        userId_used = ps.payment_methods.retrieve.call_args.args[0]

        assert userId_input == userId_used

    def test_get_payment_methods_not_found(self):
        ps.payment_methods = Mock()
        ps.payment_methods.retrieve = Mock(return_value=[])

        client = ps.app.test_client()
        response = client.get(f"/v1/payment-methods?userId=1234Test", json={})

        assert response.status_code == 204

    def test_get_payment_methods_success(self):
        ps.payment_methods = Mock()
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
        ps.payment_methods.retrieve = Mock(return_value=expected_res)

        client = ps.app.test_client()
        response = client.get("/v1/payment-methods?userId=1234Test", json={})

        assert response.status_code == 200
        assert response.get_json() == expected_res

    def test_get_payment_methods_exception(self):
        ps.payment_methods = Mock()
        ps.payment_methods.retrieve = Mock(
            side_effect=Exception("mysql.connector.errors")
        )

        client = ps.app.test_client()
        response = client.get("/v1/payment-methods?userId=1234Test", json={})

        assert response.status_code == 500
        assert response.get_json() == "Unable to retrive Payment methods."

    """Get payees API test cases"""

    def test_get_payees_validate_input(self):
        ps.payees = Mock()
        ps.payees.retrieve = Mock(return_value=1)

        client = ps.app.test_client()
        fname_input, lname_input = "test_first_name", "test_last_name"
        client.get(
            f"/v1/payees?firstName={fname_input}&&lastName={lname_input}", json={}
        )
        fname_used, lname_used = ps.payees.retrieve.call_args.args

        assert fname_input == fname_used
        assert lname_input == lname_used

    def test_get_payees_not_found(self):
        ps.payees = Mock()
        ps.payees.retrieve = Mock(return_value=[])

        client = ps.app.test_client()
        response = client.get(f"/v1/payees?firstName=TEST&&lastName=TEST", json={})

        assert response.status_code == 204

    def test_get_payees_success(self):
        ps.payees = Mock()
        expected_res = [
            {"EMAIL_ID": "dummy1@gmail.com", "FIRST_NAME": "fn", "LAST_NAME": "ln"},
            {"EMAIL_ID": "dummy2@gmail.com", "FIRST_NAME": "fn", "LAST_NAME": "ln"},
        ]
        ps.payees.retrieve = Mock(return_value=expected_res)

        client = ps.app.test_client()
        response = client.get("/v1/payees?firstName=fn&&lastName=ln", json={})

        assert response.status_code == 200
        assert response.get_json() == expected_res

    def test_get_payees_exception(self):
        ps.payees = Mock()
        ps.payees.retrieve = Mock(side_effect=Exception("mysql.connector.errors"))

        client = ps.app.test_client()
        response = client.get("/v1/payees?firstName=testfn&&lastName=testln", json={})

        assert response.status_code == 500
        assert response.get_json() == "Unable to retrive Payee's details."
