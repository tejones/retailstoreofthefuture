import os
import sys

from app import logger


def validate_and_crash(variable, message):
    if not variable:
        logger.error(message)
        sys.exit(message)


logger.info('Reading environment variables...')

CUSTOMERS_LIST_FILE = os.getenv('CUSTOMERS_LIST_FILE', 'app/resources/customers.json')
COUPONS_LIST_FILE = os.getenv('COUPONS_LIST_FILE', 'app/resources/coupons.json')

MQTT_HOST = os.getenv('MQTT_HOST')
MQTT_PORT = int(os.getenv('MQTT_PORT', 1883))
MQTT_NAME = os.getenv('MQTT_NAME', 'demoVisClient')
MQTT_USERNAME = os.getenv('MQTT_USERNAME', None)
MQTT_PASSWORD = os.getenv('MQTT_PASSWORD', None)
MQTT_BROKER_CERT_FILE = os.getenv('MQTT_BROKER_CERT_FILE', None)

CUSTOMER_ENTER_TOPIC = os.getenv('ENTER_TOPIC', 'customer/enter')
CUSTOMER_EXIT_TOPIC = os.getenv('EXIT_TOPIC', 'customer/exit')
CUSTOMER_MOVE_TOPIC = os.getenv('MOVE_TOPIC', 'customer/move')
CUSTOMER_BROWSING_TOPIC = os.getenv('BROWSING_TOPIC', 'customer/browsing')
COUPON_PREDICTION_TOPIC = os.getenv('COUPON_PREDICTION_TOPIC', 'customer/prediction')

SCENARIO_PLAYER_SCENARIO_ENDPOINT = os.getenv('SCENARIO_PLAYER_SCENARIO_ENDPOINT')

REQUIRED_PARAM_MESSAGE = 'Cannot read {} env variable. Please, make sure it is set before starting the service.'
validate_and_crash(SCENARIO_PLAYER_SCENARIO_ENDPOINT, REQUIRED_PARAM_MESSAGE.format('SCENARIO_PLAYER_SCENARIO_ENDPOINT'))
validate_and_crash(MQTT_HOST, REQUIRED_PARAM_MESSAGE.format('MQTT_HOST'))

logger.info("Environment variables read successfully.")
HIDDEN_CONSTANTS_KEYS = ['MQTT_PASSWORD']
CONSTANTS_KEYS = [k for k in globals().keys() if k[0].isupper()]
for k in CONSTANTS_KEYS:
    value = globals().get(k) if globals().get(k) else ''
    if k in HIDDEN_CONSTANTS_KEYS:
        value = len(value) * "*"
    logger.info(f'{k} = {value}')
