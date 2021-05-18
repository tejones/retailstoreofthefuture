from typing import List, Tuple

from app.scenario.scenario_model import Scenario, Step


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

    async def get_events(self, unix_time: int) -> List[Tuple[str, Step]]:
        """

        :param unix_time:
        :return: list of tuples (customer_id, step)
        """
        raise NotImplementedError
