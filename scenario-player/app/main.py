import asyncio
from datetime import datetime
from typing import List

import uvicorn
from fastapi import FastAPI, HTTPException, Query
from fastapi.responses import PlainTextResponse

from app import logger
from app.backend.priority_queue import PQueueTimelineBackend
from app.controller import TimelineController
from app.publisher.mqtt_publisher import MQTTEventPublisher
from app.scenario.scenario_deployer import ScenarioDeployer
from app.scenario.scenario_model import Scenario, CustomerState
from app.scenario.scenario_producer import ScenarioProducer
from app.simulator.simulation_engine import CustomerSimulator

app = FastAPI()

# For bigger scale and volume, use Redis backend
USE_REDIS_BACKEND = False


async def init_backend():
    if USE_REDIS_BACKEND:
        # XXX TODO add error handling
        from app.backend.redis import RedisTimelineBackend
        backend = RedisTimelineBackend('redis://127.0.0.1:6379', database=0, redis_password='redis123')
    else:
        backend = PQueueTimelineBackend()

    await backend.initialize()
    return backend


@app.on_event("startup")
async def startup_event():
    app.state.backend = await init_backend()
    app.state.scenario_producer = ScenarioProducer()
    app.state.scenario_deployer = ScenarioDeployer(app.state.backend)
    app.state.timeline_controller = TimelineController(app.state.backend, app.state.scenario_producer,
                                                       app.state.scenario_deployer)

    # app.state.event_publisher = LoggerEventPublisher()
    app.state.event_publisher = MQTTEventPublisher(app)
    await app.state.event_publisher.initialize()

    # ####################
    # # background tasks
    customer_sim = CustomerSimulator(app.state.backend, app.state.event_publisher)

    asyncio.create_task(customer_sim.run())


####################
# web handlers
logger.info('Defining web service handlers...')


@app.get('/')
async def root():
    logger.debug('/')
    return {'message': 'Hello World'}


@app.get('/health')
async def health() -> PlainTextResponse:
    """
    Service health check endpoint.
    """
    logger.info('verify health')
    return PlainTextResponse('OK')


#
# Timeline probably should be created on the app startup.
# Only modification to the timeline should be adding scenarios and rewinding current time of timeline.

@app.post('/scenario_draft')
async def accept_scenario_draft(payload: Scenario) -> PlainTextResponse:
    """
    """
    logger.info('accept_scenario')
    logger.debug(payload)

    message = payload.json(exclude_none=True)
    logger.debug(f'Received {message} payload')

    result = await app.state.timeline_controller.accept_scenario_draft(payload)

    if not result:
        raise HTTPException(status_code=404, detail='Problem storing scenario.')

    # result = 'Scenario created'
    return PlainTextResponse(result)


RECALCULATE_DESCRIPTION = 'if set to True, scenario will start with current time ' \
                          '(and step timestamps will be recalculated appropriately)'


@app.post('/scenario')
async def deploy_scenario(payload: Scenario,
                          recalculate_time: bool = Query(default=False,
                                                         description=RECALCULATE_DESCRIPTION)) -> PlainTextResponse:
    """
    Accepts a scenario definition and adds it to the current timeline.
    """
    logger.info('deploy_scenario')
    logger.debug(f'recalculate_time: {recalculate_time}')
    logger.debug(payload)

    message = payload.json(exclude_none=True)
    logger.debug(f'Received {message} payload')

    result = await app.state.timeline_controller.deploy_scenario(payload, recalculate_time)

    if not result:
        raise HTTPException(status_code=404, detail='Problem storing scenario.')

    return PlainTextResponse(str(result))


@app.get('/state')
async def get_current_state(timestamp: datetime) -> List[CustomerState]:
    logger.info(f'get_current_state as for {timestamp}')
    return await app.state.timeline_controller.get_current_state(timestamp)


# For debugging
if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
