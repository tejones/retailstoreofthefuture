from app.utils import logger
from app.utils.config import CLIENT_ID, AUTO_OFFSET_RESET, BOOTSTRAP_SERVERS, GROUP_ID


class DummyConsumer:
    def __init__(self, topic_name: str, bootstrap_servers=BOOTSTRAP_SERVERS, group_id=GROUP_ID,
                 client_id: str = CLIENT_ID, auto_offset_reset=AUTO_OFFSET_RESET):
        logger.info(f'DummyConsumer {topic_name}, {bootstrap_servers}, {group_id}, {client_id}, {auto_offset_reset}')
        self.consumer = None
        self.topic = topic_name

    async def process(self, message: str):
        logger.warning('Not implemented.')

    async def consume_messages(self):
        logger.info(f'Pretending messages consumption for {self.topic}')


class DummyProducer:
    def __init__(self, topic_name: str, bootstrap_servers=BOOTSTRAP_SERVERS, client_id: str = CLIENT_ID):
        logger.info(f'DummyProducer {topic_name}, {bootstrap_servers}, {client_id}')
        self.producer = None
        self.topic = topic_name

    def publish_message(self, value: str, key: str = None):
        logger.info(f'pretending to publish_message to topic {self.topic} with key {key}')
        logger.info(value)
        try:
            if key:
                key = key.encode('utf-8')
            if value:
                value = value.encode('utf-8')
            logger.debug(f'Message {value} published.')
        except Exception as ex:
            logger.error(f'Exception in publishing message: {type(ex)} {ex}')
