import os
from app import logger
from app.config import get_bool_env, validate_and_crash, dump_constants

logger.info('Reading environment variables...')

ENTER_TOPIC = os.getenv('ENTER_TOPIC')
FOCUS_TOPIC = os.getenv('FOCUS_TOPIC')
COUPON_PREDICTION_TOPIC = os.getenv('COUPON_PREDICTION_TOPIC')
MQTT_HOST = os.getenv('MQTT_HOST')
MQTT_PORT = os.getenv('MQTT_PORT', 1881)
MQTT_USERNAME = os.getenv('MQTT_USERNAME')
MQTT_PASSWORD = os.getenv('MQTT_PASSWORD')
MQTT_BROKER_CERT_FILE = os.getenv('MQTT_BROKER_CERT_FILE')

COUPON_SCORER_URL = os.getenv('COUPON_SCORER_URL')
CLIENT_CONTEXT_URL = os.getenv('CLIENT_CONTEXT_URL', 'http://XXX')

TESTING_NO_MQTT = get_bool_env('TESTING_NO_MQTT', False)
TESTING_NO_POSTGRES = get_bool_env('TESTING_NO_POSTGRES', False)
TESTING_NO_SCORING_SERVICE = get_bool_env('TESTING_NO_POSTGRES', False)

DEPARTMENTS = ['Women', 'Boys', 'Sport', 'Girls', 'Men']

DB_NAME = os.getenv('DB_NAME')
DB_USER = os.getenv('DB_USER')
DB_PASSWORD = os.getenv('DB_PASSWORD')
DB_HOST = os.getenv('DB_HOST')
DB_PORT = os.getenv('DB_PORT')

MAX_COUPONS_PER_CALL = 5
PREDICTION_THRESHOLD = 0.2

HIDDEN_CONSTANTS_KEYS = ['DB_PASSWORD', 'MQTT_PASSWORD']
dump_constants(logger.info, HIDDEN_CONSTANTS_KEYS)

REQUIRED_PARAM_MESSAGE = 'Cannot read {} env variable. Please, make sure it is set before starting the service.'
validate_and_crash(logger.error, ENTER_TOPIC, REQUIRED_PARAM_MESSAGE.format('ENTER_TOPIC'))
validate_and_crash(logger.error, FOCUS_TOPIC, REQUIRED_PARAM_MESSAGE.format('FOCUS_TOPIC'))
validate_and_crash(logger.error, COUPON_PREDICTION_TOPIC, REQUIRED_PARAM_MESSAGE.format('COUPON_PREDICTION_TOPIC'))
validate_and_crash(logger.error, COUPON_SCORER_URL, REQUIRED_PARAM_MESSAGE.format('COUPON_SCORER_URL'))
validate_and_crash(logger.error, MQTT_HOST, REQUIRED_PARAM_MESSAGE.format('MQTT_HOST'))
validate_and_crash(logger.error, DB_HOST, REQUIRED_PARAM_MESSAGE.format('DB_HOST'))

logger.info("Environment variables read successfully.")
