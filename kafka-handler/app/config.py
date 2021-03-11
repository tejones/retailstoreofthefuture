import os


KAFKA_BROKER = os.getenv('KAFKA_BROKER', '0.0.0.0:9092')
KAFKA_USER_ID = os.getenv('KAFKA_USER_ID', 'Lusi')
KAFKA_TOPIC_NAME = os.getenv('KAFKA_TOPIC_NAME', 'cos')