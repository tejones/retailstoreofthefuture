from datetime import datetime, timezone

from app import logger
from app.backend.base import BaseTimelineBackend
from app.scenario.scenario_deployer import ScenarioDeployer
from app.scenario.scenario_model import Scenario
from app.scenario.scenario_producer import ScenarioProducer
from app.simulator.simulation_engine import CustomerSimulator


class TimelineController:
    def __init__(self, backend: BaseTimelineBackend, scenario_producer: ScenarioProducer,
                 scenario_deployer: ScenarioDeployer, autostart=True):
        self.backend = backend
        self.scenario_producer = scenario_producer
        self.scenario_deployer = scenario_deployer
        self.autostart = autostart

    async def accept_scenario_draft(self, scenario: Scenario):
        logger.info("Converting draft to scenario...")

        result = self.scenario_producer.expand(scenario)

        await self.backend.store_scenario(result)
        if self.autostart:
            await self.deploy_scenario(result)

        return result.json(exclude_none=True)

    async def deploy_scenario(self, scenario: Scenario, recalculate_time: bool = False):
        logger.info('Deploying scenario...')

        if recalculate_time:
            logger.debug('Recalculating scenario time...')
            new_start = datetime.now(timezone.utc)
            scenario = self.scenario_deployer.recalculate_time(scenario, new_start)
        # persist the scenario
        await self.backend.store_scenario(scenario)

        # add scenario steps to the timeline
        result = await self.scenario_deployer.deploy_scenario(scenario)
        return result

    async def get_current_state(self, timestamp: datetime):
        logger.info(f'get_current_state({timestamp}):')
        events_for_users = await self.backend.get_events(timestamp)
        logger.debug(f'events: {events_for_users}')


        customer_states = [CustomerSimulator.create_customer_state(efo[0], efo[1]) for efo in events_for_users]

        return customer_states
