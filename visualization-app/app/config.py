import os
import uuid

from app import logger, validate_and_crash, dump_constants

logger.info('Reading environment variables...')

CUSTOMERS_LIST_FILE = os.getenv('CUSTOMERS_LIST_FILE', 'app/resources/customers.json')
COUPONS_LIST_FILE = os.getenv('COUPONS_LIST_FILE', 'app/resources/coupons.json')

MQTT_HOST = os.getenv('MQTT_HOST')
MQTT_PORT = int(os.getenv('MQTT_PORT', 1883))
MQTT_CLIENT_ID = os.getenv('MQTT_CLIENT_ID', 'demoVisClient')
MQTT_CLIENT_ID = f'{MQTT_CLIENT_ID}_{uuid.uuid4()}'
MQTT_USERNAME = os.getenv('MQTT_USERNAME', None)
MQTT_PASSWORD = os.getenv('MQTT_PASSWORD', None)
MQTT_BROKER_CERT_FILE = os.getenv('MQTT_BROKER_CERT_FILE', None)
# use 'MQTTv311' if your broker does not support MQTTv5
MQTT_PROTOCOL_VERSION = os.getenv('MQTT_PROTOCOL_VERSION', 'MQTTv5')

CUSTOMER_ENTER_TOPIC = os.getenv('ENTER_TOPIC', 'customer/enter')
CUSTOMER_EXIT_TOPIC = os.getenv('EXIT_TOPIC', 'customer/exit')
CUSTOMER_MOVE_TOPIC = os.getenv('MOVE_TOPIC', 'customer/move')
CUSTOMER_BROWSING_TOPIC = os.getenv('BROWSING_TOPIC', 'customer/browsing')
COUPON_PREDICTION_TOPIC = os.getenv('COUPON_PREDICTION_TOPIC', 'customer/prediction')

SCENARIO_PLAYER_SCENARIO_ENDPOINT = os.getenv('SCENARIO_PLAYER_SCENARIO_ENDPOINT')

HIDDEN_CONSTANTS_KEYS = ['MQTT_PASSWORD']
dump_constants(logger.info, HIDDEN_CONSTANTS_KEYS)

REQUIRED_PARAM_MESSAGE = 'Cannot read {} env variable. Please, make sure it is set before starting the service.'
validate_and_crash(logger.error, SCENARIO_PLAYER_SCENARIO_ENDPOINT, REQUIRED_PARAM_MESSAGE.format('SCENARIO_PLAYER_SCENARIO_ENDPOINT'))
validate_and_crash(logger.error, MQTT_HOST, REQUIRED_PARAM_MESSAGE.format('MQTT_HOST'))

logger.info("Environment variables read successfully.")
