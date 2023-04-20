from fastapi_mqtt import MQTTConfig, FastMQTT
from gmqtt.mqtt.constants import MQTTv311, MQTTv50
import ssl

from app import logger
from app.config.config import TESTING_NO_MQTT, MQTT_BROKER_CERT_FILE, MQTT_HOST, MQTT_PORT, MQTT_USERNAME, \
    MQTT_PASSWORD, MQTT_PROTOCOL_VERSION, MQTT_CLIENT_ID
from app.mqtt.dummy_mqtt import DummyMQTT


def initialize_mqtt(fastapi_app):

    if not TESTING_NO_MQTT:
        logger.debug(f'MQTT host: {MQTT_HOST}:{MQTT_PORT} | user: {MQTT_USERNAME}')
        context = False
        if MQTT_BROKER_CERT_FILE is not None:
            context = ssl.SSLContext(ssl.PROTOCOL_TLSv1)
            context.load_verify_locations(MQTT_BROKER_CERT_FILE)
        protocol_version = MQTTv311 if MQTT_PROTOCOL_VERSION == 'MQTTv311' else MQTTv50
        mqtt_config = MQTTConfig(
            host=MQTT_HOST,
            port=MQTT_PORT,
            username=MQTT_USERNAME,
            password=MQTT_PASSWORD,
            version=protocol_version,
            ssl=context)
        mqtt = FastMQTT(config=mqtt_config, client_id=MQTT_CLIENT_ID)
        mqtt.init_app(fastapi_app)

    else:
        mqtt = DummyMQTT()

    return mqtt
