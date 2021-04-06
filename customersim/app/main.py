import asyncio

from fastapi import FastAPI
from fastapi.responses import PlainTextResponse

from app import logger
from app.config import CUSTOMER_ENTER_TOPIC, CUSTOMER_EXIT_TOPIC, CUSTOMER_MOVE_TOPIC
from app.events_model import CustomerMoveEvent, CustomerExitEvent, CustomerEnterEvent
from app.log_config import configure_logger
from app.mosquitto import get_mqtt_client
from app.simulation_engine import CustomerSimulator
from app.store_initializer import init_customer_list, init_store

configure_logger()

app = FastAPI()


@app.on_event("startup")
async def startup_event():
    app.state.customer_list = init_customer_list()
    app.state.store = init_store()

    ####################
    # init connections
    app.state.mqttc = await get_mqtt_client()

    ####################
    # background tasks
    customer_sim = CustomerSimulator(app.state.store, app.state.customer_list, app.state.mqttc)
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


class CustomerEnter(object):
    pass


@app.post('/produce_entry')
async def produce_entry_event(event: CustomerEnterEvent) -> PlainTextResponse:
    """
    Test endpoint that forces publication of "customer/enter".
    """
    logger.info('produce_entry_event')
    logger.debug(event)

    message = event.json()
    result = app.state.mqttc.publish(CUSTOMER_ENTER_TOPIC, message)
    return PlainTextResponse(str(result))


@app.post('/produce_move')
async def produce_move_event(event: CustomerMoveEvent) -> PlainTextResponse:
    """
    Test endpoint that forces publication of "customer/move".
    """
    logger.info('produce_move_event')
    logger.debug(event)

    message = event.json()
    result = app.state.mqttc.publish(CUSTOMER_MOVE_TOPIC, message)
    return PlainTextResponse(str(result))


@app.post('/produce_exit')
async def produce_exit_event(event: CustomerExitEvent) -> PlainTextResponse:
    """
    Test endpoint that forces publication of "customer/exit".
    """
    logger.info('produce_exit_event')
    logger.debug(event)

    message = event.json()
    result = app.state.mqttc.publish(CUSTOMER_EXIT_TOPIC, message)
    return PlainTextResponse(str(result))
