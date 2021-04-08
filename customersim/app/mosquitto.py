from paho.mqtt import client

from app import logger
from app.config import TESTING_MOCK_MQTT, MQTT_HOST, MQTT_PORT, MQTT_NAME

if TESTING_MOCK_MQTT:
    class MQTTClient:
        def __init__(self, mqtt_host: str, mqtt_port: int, mqtt_client_name: str):
            logger.info(f'simulating a client to {mqtt_host}')
            self.mqtt_client_name = mqtt_client_name
            self.mqtt_host = mqtt_host
            self.mqtt_port = mqtt_port

        def publish(self, topic, message):
            logger.info(f'simulated publishing to {topic}. message: {message}')

        async def connect(self):
            pass
else:
    class MQTTClient:
        def __init__(self, mqtt_host: str, mqtt_port: int, mqtt_client_name: str):

            logger.info(f'Creating MQTT client {mqtt_host}, {mqtt_port}, {mqtt_client_name}')
            self.mqtt_client_name = mqtt_client_name
            self.mqtt_host = mqtt_host
            self.mqtt_port = mqtt_port

        def publish(self, topic, message):
            logger.info(f' publishing to {topic}. message: {message}')
            return self.mqttc.publish(topic, message)

        async def connect(self):
            logger.info("before connect")
            self.mqttc = client.Client(self.mqtt_client_name)
            logger.info(f'connect({self.mqtt_host}, {self.mqtt_port})')
            self.mqttc.connect(self.mqtt_host, self.mqtt_port)
            logger.info("after connect")


async def get_mqtt_client():
    mqttc = MQTTClient(MQTT_HOST, MQTT_PORT, MQTT_NAME)
    await mqttc.connect()
    return mqttc
