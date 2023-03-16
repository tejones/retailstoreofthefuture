from datetime import datetime
from typing import List

from fastapi_mqtt import FastMQTT

from app import logger
from app.cache.model import Product as CacheProduct, Coupon as CacheCoupon
from app.config.config import COUPON_PREDICTION_TOPIC
from app.event_emitters.model import Customer, PredictionResult, RecommendedCoupon


class PredictionProducer:

    def __init__(self, mqtt: FastMQTT):
        self._mqtt = mqtt
        self._topic_name = COUPON_PREDICTION_TOPIC

    async def publish(self, customer_id: str, coupon_info: CacheCoupon, products: List[CacheProduct]):
        message = self._create_message(customer_id, coupon_info, products)
        logger.info(f'Publishing message: {message}')
        self._mqtt.publish(self._topic_name, message)

    def _create_message(self, customer_id: str, coupon_info: CacheCoupon, products: List[CacheProduct]) -> str:
        result = PredictionResult(
            customer=Customer(customer_id=customer_id),
            coupon=RecommendedCoupon(
                products=products,
                **coupon_info.dict()
            ),
            ts=datetime.utcnow().timestamp())
        return result.json()
