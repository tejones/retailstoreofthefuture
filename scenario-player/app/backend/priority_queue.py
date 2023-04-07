from queue import PriorityQueue
from typing import List, Tuple

from app import logger
from app.scenario.scenario_model import Scenario, Step


class PQueueTimelineBackend:
    def __init__(self):
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
        logger.info(f'add_to_timeline: {customer_id} {step} ')
        self.timeline.put((int(step.timestamp.timestamp()), (customer_id, step)))
        return True

    # XXX TODO probably wrong return type definition (Tuple[int, Tuple[str, Step])
    def peek(self) -> Tuple[str, Step]:
        return self.timeline.queue[0] if len(self.timeline.queue) > 0 else None

    async def get_events(self, unix_time: int, include_earlier: bool = False) -> List[Tuple[str, Step]]:
        logger.debug(f'get events for timestamp {unix_time}')
        earliest_element = self.peek()
        logger.debug(f'earliest_element: {earliest_element}')

        result = []
        # proceed, if the next element in the queue is "old enough" for our query
        if earliest_element and earliest_element[0] <= unix_time:
            # consume elements until we reach desired timestamp
            while True:
                element = self.timeline.get_nowait()
                print(element)
                print(type(element))
                if element[0] < unix_time:
                    if include_earlier:
                        result.append(element[1])
                else:
                    result.append(element[1])

                earliest_element = self.peek()
                # if there is no elements left or if the next element is too new, break
                if not earliest_element or earliest_element[0] > unix_time:
                    break

        return result
