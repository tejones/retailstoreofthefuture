from datetime import datetime
from typing import List, Tuple

from app.scenario.scenario_model import Scenario, Step, UtcDatetime


class BaseTimelineBackend:
    def __init__(self):
        """
        Initialize internal fields.
        """
        pass

    async def initialize(self):
        """
        Initialize the backend (for example, connect to the DB, etc.)
        :return:
        """
        pass

    async def store_scenario(self, scenario: Scenario):
        """
        Persist timeline metadata.
        :param scenario:
        :return:
        """
        raise NotImplementedError

    async def add_to_timeline(self, customer_id: str, step: Step):
        """
        Store info about given step for a given customer.
        :param customer_id:
        :param step:
        :return:
        """
        raise NotImplementedError

    @staticmethod
    def get_epoch_ms(timestamp: datetime):
        return int(timestamp.timestamp() * 1000)

    async def get_events(self, for_timestamp: UtcDatetime, from_timestamp: UtcDatetime, batch_size: int) -> List[Tuple[str, Step]]:
        """

        :param for_timestamp: timezone-aware datetime
        :param from_timestamp: timezone-aware datetime
        :param batch_size: number of events to return in one go
        :return: list of tuples (customer_id, step)
        """
        raise NotImplementedError
