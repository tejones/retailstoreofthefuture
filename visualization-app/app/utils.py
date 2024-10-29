import ssl

from fastapi_mqtt import MQTTConfig, FastMQTT
from gmqtt.mqtt.constants import MQTTv311, MQTTv50

from app import logger
from app.config import MQTT_HOST, MQTT_PORT, MQTT_USERNAME, MQTT_BROKER_CERT_FILE, MQTT_PROTOCOL_VERSION, MQTT_PASSWORD, \
    MQTT_CLIENT_ID


def find_customer(customer_id, customers):
    customer_id = int(customer_id)
    if len(customers) >= customer_id and int(customers[customer_id - 1].customer_id) == customer_id:
        return customers[customer_id - 1]
    for customer in customers:
        if customer_id == customer.customer_id:
            return customer

    logger.warning(f'Customer {customer_id} not found in customers list')
    return None


def initialize_mqtt(fastapi_app):
    logger.info(f'MQTT host: {MQTT_HOST}:{MQTT_PORT} | user: {MQTT_USERNAME}')
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

    return mqtt
