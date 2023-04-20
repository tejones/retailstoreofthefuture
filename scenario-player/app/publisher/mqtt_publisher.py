import ssl
import uuid

from fastapi import FastAPI
from fastapi_mqtt import FastMQTT, MQTTConfig
from gmqtt.mqtt.constants import MQTTv311, MQTTv50

from app import logger
from app.config import TESTING_MOCK_MQTT, MQTT_HOST, MQTT_PORT, MQTT_CLIENT_ID, MQTT_USERNAME, MQTT_PASSWORD, \
    CUSTOMER_EXIT_TOPIC, CUSTOMER_MOVE_TOPIC, CUSTOMER_ENTER_TOPIC, MQTT_BROKER_CERT_FILE, MQTT_PROTOCOL_VERSION
from app.publisher.base import BaseEventPublisher
from app.publisher.mqtt_model import CustomerMoveEvent, CustomerEnterEvent, CustomerExitEvent
from app.scenario.scenario_model import CustomerState, STEP_TYPE_ENTER, STEP_TYPE_MOVE, STEP_TYPE_EXIT

MAP = {
    STEP_TYPE_ENTER: CUSTOMER_ENTER_TOPIC,
    STEP_TYPE_MOVE: CUSTOMER_MOVE_TOPIC,
    STEP_TYPE_EXIT: CUSTOMER_EXIT_TOPIC
}

if TESTING_MOCK_MQTT:
    class MQTTClient:
        def __init__(self, app: FastAPI, mqtt_host: str, mqtt_port: int, mqtt_client_name: str):
            logger.warning(f'simulating an MQTT client to {mqtt_host}')
            self.mqtt_client_name = mqtt_client_name
            self.mqtt_host = mqtt_host
            self.mqtt_port = mqtt_port
            self.app = app

        def publish(self, topic, message):
            logger.info(f'simulated publishing to {topic}. message: {message}')

        async def connect(self):
            pass

        async def set_connection_handlers(self, user_connect_handler, on_disconnect):
            pass
else:
    class MQTTClient:
        def __init__(self, app: FastAPI, mqtt_host: str, mqtt_port: int, mqtt_client_name: str):
            logger.info(f'Creating MQTT client {mqtt_host}, {mqtt_port}, {mqtt_client_name}')
            self.mqtt_client_name = mqtt_client_name
            self.mqtt_host = mqtt_host
            self.mqtt_port = mqtt_port
            self.app = app

            # SSL
            context = False

            if MQTT_BROKER_CERT_FILE is not None:
                context = ssl.SSLContext(ssl.PROTOCOL_TLSv1)
                context.load_verify_locations(MQTT_BROKER_CERT_FILE)

            protocol_version = MQTTv311 if MQTT_PROTOCOL_VERSION == 'MQTTv311' else MQTTv50
            # use unique postfix in case of many instances of the same service
            client_id = f'{self.mqtt_client_name}_{uuid.uuid4()}'
            mqtt_config = MQTTConfig(host=self.mqtt_host, port=self.mqtt_port, username=MQTT_USERNAME,
                                     password=MQTT_PASSWORD, version=protocol_version, ssl=context)
            self.fast_mqtt = FastMQTT(config=mqtt_config, client_id=client_id)

        def publish(self, topic, message):
            logger.debug(f' publishing to {topic}. message: {message}')
            return self.fast_mqtt.publish(topic, message)

        async def connect(self):
            logger.info("before connect")

            self.fast_mqtt.init_app(self.app)
            logger.info("after connect")

        async def set_connection_handlers(self, user_connect_handler, on_disconnect):
            self.fast_mqtt.user_connect_handler = user_connect_handler
            self.fast_mqtt.client.on_disconnect = on_disconnect


class MQTTEventMarshaller(object):
    @staticmethod
    def construct_entry_message(cs: CustomerState):
        message = CustomerEnterEvent(id=cs.customer_description.customer_id, ts=int(cs.timestamp.timestamp()))
        return message.json()

    @staticmethod
    def construct_move_message(cs: CustomerState):
        ts = int(cs.timestamp.timestamp())
        message = CustomerMoveEvent(id=cs.customer_description.customer_id, ts=ts, x=cs.location.x, y=cs.location.y)
        return message.json()

    @staticmethod
    def construct_exit_message(cs: CustomerState):
        message = CustomerExitEvent(id=cs.customer_description.customer_id, ts=int(cs.timestamp.timestamp()))
        return message.json()


class MQTTEventPublisher(BaseEventPublisher):
    def __init__(self, app: FastAPI, mqtt_host=MQTT_HOST, mqtt_port=MQTT_PORT, mqtt_client_name=MQTT_CLIENT_ID):
        logger.info(f'Initializing MQTT client {mqtt_host}')
        self.app = app
        self.client = MQTTClient(app, mqtt_host, mqtt_port, mqtt_client_name)

    async def initialize(self):
        logger.info('Initializing MQTT connection')
        await self.client.set_connection_handlers(MQTTEventPublisher.on_connect, MQTTEventPublisher.on_disconnect)

        await self.client.connect()

    @staticmethod
    def on_connect(client, flags, rc, properties):
        logger.warning(f'Connected: , {client}, {flags}, {rc}, {properties}')

    @staticmethod
    def on_disconnect(client, packet):
        logger.warning(f'Disconnected: {client}, {packet}')

    @staticmethod
    def get_topic_for_event_type(event_type):
        return MAP[event_type]

    def prepare_payload(self, customer_state: CustomerState):

        if customer_state.status == STEP_TYPE_ENTER:
            message = MQTTEventMarshaller.construct_entry_message(customer_state)
        elif customer_state.status == STEP_TYPE_MOVE:
            message = MQTTEventMarshaller.construct_move_message(customer_state)
        elif customer_state.status == STEP_TYPE_EXIT:
            message = MQTTEventMarshaller.construct_exit_message(customer_state)
        else:
            raise RuntimeError(f'Unknown message type ({customer_state.status})')

        return message

    async def publish_state(self, customer_state: CustomerState):
        logger.debug('publish_state')
        topic = self.get_topic_for_event_type(customer_state.status)
        logger.debug(f'Publishing {customer_state} to {topic} topic')
        message = self.prepare_payload(customer_state)
        self.client.publish(topic, message)
