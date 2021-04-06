import os
import sys

from app import logger


def validate_and_crash(variable, message):
    if not variable:
        logger.error(message)
        sys.exit(message)


logger.info('Reading environment variables...')

STORE_HEIGHT = int(os.getenv('STORE_HEIGHT', 10))
STORE_WIDTH = int(os.getenv('STORE_WIDTH', 6))

CUSTOMERS_AVERAGE_IN_STORE = int(os.getenv('CUSTOMERS_AVERAGE_IN_STORE', 6))
CUSTOMERS_LIST_FILE = os.getenv('CUSTOMERS_LIST_FILE', 'customers.csv')

MQTT_HOST = os.getenv('MQTT_HOST')
MQTT_PORT = int(os.getenv('MQTT_PORT', 1883))
MQTT_NAME = os.getenv('MQTT_NAME', 'demoClient')

CUSTOMER_ENTER_TOPIC = os.getenv('ENTER_TOPIC', 'customer/enter')
CUSTOMER_EXIT_TOPIC = os.getenv('EXIT_TOPIC', 'customer/exit')
CUSTOMER_MOVE_TOPIC = os.getenv('MOVE_TOPIC', 'customer/move')

TESTING_MOCK_MQTT = os.getenv('TESTING_MOCK_MQTT', 'false')
TESTING_MOCK_MQTT = TESTING_MOCK_MQTT.lower() in ['1', 'yes', 'true']


REQUIRED_PARAM_MESSAGE = 'Cannot read {} env variable. Please, make sure it is set before starting the service.'
validate_and_crash(MQTT_HOST, REQUIRED_PARAM_MESSAGE.format('MQTT_HOST'))
