import datetime
import json

from app.utils import logger
from app.utils.config import COUPON_SCORER_URL
from app.utils.kafka_clients import prediction_producer

PREDICTION_RESPONSE_TEMPLATE = """
{{
    "event_type": "prediction result",
    "event_timestamp": "{}",
    "payload": {{
        "customer_id": {},
        "coupon_id": {},
        "prediction": {}
    }}
}}"""

scorer_url = f'{COUPON_SCORER_URL}/score_coupons'


async def process_prediction_request(message: str) -> float:
    logger.info('process_prediction_request')

    json_object = json.loads(message)

    # TODO XXX unmarshall the payload
    customer_id: int = 1
    department_id: int = 1

    logger.info(f'calling Score Coupons service with {customer_id}, {department_id}')

    # TODO XXX make a real call
    logger.warn(f'not implemented -- should invoke {scorer_url}')

    result = 0.7

    timestamp = datetime.datetime.utcnow().isoformat()
    message = PREDICTION_RESPONSE_TEMPLATE.format(timestamp, customer_id, department_id, result)

    prediction_producer.publish_message(message)

    return result
