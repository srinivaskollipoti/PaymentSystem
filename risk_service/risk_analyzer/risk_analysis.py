import logging
import random
from typing import Dict


def calculate_risk_score() -> int:
    """
    Generates random intger in range of (1,10) both are inclusive

    Returns
    --------
    a random number

    """
    return random.randint(1, 10)


def risk_analysis(payload: Dict) -> Dict:
    """
    Risk analysis is done by checking against the risk score
    Risk analysis evaluate the risk_score and let paas the 70% of message
    received from queue
    """

    try:
        risk_score = calculate_risk_score()
        payload["risk_score"] = risk_score
        if risk_score <= 7:
            payload["state"] = "SUCCESS"
        else:
            payload["state"] = "FAILED"
    except Exception as e:
        logging.debug("failed to analyze the risk")
        raise e

    return payload
