import os
import sys

from app import logger


def validate_and_crash(variable, message):
    if not variable:
        logger.error(message)
        sys.exit(message)


logger.info('Reading environment variables...')

# XXX TODO make these parameters required again for production!
ENTRY_EVENT_TOPIC_NAME = os.getenv('ENTRY_EVENT_TOPIC_NAME')
FOCUS_EVENT_TOPIC_NAME = os.getenv('FOCUS_EVENT_TOPIC_NAME')
COUPON_PREDICTION_TOPIC_NAME = os.getenv('COUPON_PREDICTION_TOPIC_NAME')
MQTT_HOST = os.getenv('MQTT_HOST')
MQTT_PORT = os.getenv('MQTT_PORT', 1881)
MQTT_USERNAME = os.getenv('MQTT_USERNAME')
MQTT_PASSWORD = os.getenv('MQTT_PASSWORD')
MQTT_BROKER_CERT_FILE = os.getenv('MQTT_BROKER_CERT_FILE')

COUPON_SCORER_URL = os.getenv('COUPON_SCORER_URL')

TESTING_NO_MQTT = os.getenv('TESTING_NO_MQTT', 'false')
TESTING_NO_MQTT = TESTING_NO_MQTT.lower() in ['1', 'yes', 'true']
TESTING_NO_POSTGRES = os.getenv('TESTING_NO_POSTGRES', 'false')
TESTING_NO_POSTGRES = TESTING_NO_POSTGRES.lower() in ['1', 'yes', 'true']
TESTING_NO_SCORING_SERVICE = os.getenv('TESTING_NO_SCORING_SERVICE', 'false')
TESTING_NO_SCORING_SERVICE = TESTING_NO_SCORING_SERVICE.lower() in ['1', 'yes', 'true']

DEPARTMENTS = ['Women', 'Boys', 'Sport', 'Girls', 'Men']

DB_NAME = os.getenv('DB_NAME')
DB_USER = os.getenv('DB_USER')
DB_PASSWORD = os.getenv('DB_PASSWORD')
DB_HOST = os.getenv('DB_HOST')
DB_PORT = os.getenv('DB_PORT')

REQUIRED_PARAM_MESSAGE = 'Cannot read {} env variable. Please, make sure it is set before starting the service.'

validate_and_crash(ENTRY_EVENT_TOPIC_NAME, REQUIRED_PARAM_MESSAGE.format('ENTRY_EVENT_TOPIC_NAME'))
validate_and_crash(FOCUS_EVENT_TOPIC_NAME, REQUIRED_PARAM_MESSAGE.format('FOCUS_EVENT_TOPIC_NAME'))
validate_and_crash(COUPON_PREDICTION_TOPIC_NAME, REQUIRED_PARAM_MESSAGE.format('COUPON_PREDICTION_TOPIC_NAME'))
validate_and_crash(COUPON_SCORER_URL, REQUIRED_PARAM_MESSAGE.format('COUPON_SCORER_URL'))
validate_and_crash(MQTT_HOST, REQUIRED_PARAM_MESSAGE.format('MQTT_HOST'))
validate_and_crash(DB_HOST, REQUIRED_PARAM_MESSAGE.format('DB_HOST'))

MAX_COUPONS_PER_CALL = 5
PREDICTION_THRESHOLD = 0.2

logger.info("Environment variables read successfully.")
HIDDEN_CONSTANTS_KEYS = ['DB_PASSWORD', 'MQTT_PASSWORD']
CONSTANTS_KEYS = [k for k in globals().keys() if k[0].isupper()]
for k in CONSTANTS_KEYS:
    value = globals().get(k) if globals().get(k) else ''
    if k in HIDDEN_CONSTANTS_KEYS:
        value = len(value) * "*"
    logger.info(f'{k} = {value}')


# XXX TODO is context service used?
CLIENT_CONTEXT_URL = os.getenv('CLIENT_CONTEXT_URL', 'http://XXX')
