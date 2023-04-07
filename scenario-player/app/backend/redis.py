from datetime import datetime
from typing import List, Tuple

import aioredis

from app import logger
from app.backend.base import BaseTimelineBackend
from app.scenario.scenario_model import Scenario, Step, Location

TIMELINE_KEY = f'TIMELINE:CURRENT'
SCENARIO_KEY = 'SCENARIO'
TIMESTAMP_FORMAT = '%Y-%m-%d %H:%M:%S.%f%z'


class RedisTimelineBackend(BaseTimelineBackend):

    def __init__(self, connection_url: str = 'redis://localhost', database: int = 0, redis_password: str = None):
        """
        Initialize internal fields.
        """
        super().__init__()
        self.connection_url = connection_url
        self.database = database
        self.redis_password = redis_password
        self.redis = None

    async def initialize(self):
        """
        Initialize the backend (for example, connect to the DB, etc.)
        :return:
        """
        logger.info("Connecting to Redis...")
        logger.info(f'{self.connection_url}, {self.database},{self.redis_password}')
        try:
            self.redis = await aioredis.create_redis_pool(address=self.connection_url, db=self.database,
                                                          password=self.redis_password, encoding='utf-8')
        except Exception as e:
            logger.error(f"Error while connecting to redis: {e}")
            logger.exception(e)
            raise e

    ###
    # scenario related
    #

    @staticmethod
    def marshall_step(p: Step):
        tmpstmp = p.timestamp.strftime(TIMESTAMP_FORMAT)
        return f'{tmpstmp}|{p.type}|{p.location.x}|{p.location.y}'

    def serialize_steps(self, steps: List[Step]):
        return [self.marshall_step(x) for x in steps]

    async def store_scenario(self, scenario: Scenario, namespace: str = SCENARIO_KEY):
        logger.info('store_scenario')
        result = None
        try:
            scenario_key = f'{namespace}:{scenario.customer.customer_id}'
            values = self.serialize_steps(scenario.path)
            length = len(values)

            if length >= 1:
                logger.info(f'Sending multiple values ... {values}')
                result = await self.redis.rpush(scenario_key, *values)

                result = scenario_key
        except Exception as e:
            logger.error(f"Error while talking to redis: {e}")
            logger.exception(e)

        return result

    ###
    # timeline related
    #

    @staticmethod
    def marshall_event(client_id: str, p: Step):
        tmpstmp = p.timestamp.strftime(TIMESTAMP_FORMAT)
        return f'{client_id}|{p.location.x}|{p.location.y}|{p.type}|{tmpstmp}'

    @staticmethod
    def unmarshall_event(s: str):
        logger.debug(f'unmarshal event {s}')
        parts = s.split(sep='|')

        client_id = parts[0]
        loc = Location(x=int(parts[1]), y=int(parts[2]))
        timestamp = datetime.strptime(parts[4], TIMESTAMP_FORMAT)

        return client_id, Step(location=loc, type=parts[3], timestamp=timestamp)

    async def add_to_timeline(self, customer_id: str, step: Step):
        """
        Store info about given step for a given customer.
        :param customer_id:
        :param step:
        :return:
        """
        logger.info(f'add_to_timeline: {customer_id} {step} ')

        result = False

        try:
            event_representation = self.marshall_event(customer_id, step)
            logger.warning(f'marshalled event_representation: {event_representation}')
            result = await self.redis.zadd(TIMELINE_KEY, int(step.timestamp.timestamp()), event_representation)
        except Exception as e:
            logger.error(f"Error while talking to redis: {e}")
            logger.exception(e)

        return result

    async def get_events(self, unix_time: int) -> List[Tuple[str, Step]]:
        logger.debug(f'get events from redis for timestamp {unix_time}')
        """
        Get events definitions for a given point in time
        """
        result = []

        try:
            events = await self.redis.zrangebyscore(TIMELINE_KEY, min=unix_time, max=unix_time)
            logger.info("events: " + str(events))
            result = [self.unmarshall_event(e) for e in events]
            mop = await self.redis.zremrangebyscore(TIMELINE_KEY, min=unix_time, max=unix_time)
        except Exception as e:
            logger.error(f"Error while talking to redis: {e}")
            logger.exception(e)
            logger.error(type(e))

        return result
