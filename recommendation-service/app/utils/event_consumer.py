import asyncio

from confluent_kafka import Consumer

from app.utils import logger
from app.utils.config import CLIENT_ID, AUTO_OFFSET_RESET, BOOTSTRAP_SERVERS, GROUP_ID, POLL_TIMEOUT


class EventConsumer:
    def __init__(self, topic_name: str, bootstrap_servers=BOOTSTRAP_SERVERS, group_id=GROUP_ID,
                 client_id: str = CLIENT_ID, auto_offset_reset=AUTO_OFFSET_RESET):
        logger.info(f'EventConsumer {topic_name}, {bootstrap_servers}, {group_id}, {client_id}, {auto_offset_reset}')

        bootstrap_servers_str = ','.join(bootstrap_servers)
        cfg = {
            'bootstrap.servers': bootstrap_servers_str,
            'group.id': group_id,
            'auto.offset.reset': auto_offset_reset,
            'client.id': client_id
        }
        self.consumer = self.__create_kafka_consumer(cfg)

        self.topic = topic_name
        self.consumer.subscribe([topic_name])

        self.process_args = []
        self.process_kwargs = {}

    @staticmethod
    def __create_kafka_consumer(cfg):
        _consumer = None
        try:
            _consumer = Consumer(cfg)
            logger.info('The connection with Kafka has been established.')
        except Exception as ex:
            logger.error('Exception while connecting to Kafka')
            logger.error(ex)
            raise

        return _consumer

    async def process(self, message: str, *args, **kwargs):
        logger.warning('Not implemented.')

    async def consume_messages(self):
        logger.info(f'Starting messages consumption for {self.topic}')

        running = True
        while running:
            message = self.consumer.poll(POLL_TIMEOUT)

            if message is None:
                # logger.debug("no messages")
                pass
            elif message.error():
                logger.error('Consumer error: {}'.format(message.error()))
            else:
                logger.debug(
                    f'{message.topic()}:{message.partition()}:{message.offset()} key={message.key()}, value={message.value()}')
                await self.process(message.value().decode('utf-8'), *self.process_args, **self.process_kwargs)
                await asyncio.sleep(0)

            await asyncio.sleep(1)

        self.consumer.close()
