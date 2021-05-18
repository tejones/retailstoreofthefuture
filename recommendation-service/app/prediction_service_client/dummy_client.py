import random
from typing import List

from app import logger
from app.prediction_service_client.model import Customer, Coupon, PredictionOutput


class DummyPredictionServiceClient:

    def __init__(self):
        logger.warning('- ' * 20)
        logger.warning('')
        logger.warning('Using dummy prediction-service client.')
        logger.warning('')
        logger.warning('- ' * 20)

    async def get_prediction(self, customer_context: Customer, coupons: List[Coupon]) -> List[PredictionOutput]:
        output = [
            PredictionOutput(
                coupon_id=c.coupon_id,
                customer_id=customer_context.customer_id,
                prediction=0.45
            )
            for c in coupons
        ]
        return sorted(output, key=lambda i: i.prediction, reverse=True)
