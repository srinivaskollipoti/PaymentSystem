import pytest
from mock import Mock

import risk_service.risk_analyzer.risk_analysis as rs


class TestRiskAnalysis:

    """
    This test confirms the risk_analyzer analyzes request payload and set risk_score and state
    """

    def test_success_payment_data(self):
        rs.calculate_risk_score = Mock(return_value=5)
        expected_payload = {"risk_score": 5, "state": "SUCCESS"}
        assert rs.risk_analysis({}) == expected_payload

    def test_failed_payment_data(self):
        rs.calculate_risk_score = Mock(return_value=8)
        expected_payload = {"risk_score": 8, "state": "FAILED"}
        assert rs.risk_analysis({}) == expected_payload

    def test_risk_analysis_exception(self):
        rs.calculate_risk_score = Mock(side_effect=Exception("internal.server.error"))
        with pytest.raises(Exception):
            rs.risk_analysis({})
