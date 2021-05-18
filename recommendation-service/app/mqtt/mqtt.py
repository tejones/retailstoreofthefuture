from fastapi_mqtt import MQTTConfig, FastMQTT
from gmqtt.mqtt.constants import MQTTv311
import ssl

from app import logger
from app.config import config
from app.mqtt.dummy_mqtt import DummyMQTT


def initialize_mqtt(fastapi_app):

    if not config.TESTING_NO_MQTT:
        logger.debug(f'MQTT host: {config.MQTT_HOST}:{config.MQTT_PORT} | user: {config.MQTT_USERNAME}')
        context = False
        if config.MQTT_BROKER_CERT_FILE is not None:
            context = ssl.SSLContext(ssl.PROTOCOL_TLSv1)
            context.load_verify_locations(config.MQTT_BROKER_CERT_FILE)
        mqtt_config = MQTTConfig(
            host=config.MQTT_HOST,
            port=config.MQTT_PORT,
            username=config.MQTT_USERNAME,
            password=config.MQTT_PASSWORD,
            version=MQTTv311,
            ssl=context)
        mqtt = FastMQTT(config=mqtt_config)
        mqtt.init_app(fastapi_app)

    else:
        mqtt = DummyMQTT()

    return mqtt
