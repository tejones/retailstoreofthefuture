import asyncio

from kafka import KafkaConsumer

from app.utils import logger
from app.utils.config import CLIENT_ID, AUTO_OFFSET_RESET, BOOTSTRAP_SERVERS, GROUP_ID, POLL_TIMEOUT


class EventConsumer:
    def __init__(self, topic_name: str, bootstrap_servers=BOOTSTRAP_SERVERS, group_id=GROUP_ID,
                 client_id: str = CLIENT_ID, auto_offset_reset=AUTO_OFFSET_RESET):
        logger.info(f'EventConsumer {topic_name}, {bootstrap_servers}, {group_id}, {client_id}, {auto_offset_reset}')
        self.consumer = self.__create_kafka_consumer(bootstrap_servers, group_id, client_id, auto_offset_reset)

        self.topic = topic_name
        self.consumer.subscribe([topic_name])

        self.process_args = []
        self.process_kwargs = {}

    @staticmethod
    def __create_kafka_consumer(bootstrap_servers=BOOTSTRAP_SERVERS, group_id=GROUP_ID,
                                client_id=CLIENT_ID, auto_offset_reset=AUTO_OFFSET_RESET):
        _consumer = None
        try:
            _consumer = KafkaConsumer(bootstrap_servers=bootstrap_servers, group_id=group_id, client_id=client_id,
                                      auto_offset_reset=auto_offset_reset)
            logger.info('The connection with Kafka has been established.')
        except Exception as ex:
            logger.error('Exception while connecting to Kafka')
            logger.error(ex)
            raise

        return _consumer

    async def process(self, message: str, *args, **kwargs):
        logger.warning('Not implemented.')

    async def consume_messages_blocking(self):
        logger.info(f'Starting messages consumption for {self.topic}')
        for message in self.consumer:
            logger.debug(f'Received {message}')
            await self.process(message, *self.process_args, **self.process_kwargs)

    async def consume_messages(self):
        logger.info(f'Starting messages consumption for {self.topic}')
        running = True
        while running:
            msg_pack = self.consumer.poll(POLL_TIMEOUT)
            for tp, messages in msg_pack.items():
                for message in messages:
                    logger.debug(f"{tp.topic}:{tp.partition}:{message.offset} key={message.key}, value={message.value}")
                    await self.process(message.value.decode('utf-8'), *self.process_args, **self.process_kwargs)
                await asyncio.sleep(0)
            await asyncio.sleep(1)





