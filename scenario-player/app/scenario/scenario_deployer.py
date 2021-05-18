from datetime import datetime

from app import logger
from app.backend.base import BaseTimelineBackend
from app.scenario.scenario_model import Scenario


class ScenarioDeployer(object):
    def __init__(self, backend: BaseTimelineBackend):
        logger.info(f'Initializing ScenarioDeployer')
        self.backend = backend

    @staticmethod
    def recalculate_time(scenario: Scenario, start_time: datetime):
        logger.info(f'recalculate_time {scenario} (start from {start_time}')

        new_scenario = Scenario(customer=scenario.customer, path=[])

        first_timestamp = scenario.path[0].timestamp
        time_delta = start_time - first_timestamp

        # go trough draft steps
        for s in scenario.path:
            step = s.copy()
            step.timestamp = s.timestamp + time_delta

            # add the step to the new scenario
            new_scenario.path.append(step)

        return new_scenario

    async def deploy_scenario(self, scenario: Scenario):
        logger.info(f'deploy_scenario {scenario}')

        # go trough draft steps
        for step in scenario.path:
            await self.backend.add_to_timeline(scenario.customer.customer_id, step)

        return True
