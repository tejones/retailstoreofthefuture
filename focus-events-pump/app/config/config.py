import os

from app import logger
from app.config import dump_constants, validate_and_crash, get_bool_env

logger.info('Reading environment variables...')

FOCUS_TOPIC = os.getenv('FOCUS_TOPIC')
MQTT_HOST = os.getenv('MQTT_HOST')
MQTT_PORT = os.getenv('MQTT_PORT', 1881)
MQTT_USERNAME = os.getenv('MQTT_USERNAME')
MQTT_PASSWORD = os.getenv('MQTT_PASSWORD')
MQTT_BROKER_CERT_FILE = os.getenv('MQTT_BROKER_CERT_FILE')

DB_NAME = os.getenv('DB_NAME')
DB_USER = os.getenv('DB_USER')
DB_PASSWORD = os.getenv('DB_PASSWORD')
DB_HOST = os.getenv('DB_HOST')
DB_PORT = os.getenv('DB_PORT')

TESTING_NO_MQTT = get_bool_env('TESTING_NO_MQTT', False)
TESTING_NO_POSTGRES = get_bool_env('TESTING_NO_POSTGRES', True)

# TODO: read from env
DEPARTMENTS = ['Women', 'Boys', 'Sport', 'Girls', 'Men']
MIN_CUSTOMER_ID = int(os.getenv('MIN_CUSTOMER_ID', 1))
MAX_CUSTOMER_ID = int(os.getenv('MAX_CUSTOMER_ID', 1000))
PERIODIC_TASKS_INTERVAL = float(os.getenv('PERIODIC_TASKS_INTERVAL', 1.0))

GENERATOR_AUTO_START = get_bool_env('GENERATOR_AUTO_START', True)

HIDDEN_CONSTANTS_KEYS = ['DB_PASSWORD', 'MQTT_PASSWORD']

dump_constants(logger.info, HIDDEN_CONSTANTS_KEYS)

REQUIRED_PARAM_MESSAGE = 'Cannot read {} env variable. Please, make sure it is set before starting the service.'

if not TESTING_NO_MQTT:
    validate_and_crash(logger.error, FOCUS_TOPIC, REQUIRED_PARAM_MESSAGE.format('FOCUS_TOPIC'))
    validate_and_crash(logger.error, MQTT_HOST, REQUIRED_PARAM_MESSAGE.format('MQTT_HOST'))

if not TESTING_NO_POSTGRES:
    validate_and_crash(logger.error, DB_HOST, REQUIRED_PARAM_MESSAGE.format('DB_HOST'))

logger.info("Environment variables read successfully.")
