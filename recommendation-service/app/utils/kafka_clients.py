from app.utils import logger
from app.utils.config import ENTRY_EVENT_TOPIC_NAME, FOCUS_EVENT_TOPIC_NAME, COUPON_PREDICTION_TOPIC_NAME, GROUP_ID, \
    TESTING_NO_KAFKA
from app.utils.event_consumer import EventConsumer
from app.utils.event_producer import EventProducer
from app.utils.testing import DummyConsumer, DummyProducer

if not TESTING_NO_KAFKA:
    logger.info('Initializing Kafka consumers')
    entry_consumer = EventConsumer(ENTRY_EVENT_TOPIC_NAME, group_id=GROUP_ID)
    focus_consumer = EventConsumer(FOCUS_EVENT_TOPIC_NAME, group_id=GROUP_ID)

    logger.info('Initializing Kafka producer')
    prediction_producer = EventProducer(COUPON_PREDICTION_TOPIC_NAME)

else:
    logger.warn('Initializing dummy consumers and producer (no Kafka connection).')
    entry_consumer = DummyConsumer(ENTRY_EVENT_TOPIC_NAME, group_id=GROUP_ID)
    focus_consumer = DummyConsumer(FOCUS_EVENT_TOPIC_NAME, group_id=GROUP_ID)

    prediction_producer = DummyProducer(COUPON_PREDICTION_TOPIC_NAME)
