import math
from datetime import datetime, timedelta, timezone

from app import logger
from app.scenario.scenario_model import Scenario, Step, Location, STEP_TYPE_MOVE, STEP_TYPE_FOCUS

CUSTOMER_AVERAGE_PACE = 0.03  # seconds per space unit
# XXX TODO: the speed per unit should be determined by the map size...

SCENARIO_AUTOSTART_DELAY = 10


class ScenarioProducer(object):
    def __init__(self, store_map=None):
        logger.info(f'Initializing ScenarioProducer with map {store_map}')
        self.map = store_map

    def expand(self, scenario_draft: Scenario, start_timestamp=None):
        logger.info(f'Expanding scenario {scenario_draft}')
        if not start_timestamp:
            start_timestamp = datetime.now(timezone.utc)
            if SCENARIO_AUTOSTART_DELAY:
                start_timestamp = start_timestamp + timedelta(seconds=SCENARIO_AUTOSTART_DELAY)

        # create new scenario
        scenario = Scenario(customer=scenario_draft.customer, path=[])

        last_step = None

        # go through draft's steps
        for i, s in enumerate(scenario_draft.path):
            step = s.copy(update={'type': STEP_TYPE_MOVE})
            step.timestamp = self.compute_timestamp(last_step, s) if last_step else start_timestamp

            # add the step to the new scenario
            scenario.path.append(step)

            # remember last step
            last_step = step

            if s.type.upper() == STEP_TYPE_FOCUS:
                additional_steps = self.generate_additional_steps(last_step, count=5, period=30)
                scenario.path.extend(additional_steps)
                last_step = additional_steps[-1]

        return scenario

    def compute_timestamp(self, previous_step: Step, current_step: Step,
                          customer_pace: float = CUSTOMER_AVERAGE_PACE) -> datetime:
        logger.debug(f'compute_timestamp {previous_step}, {current_step}')
        distance = self.get_distance(previous_step.location, current_step.location)
        elapsed_time = distance * customer_pace
        return previous_step.timestamp + timedelta(seconds=elapsed_time)

    def get_distance(self, l1: Location, l2: Location):
        # In the future, use map and path finding to find distance
        # for now use cartesian distance

        return math.dist([l1.x, l1.y], [l2.x, l2.y])

    def generate_additional_steps(self, previous_step: Step, count: int, period: float):
        """
        :param previous_step:
        :param count: how many steps to produce
        :param period: [seconds] the period to fill with the steps (time from the previous step to the last step)
        :return:
        """
        assert count >= 1

        time_delta = period / (count - 1)

        result = []
        previous_timestamp = previous_step.timestamp
        previous_location = previous_step.location
        for i in range(0, count):
            # TODO: add some movement around the same place (for example move left then right, then left
            new_location = previous_location
            new_timestamp = previous_timestamp + timedelta(seconds=time_delta)

            result.append(Step(type=STEP_TYPE_MOVE, location=new_location, timestamp=new_timestamp))
            previous_timestamp = new_timestamp
            previous_location = new_location

        return result
