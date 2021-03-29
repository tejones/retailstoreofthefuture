import datetime
import json
import httpx

from app.utils import logger
from app.utils.config import COUPON_SCORER_URL, MAX_COUPONS_PER_CALL, PREDICTION_THRESHOLD
from app.utils.kafka_clients import prediction_producer

from app.utils.model import PredictionResultEvent, PredictionResultPayload
from app.utils.prediction_model import PredictionInput, PredictionOutput
from app.cache.read_cache import ReadCache


async def process_prediction_request(message: str, db_pool) -> float:
    logger.info('process_prediction_request')

    # Extract customer and departament category
    json_object = json.loads(message)
    customer_id: int = json_object.get('payload')['customer_id']
    category: str = json_object.get('payload')['category']

    rc = ReadCache(db_pool)
    # Get customer context
    customer = await rc.read_customer(customer_id)

    # Get coupons
    coupons = await rc.read_coupons(category)

    # Create request payload
    payload = PredictionInput(customer=customer, coupons=coupons)

    # Make the request
    logger.info(f'Calling Score Coupons service with {customer_id}, {category}')
    prediction_output = await get_prediction(payload)

    # Filter
    prediction_output = list(sorted(prediction_output, key=lambda p: -p.prediction))[:MAX_COUPONS_PER_CALL]
    prediction_output = list(filter(lambda p: p.prediction > PREDICTION_THRESHOLD, prediction_output))

    # Emmit prediction result event
    timestamp = datetime.datetime.utcnow()

    logger.info(f'Publishing messages with results')
    for p in prediction_output:
        payload = PredictionResultPayload(customer_id=p.customer_id, coupon_id=p.coupon_id, prediction=p.prediction)
        event = PredictionResultEvent(event_timestamp=timestamp, payload=payload)

        prediction_producer.publish_message(event.json())
    logger.info(str(len(prediction_output)) + ' messages has been published')

    # TODO construct response
    return "Done"


async def get_prediction(customer_data):
    logger.info(f"Calling: {COUPON_SCORER_URL}")
    logger.debug(f"With the following payload: {customer_data.json()}")
    
    async with httpx.AsyncClient() as client:
        r = await client.post(COUPON_SCORER_URL, data=customer_data.json())
    
    logger.info(f"Response code: {r.status_code}")
    assert r.status_code == 200
    logger.debug(f'Response text: {r.text}')
    output = r.json()

    return [PredictionOutput(**row) for row in output]
