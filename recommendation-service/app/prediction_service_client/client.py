from typing import List

import httpx

from app import logger
from app.config import config
from app.prediction_service_client.dummy_client import DummyPredictionServiceClient
from app.prediction_service_client.model import Customer, Coupon, PredictionOutput


class PredictionServiceClient:
    _service_url = config.COUPON_SCORER_URL

    def __init__(self):
        logger.info(f'Using prediction service at {self._service_url}')

    async def get_prediction(self, customer_context: Customer, coupons: List[Coupon]) -> List[PredictionOutput]:
        payload = self._create_payload(customer_context, coupons)
        logger.info(f'Calling {self._service_url}')
        logger.debug(f'payload: {payload}')

        async with httpx.AsyncClient() as client:
            response = await client.post(self._service_url, json=payload)

        logger.info(f'Response code: {response.status_code}')
        if response.status_code != 200:
            raise PredictionServiceException(f'Prediction Service response: {response.status_code}, {response.text}')
        logger.debug(f'Response text: {response.text}')

        return [PredictionOutput(**row) for row in response.json()]

    def _create_payload(self, customer_context: Customer, coupons: List[Coupon]):
        return {
            'customer': customer_context.dict(),
            'coupons': [c.dict() for c in coupons]
        }


class PredictionServiceException(Exception):
    pass


def create_prediction_service_client():
    if not config.TESTING_NO_SCORING_SERVICE:
        return PredictionServiceClient()
    else:
        return DummyPredictionServiceClient()
