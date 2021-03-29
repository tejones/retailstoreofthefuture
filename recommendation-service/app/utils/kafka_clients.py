from app.utils import log_config
from app.utils import logger
from app.utils.config import ENTRY_EVENT_TOPIC_NAME, FOCUS_EVENT_TOPIC_NAME, COUPON_PREDICTION_TOPIC_NAME, GROUP_ID, \
    TESTING_NO_KAFKA
from app.utils.context_client import EntryEventProcessor
from app.utils.event_producer import EventProducer
from app.utils.prediction_client import FocusEventProcessor
from app.utils.testing import DummyConsumer, DummyProducer


def create_kafka_clients(cache_reader):
    if not TESTING_NO_KAFKA:
        logger.info('Initializing entry topic consumer')
        entry_consumer = EntryEventProcessor(ENTRY_EVENT_TOPIC_NAME, group_id=GROUP_ID)
        entry_consumer.set_cache_reader(cache_reader)

        logger.info('Initializing Kafka producer')
        prediction_producer = EventProducer(COUPON_PREDICTION_TOPIC_NAME)

        logger.info('Initializing focus topic consumer')
        focus_consumer = FocusEventProcessor(FOCUS_EVENT_TOPIC_NAME, group_id=GROUP_ID)
        focus_consumer.set_result_producer(prediction_producer)
        focus_consumer.set_cache_reader(cache_reader)

    else:
        logger.warn('- ' * 20)
        logger.warn('')
        logger.warn('Initializing dummy consumers and producer (no Kafka connection).')
        logger.warn('Please don\'t be fooled!')
        logger.warn('')
        logger.warn('- ' * 20)
        entry_consumer = DummyConsumer(ENTRY_EVENT_TOPIC_NAME, group_id=GROUP_ID)
        focus_consumer = DummyConsumer(FOCUS_EVENT_TOPIC_NAME, group_id=GROUP_ID)

        prediction_producer = DummyProducer(COUPON_PREDICTION_TOPIC_NAME)
    return entry_consumer, focus_consumer, prediction_producer
