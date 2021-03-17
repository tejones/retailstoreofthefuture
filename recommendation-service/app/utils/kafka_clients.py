from app.utils import logger
from app.utils.config import ENTRY_EVENT_TOPIC_NAME, FOCUS_EVENT_TOPIC_NAME, COUPON_PREDICTION_TOPIC_NAME, GROUP_ID
from app.utils.event_consumer import EventConsumer
from app.utils.event_producer import EventProducer

logger.info('Initializing Kafka consumers')
entry_consumer = EventConsumer(ENTRY_EVENT_TOPIC_NAME, group_id=GROUP_ID)
focus_consumer = EventConsumer(FOCUS_EVENT_TOPIC_NAME, group_id=GROUP_ID)


logger.info('Initializing Kafka producer')
prediction_producer = EventProducer(COUPON_PREDICTION_TOPIC_NAME)
