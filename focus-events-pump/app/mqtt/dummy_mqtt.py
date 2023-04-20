from typing import Callable

from app import logger


class DummyMQTT:

    def __init__(self):
        logger.warning('- ' * 20)
        logger.warning('')
        logger.warning('Initializing Dummy MQTT connection.')
        logger.warning('')
        logger.warning('- ' * 20)

    def subscribe(self, *topics):
        def func(handler: Callable) -> Callable:
            logger.info(f'Dummy MQTT subscribe to {topics}')
            return handler
        return func

    def publish(self, topic, payload):
        logger.info('Dummy MQTT publishing message:')
        logger.info(f'Topic: {topic}; Message: {payload}')
        return {
            'topic': topic,
            'payload': payload
        }
