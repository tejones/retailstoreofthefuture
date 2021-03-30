from confluent_kafka import Producer

from app.utils import logger
from app.utils.config import CLIENT_ID, BOOTSTRAP_SERVERS


class EventProducer:
    def __init__(self, topic_name: str, bootstrap_servers=BOOTSTRAP_SERVERS, client_id: str = CLIENT_ID):
        logger.info(f'EventProducer {topic_name}, {bootstrap_servers}, {client_id}')

        bootstrap_servers_str = ','.join(bootstrap_servers)
        cfg = {
            'bootstrap.servers': bootstrap_servers_str,
            'client.id': client_id
        }
        self.producer = self._create_kafka_producer(cfg)

        self.topic = topic_name

    @staticmethod
    def _create_kafka_producer(config: dict):
        _producer = None
        try:
            _producer = Producer(config)
            logger.info('The connection with Kafka has been established.')
        except Exception as ex:
            logger.error('Exception while connecting to Kafka')
            logger.error(ex)
            raise

        return _producer

    def publish_message(self, value: str, key: str = None):
        logger.info(f'publish_message to topic {self.topic} with key {key}')
        logger.debug(value)
        try:
            # XXX TODO think about defining serializers for the producer
            if key:
                key = key.encode('utf-8')
            if value:
                value = value.encode('utf-8')

            # XXX TODO change to asynchronous call
            self.producer.produce(self.topic, value, key)
            self.producer.flush()
            logger.debug(f'Message {value} published.')
        except Exception as ex:
            logger.error(f'Exception in publishing message: {type(ex)} {ex}')
            # TODO propagate the exception?
            # raise
