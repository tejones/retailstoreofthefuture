import os


MQTT_HOST = os.getenv('MQTT_HOST', 'localhost')
MQTT_PORT = int(os.getenv('MQTT_PORT', 1883))

CUSTOMER_ENTER_TOPIC = os.getenv('ENTER_TOPIC', 'customer/enter')
CUSTOMER_EXIT_TOPIC = os.getenv('EXIT_TOPIC', 'customer/exit')
CUSTOMER_MOVE_TOPIC = os.getenv('MOVE_TOPIC', 'customer/move')
CUSTOMER_BROWSING_TOPIC = os.getenv('BROWSING_TOPIC', 'customer/browsing')
COUPON_PREDICTION_TOPIC = os.getenv('COUPON_PREDICTION_TOPIC', 'customer/prediction')

MQTT_TOPICS = {
    'ENTER': CUSTOMER_ENTER_TOPIC,
    'EXIT': CUSTOMER_EXIT_TOPIC,
    'MOVE': CUSTOMER_MOVE_TOPIC,
    'BROWSING': CUSTOMER_BROWSING_TOPIC,
    'PREDICTION': COUPON_PREDICTION_TOPIC
}

SCENARIOS_PATH = os.getenv('SCENARIOS_PATH', './scenarios')
STEP_LENGTH = int(os.getenv('STEP_LENGTH', 1))
