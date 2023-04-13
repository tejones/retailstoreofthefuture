from queue import PriorityQueue
from typing import List, Tuple

from app import logger
from app.backend.base import BaseTimelineBackend
from app.scenario.scenario_model import Scenario, Step, UtcDatetime


class PQueueTimelineBackend(BaseTimelineBackend):
    def __init__(self):
        super().__init__()
        logger.info('Initializing PriorityQueue backend...')
        self.timeline = PriorityQueue()
        self.scenarios = {}

    async def initialize(self):
        pass

    async def store_scenario(self, scenario: Scenario):
        logger.info('store_scenario')
        scenario_key = f'{scenario.customer.customer_id}'
        self.scenarios.update({scenario_key: scenario})
        return scenario_key

    async def add_to_timeline(self, customer_id: str, step: Step):
        logger.debug(f'add_to_timeline: {customer_id} {step} {step.timestamp.isoformat()}')
        self.timeline.put((int(self.get_epoch_ms(step.timestamp)), (customer_id, step)))
        return True

    def peek(self) -> Tuple[int, Tuple[str, Step]]:
        return self.timeline.queue[0] if len(self.timeline.queue) > 0 else None

    async def get_events(self, for_timestamp: UtcDatetime, from_timestamp: UtcDatetime,
                         batch_size: int) -> List[Tuple[str, Step]]:
        logger.info(f'get events for timestamp {for_timestamp}')
        include_earlier = True

        earliest_element = self.peek()  # just for debugging; actual peeking is done in the loop
        min, epoch = self.get_epoch_ms(from_timestamp), self.get_epoch_ms(for_timestamp)
        logger.info(f'min: {min}; max: {epoch}; earliest element: {earliest_element}')

        result = []
        consumed_elements = 0

        # PriorityQueue class has no methods for getting an element by its priority.
        # (It is only capable of getting an element with the lowest priority.)
        # We need to do it "manually".

        # repeat if the queue is not empty and the earliest element is not too new
        while (earliest_element := self.peek()) and earliest_element[0] <= epoch and consumed_elements < batch_size:
            element = self.timeline.get_nowait()
            element_timestamp = element[0]

            # skip elements that are too old (they should be already consumed)
            if element_timestamp < min:
                if include_earlier:
                    result.append(element[1])
            # include elements that are not to new
            elif element_timestamp <= epoch:
                result.append(element[1])

                consumed_elements += 1

        logger.info(f'consumed_elements: {consumed_elements}')
        return result
