from fastapi_mqtt import MQTTConfig, FastMQTT
from gmqtt.mqtt.constants import MQTTv311, MQTTv50
import ssl

from app import logger
from app.config import config
from app.config.config import MQTT_PROTOCOL_VERSION, MQTT_CLIENT_ID
from app.mqtt.dummy_mqtt import DummyMQTT


def initialize_mqtt(fastapi_app):
    logger.info("Initializing MQTT...")
    if not config.TESTING_NO_MQTT:
        logger.info(f'MQTT host: {config.MQTT_HOST}:{config.MQTT_PORT} | user: {config.MQTT_USERNAME}')
        context = False
        if config.MQTT_BROKER_CERT_FILE is not None:
            context = ssl.SSLContext(ssl.PROTOCOL_TLSv1)
            context.load_verify_locations(config.MQTT_BROKER_CERT_FILE)

        protocol_version = MQTTv311 if MQTT_PROTOCOL_VERSION == 'MQTTv311' else MQTTv50
        mqtt_config = MQTTConfig(
            host=config.MQTT_HOST,
            port=config.MQTT_PORT,
            username=config.MQTT_USERNAME,
            password=config.MQTT_PASSWORD,
            version=protocol_version,
            ssl=context)
        mqtt = FastMQTT(config=mqtt_config, client_id=MQTT_CLIENT_ID)
        mqtt.init_app(fastapi_app)

    else:
        logger.warning('MQTT is disabled (TESTING_NO_MQTT is set to True)')
        mqtt = DummyMQTT()

    return mqtt
