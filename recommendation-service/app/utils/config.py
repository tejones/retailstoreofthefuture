import os
import sys

from app.utils import logger


def validate_and_crash(variable, message):
    if not variable:
        logger.error(message)
        sys.exit(message)


logger.info('Reading environment variables...')

BOOTSTRAP_SERVERS = os.getenv('BOOTSTRAP_SERVERS', '127.0.0.1:9092')
BOOTSTRAP_SERVERS = [x.strip() for x in BOOTSTRAP_SERVERS.split(',')]

CLIENT_ID = os.getenv('CLIENT_ID', 'kafkaClients')

# XXX TODO make these parameters required again for production!
GROUP_ID = os.getenv('GROUP_ID')
ENTRY_EVENT_TOPIC_NAME = os.getenv('ENTRY_EVENT_TOPIC_NAME')
FOCUS_EVENT_TOPIC_NAME = os.getenv('FOCUS_EVENT_TOPIC_NAME')
COUPON_PREDICTION_TOPIC_NAME = os.getenv('COUPON_PREDICTION_TOPIC_NAME')

AUTO_OFFSET_RESET = os.getenv('AUTO_OFFSET_RESET', 'latest')
POLL_TIMEOUT = float(os.getenv('POLL_TIMEOUT', 0.1))

# XXX TODO add to required parameters
COUPON_SCORER_URL = os.getenv('COUPON_SCORER_URL', 'http://127.0.0.1:8001/score')
CLIENT_CONTEXT_URL = os.getenv('CLIENT_CONTEXT_URL', 'http://XXX')

TESTING_NO_KAFKA = os.getenv('TESTING_NO_KAFKA', 'false')
TESTING_NO_KAFKA = TESTING_NO_KAFKA.lower() in ['1', 'yes', 'true']
TESTING_NO_POSTGRES = os.getenv('TESTING_NO_POSTGRES', 'false')
TESTING_NO_POSTGRES = TESTING_NO_POSTGRES.lower() in ['1', 'yes', 'true']

DEPARTMENTS = ['Women', 'Boys', 'Sport', 'Girls', 'Men']

DB_NAME = os.getenv('DB_NAME')
DB_USER = os.getenv('DB_USER')
DB_PASSWORD = os.getenv('DB_PASSWORD')
DB_HOST = os.getenv('DB_HOST')
DB_PORT = os.getenv('DB_PORT')


REQUIRED_PARAM_MESSAGE = 'Cannot read {} env variable. Please, make sure it is set before starting the service.'

validate_and_crash(BOOTSTRAP_SERVERS, REQUIRED_PARAM_MESSAGE.format('BOOTSTRAP_SERVERS'))
validate_and_crash(ENTRY_EVENT_TOPIC_NAME, REQUIRED_PARAM_MESSAGE.format('ENTRY_EVENT_TOPIC_NAME'))
validate_and_crash(FOCUS_EVENT_TOPIC_NAME, REQUIRED_PARAM_MESSAGE.format('FOCUS_EVENT_TOPIC_NAME'))
validate_and_crash(COUPON_PREDICTION_TOPIC_NAME, REQUIRED_PARAM_MESSAGE.format('COUPON_PREDICTION_TOPIC_NAME'))
validate_and_crash(COUPON_SCORER_URL, REQUIRED_PARAM_MESSAGE.format('COUPON_SCORER_URL'))
validate_and_crash(GROUP_ID, REQUIRED_PARAM_MESSAGE.format('GROUP_ID'))

MAX_COUPONS_PER_CALL = 5
PREDICTION_THRESHOLD = 0.2
