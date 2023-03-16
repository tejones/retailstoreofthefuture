from fastapi_mqtt import MQTTConfig, FastMQTT
from gmqtt.mqtt.constants import MQTTv311
import ssl

from app import logger
from app.config import config
from app.mqtt.dummy_mqtt import DummyMQTT


def initialize_mqtt(fastapi_app):
    logger.info("Initializing MQTT...")
    if not config.TESTING_NO_MQTT:
        logger.info(f'MQTT host: {config.MQTT_HOST}:{config.MQTT_PORT} | user: {config.MQTT_USERNAME}')
        context = False
        if config.MQTT_BROKER_CERT_FILE is not None:
            context = ssl.SSLContext(ssl.PROTOCOL_TLSv1)
            context.load_verify_locations(config.MQTT_BROKER_CERT_FILE)
        mqtt_config = MQTTConfig(
            host=config.MQTT_HOST,
            port=config.MQTT_PORT,
            username=config.MQTT_USERNAME,
            password=config.MQTT_PASSWORD,
            # TODO XXX consider using MQTTv5 (parametrize this setting)
            version=MQTTv311,
            ssl=context)
        mqtt = FastMQTT(config=mqtt_config)
        mqtt.init_app(fastapi_app)

    else:
        logger.warning('MQTT is disabled (TESTING_NO_MQTT is set to True)')
        mqtt = DummyMQTT()

    return mqtt
