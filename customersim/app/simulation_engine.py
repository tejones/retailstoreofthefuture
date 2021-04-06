import asyncio
import json
import datetime
import random

from app import logger
from app.config import CUSTOMERS_AVERAGE_IN_STORE, CUSTOMER_ENTER_TOPIC, CUSTOMER_EXIT_TOPIC, CUSTOMER_MOVE_TOPIC
from app.domain_model import Store, Customer

CUSTOMER_STATE_TEMPLATE = '{0} is Entering. MDT: {1:0.1f}, C: {2:0.1f}, E: {3}'


class CustomerSimulator:
    def __init__(self, store: Store, customer_list: list, publisher,
                 next_entrance_time: datetime = datetime.datetime.now()):
        self.customer_list = customer_list
        self.store = store
        self.customer_queue = []  # List of customers in the store
        self.next_customer_entrance_time = next_entrance_time
        self.is_running = True
        self.mqttc = publisher

    def manage_customer_movements(self, c):
        if c.tick():
            if c.isExiting and c.currentLocation.x == 0 and c.currentLocation.y == 0:
                # remove the customer and signal the exit
                timestamp_value = self.get_timestamp_value(datetime.datetime.now())
                # TODO convert to pydantic model usage
                msg = {'id': str(c.id), 'ts': timestamp_value}
                # TODO simulation engine don't need to know details like topic name or message marshaling
                # it should be encapsulated in event publisher
                self.mqttc.publish(CUSTOMER_EXIT_TOPIC, json.dumps(msg))
                logger.info(f'{c.name} is Exiting.')
                self.customer_queue.remove(c)
            else:
                # signal move
                timestamp_value = self.get_timestamp_value(datetime.datetime.now())
                msg = {'id': str(c.id), 'ts': timestamp_value, 'x': c.currentLocation.x, 'y': c.currentLocation.y}
                self.mqttc.publish(CUSTOMER_MOVE_TOPIC, json.dumps(msg))

    async def run(self):
        # Check if any customers are due to enter, move, or exit. Sleep for one second, then repeat
        while self.is_running:
            if self.next_customer_entrance_time < datetime.datetime.now():
                # add the new customer, and signal the entrance
                new_customer_prototype = random.choice(self.customer_list)
                logger.info(f"new customer prototype {new_customer_prototype}")
                new_customer = Customer(self.store, new_customer_prototype['customer_id'],
                                        new_customer_prototype['name'])
                self.customer_queue.append(new_customer)

                timestamp = datetime.datetime.utcnow()
                timestamp_value = self.get_timestamp_value(timestamp)

                msg = {'id': str(new_customer.id), 'ts': timestamp_value}
                self.mqttc.publish(CUSTOMER_ENTER_TOPIC, json.dumps(msg))

                next_customer_entrance_time = self.get_new_entrance_time()

                logger.info('inspecting customer: ----------')
                logger.info(self.customer_state_dump(new_customer))
                logger.info(f'Next Customer Entering at {next_customer_entrance_time}')

            [self.manage_customer_movements(c) for c in self.customer_queue]
            await asyncio.sleep(1)

    @staticmethod
    def get_timestamp_value(tmstmp: datetime):
        # # For iso format use:
        # timestamp_value = f'"{timestamp.isoformat()}"'
        # For second since Epoch use:
        timestamp_value = int(tmstmp.timestamp())
        return timestamp_value

    @staticmethod
    def get_new_entrance_time():
        return datetime.datetime.now() + datetime.timedelta(0, random.uniform(1, 600 / CUSTOMERS_AVERAGE_IN_STORE))

    @staticmethod
    def customer_state_dump(c: Customer):
        return CUSTOMER_STATE_TEMPLATE.format(c.name, c.meanDwellTime, c.consistency, c.exitTime)
