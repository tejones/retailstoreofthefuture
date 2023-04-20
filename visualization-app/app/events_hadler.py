import json

from app import logger
from app.config import CUSTOMER_EXIT_TOPIC, CUSTOMER_MOVE_TOPIC, CUSTOMER_ENTER_TOPIC, CUSTOMER_BROWSING_TOPIC
from app.data_models import Location
from app.events_model import CustomerEvent, CustomerEventExtended
from app.utils import find_customer

TOPIC_EVENT_TYPE_MAPPING = {
    f'{CUSTOMER_ENTER_TOPIC}': 'ENTER',
    f'{CUSTOMER_MOVE_TOPIC}': 'MOVE',
    f'{CUSTOMER_EXIT_TOPIC}': 'EXIT',
    f'{CUSTOMER_BROWSING_TOPIC}': 'BROWSING'
}


class EventsHandler:
    @staticmethod
    def handle_event(topic, payload, app_state):
        logger.debug(f'Handling event: {topic} - {payload}')
        payload = payload if type(payload) == str else payload.decode()
        cme = CustomerEvent.parse_raw(payload)
        customer = find_customer(cme.id, app_state.customers)
        event_type = TOPIC_EVENT_TYPE_MAPPING[topic]

        location = None
        if cme.x is not None and cme.y is not None:
            location = Location(x=cme.x, y=cme.y)

        cl = CustomerEventExtended(customer=customer, timestamp=cme.ts, event_type=event_type, location=location,
                                   department=cme.dep)

        app_state.customer_positions[cme.id] = {
            'customer': cl,
            'ws_consumers': []
        }
        return 0

    @staticmethod
    def handle_predictions(topic, payload, app_state):
        payload = payload.decode()
        cme = json.loads(payload)

        app_state.predictions[cme['customer']['id']] = cme
        return 0
