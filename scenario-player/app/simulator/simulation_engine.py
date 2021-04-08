import asyncio
from datetime import datetime, timezone

from app import logger
from app.backend.base import BaseTimelineBackend
from app.publisher.base import BaseEventPublisher
from app.scenario.scenario_model import CustomerDescription, CustomerState, Step

CUSTOMER_STATE_TEMPLATE = '{0} is Entering. MDT: {1:0.1f}, C: {2:0.1f}, E: {3}'


class CustomerSimulator:
    def __init__(self, backend: BaseTimelineBackend, event_publisher: BaseEventPublisher,
                 start_time: datetime = datetime.now(timezone.utc)):
        self.tick_time = start_time
        self.last_tick_time: int = 0
        self.backend = backend
        self.event_publisher = event_publisher
        self.is_running = True

    @staticmethod
    def create_customer_state(customer_id, step: Step):
        customer_description = CustomerDescription(customer_id=customer_id)
        return CustomerState(customer_description=customer_description, location=step.location,
                             timestamp=step.timestamp, status=step.type)

    async def run(self):
        logger.info('Starting simulator loop')
        while self.is_running:
            logger.debug('another pass of simulator loop...')
            tmpstmp = int(datetime.now(timezone.utc).timestamp())

            # TODO get_events returns the events and REMOVES them from the queue, maybe change name to consume_events
            # TODO maybe it should be: get events from the last tick 'till now
            events_for_users = await self.backend.get_events(tmpstmp)
            logger.debug(f'events: {events_for_users}')

            customer_states = [self.create_customer_state(efo[0], efo[1]) for efo in events_for_users]
            for state in customer_states:
                await self.event_publisher.publish_state(state)

            # remember last tick time
            self.last_tick_time = tmpstmp

            # go to sleep
            await asyncio.sleep(1)
