from pydantic import ValidationError

from app import logger
from app.cache.cache_reader import CacheReader
from app.config import config
from app.event_emitters.prediction_producer import PredictionProducer
from app.event_processors.model import FocusEvent
from app.prediction_service_client.client import PredictionServiceClient


class FocusEventProcessor:

    def __init__(self,
                 cache_reader: CacheReader,
                 prediction_service_client: PredictionServiceClient,
                 prediction_producer: PredictionProducer
                 ):
        self._cache_reader = cache_reader
        self._prediction_service_client = prediction_service_client
        self._prediction_producer = prediction_producer

    async def process(self, message: str):
        logger.info(f'Process focus (message: f{message}')
        try:
            focus_event = FocusEvent.parse_raw(message)
        except ValidationError as e:
            logger.error(
                f'Could not parse focus event message: {message}: {e}')
            return

        # Get customer context
        logger.debug(f"focus_event: {focus_event}")
        customer_context = await self._cache_reader.read_customer(int(focus_event.customer_id))
        logger.debug(f'Got customer context: {customer_context}')

        # Get available coupons
        available_coupons = await self._cache_reader.read_coupons(focus_event.dep)
        logger.debug(f'There are {len(available_coupons)} coupons available.')

        # Get prediction
        scored_coupons = await self._prediction_service_client.get_prediction(customer_context, available_coupons)

        # Filter
        scored_coupons = sorted(scored_coupons, key=lambda p: -p.prediction)[:config.MAX_COUPONS_PER_CALL]
        scored_coupons = list(filter(lambda p: p.prediction > config.PREDICTION_THRESHOLD, scored_coupons))

        # for sc in scored_coupons:
        # Get products for the recommended coupon
        # TODO: check if coupons were returned in the first place
        sc = scored_coupons[0]
        products = await self._cache_reader.read_products(coupon_id=sc.coupon_id)
        coupon_info = next(c for c in available_coupons if c.coupon_id == sc.coupon_id)

        # Emit prediction result event
        await self._prediction_producer.publish(
            customer_id=customer_context.customer_id,
            coupon_info=coupon_info,
            products=products
        )

        logger.info(f'1 message has been published')

        # TODO construct response
        return 'Done'
