from kafka import KafkaProducer

from app.utils import logger
from app.utils.config import CLIENT_ID, BOOTSTRAP_SERVERS


class EventProducer:
    def __init__(self, topic_name: str, bootstrap_servers=BOOTSTRAP_SERVERS, client_id: str = CLIENT_ID):
        logger.info(f'EventProducer {topic_name}, {bootstrap_servers}, {client_id}')
        self.producer = self._create_kafka_producer()

        self.topic = topic_name

    @staticmethod
    def _create_kafka_producer(bootstrap_servers=BOOTSTRAP_SERVERS, client_id: str = CLIENT_ID):
        _producer = None
        try:
            _producer = KafkaProducer(bootstrap_servers=bootstrap_servers, client_id=client_id)
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
            self.producer.send(self.topic, value, key)
            logger.debug(f'Message {value} published.')
        except Exception as ex:
            logger.error(f'Exception in publishing message: {type(ex)} {ex}')
            # TODO propagate the exception?
            # raise
