from apscheduler.schedulers.asyncio import AsyncIOScheduler
from fastapi import FastAPI
from fastapi.responses import PlainTextResponse

from app import logger
from app.config.config import PERIODIC_TASKS_INTERVAL, DEPARTMENTS, FOCUS_TOPIC, GENERATOR_AUTO_START
from app.generator import FocusEventGenerator
from app.mqtt.mqtt import initialize_mqtt

app = FastAPI()
mqtt = initialize_mqtt(app)

####################
# web handlers
logger.info('Defining web service handlers...')


@app.get('/healthcheck')
async def healthcheck():
    """
    Service health check endpoint.
    """
    logger.info('verify health')
    return PlainTextResponse('OK')


@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.post('/start')
async def start_generator():
    logger.info('start_generator')
    result = "OK"
    if app.state.generator_enabled:
        result = "Generator is already enabled"
    else:
        app.state.generator_enabled = True

    return PlainTextResponse(result)


@app.post('/stop')
async def stop_generator():
    logger.info('stop_generator')
    result = "OK"
    if not app.state.generator_enabled:
        result = "Generator is already disabled"
    else:
        app.state.generator_enabled = False

    return PlainTextResponse(result)


####################
# utility functions
def tick():
    logger.debug("tick")
    if not app.state.generator_enabled:
        logger.debug("Generator is disabled")
    else:
        logger.info("Publishing a new event")
        event = app.state.message_generator.generate()
        payload = event.json(by_alias=True, exclude_none=True).encode()
        logger.debug(f"event: {payload}")
        mqtt.publish(FOCUS_TOPIC, payload)


#####
# App startup and shutdown
@app.on_event('startup')
async def init_app():
    logger.info("Initializing the app")
    app.state.message_generator = FocusEventGenerator(DEPARTMENTS)
    app.state.generator_enabled = GENERATOR_AUTO_START

    logger.info("Starting the scheduler")
    scheduler = AsyncIOScheduler()
    scheduler.add_job(tick, 'interval', seconds=PERIODIC_TASKS_INTERVAL)
    scheduler.start()
