from .config import KAFKA_BROKER, KAFKA_USER_ID
from kafka import KafkaProducer
from kafka.admin import KafkaAdminClient, NewTopic


class Producer:
    
    
    def __init__(self):
        self.producer = self._create_kafka_producer()
        self.admin_client = self._create_kafka_admin_client(KAFKA_USER_ID)
        self.topic_list = []


    def create_topic(self, topic_name):
        self.topic_list.append(NewTopic(name=topic_name, num_partitions=1, replication_factor=1))
        self.admin_client.create_topics(new_topics=self.topic_list, validate_only=False)


    def publish_message(self, topic_name, key, value):
        try:
            key_bytes = bytes(key, encoding='utf-8')
            value_bytes = bytes(value, encoding='utf-8')
            self.producer.send(topic_name, key=key_bytes, value=value_bytes)
            self.producer.flush()
            print('Message published successfully.')
        except Exception as ex:
            print('Exception in publishing message')


    def _create_kafka_producer(self):
        _producer = None
        try:
            _producer = KafkaProducer(bootstrap_servers=[KAFKA_BROKER], api_version=(0, 10))
            print('The connection with Kafka has been established.')
        except Exception as ex:
            print('Exception while connecting Kafka')
        finally:
            return _producer


    def _create_kafka_admin_client(self, client_ID):
        _admin_client = None
        try:
            _admin_client = KafkaAdminClient(bootstrap_servers=KAFKA_BROKER, client_id=client_ID)
            print('The connection with Kafka has been established.')
        except Exception as ex:
            print('Exception while connecting Kafka')
        finally:
            return _admin_client
