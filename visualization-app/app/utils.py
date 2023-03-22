import ssl

from fastapi_mqtt import MQTTConfig, FastMQTT
from gmqtt.mqtt.constants import MQTTv311, MQTTv50

from app import logger, config


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
    logger.info(f'MQTT host: {config.MQTT_HOST}:{config.MQTT_PORT} | user: {config.MQTT_USERNAME}')
    context = False
    if config.MQTT_BROKER_CERT_FILE is not None:
        context = ssl.SSLContext(ssl.PROTOCOL_TLSv1)
        context.load_verify_locations(config.MQTT_BROKER_CERT_FILE)
    protocol_version = MQTTv311 if config.MQTT_PROTOCOL_VERSION == 'MQTTv311' else MQTTv50
    mqtt_config = MQTTConfig(
        host=config.MQTT_HOST,
        port=config.MQTT_PORT,
        username=config.MQTT_USERNAME,
        password=config.MQTT_PASSWORD,
        version=protocol_version,
        ssl=context)
    mqtt = FastMQTT(config=mqtt_config)
    mqtt.init_app(fastapi_app)

    return mqtt
