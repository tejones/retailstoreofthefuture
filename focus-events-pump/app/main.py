import uvicorn
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from fastapi import FastAPI
from fastapi.responses import PlainTextResponse

from app import logger
from app.config import show_banner
from app.config.config import PERIODIC_TASKS_INTERVAL, DEPARTMENTS, FOCUS_TOPIC, GENERATOR_AUTO_START, COMMAND_TOPIC, \
    MQTT_CLIENT_ID
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


@app.get("/state")
async def get_state():
    return {"state": "started" if app.state.generator_enabled else "stopped"}


@app.post('/start')
async def start():
    logger.info('start_generator')
    result = "OK" if change_generator_state(True) else "Generator is already enabled"

    # let other instances know that we want to start
    mqtt.publish(COMMAND_TOPIC, 'START')
    return PlainTextResponse(result)


@app.post('/stop')
async def stop():
    logger.info('stop_generator')
    result = "OK" if change_generator_state(False) else "Generator is already disabled"

    # let other instances know that we want to stop
    mqtt.publish(COMMAND_TOPIC, 'STOP')
    return PlainTextResponse(result)


####################
# utility functions
def tick():
    logger.debug("tick")
    if not app.state.generator_enabled:
        logger.debug("Generator is disabled")
    else:
        logger.debug("Publishing a new event")
        event = app.state.message_generator.generate()
        payload = event.json(by_alias=True, exclude_none=True).encode()
        logger.debug(f"event: {payload}")
        mqtt.publish(FOCUS_TOPIC, payload)


def change_generator_state(on_off: bool):
    logger.info('change_generator_state to ' + ('on' if on_off else 'off'))
    if app.state.generator_enabled == on_off:
        return False
    else:
        app.state.generator_enabled = on_off
        return True


#####
# App startup and shutdown
@app.on_event('startup')
async def init_app():
    logger.info("Initializing the app")
    app.state.message_generator = FocusEventGenerator(DEPARTMENTS)
    app.state.generator_enabled = GENERATOR_AUTO_START
    if not app.state.generator_enabled:
        show_banner(logger.warning, "Generator is disabled. Use /start to enable it.")

    logger.info("Starting the scheduler")
    scheduler = AsyncIOScheduler()
    scheduler.add_job(tick, 'interval', seconds=PERIODIC_TASKS_INTERVAL)
    scheduler.start()


@mqtt.subscribe(COMMAND_TOPIC + '/#')
async def command_message(client, topic, payload, qos, properties):
    logger.info(f"Received message on topic {topic}: {payload}")
    # strip the command topic and the leading slash from the actual topic
    specific_id = topic[len(COMMAND_TOPIC):]
    if specific_id.startswith('/'):
        specific_id = specific_id[1:]

    # act only on the specific id or on all (no id specified)
    if not specific_id or specific_id == MQTT_CLIENT_ID:
        # convert payload to string and make upper case
        command = payload.decode().upper()
        if command == 'START':
            logger.info("Starting...")
            change_generator_state(True)
        elif command == 'STOP':
            logger.info("Stopping...")
            change_generator_state(False)
        else:
            logger.warning(f"Unknown command {command}")
    else:
        logger.info(f"Skipping message for id {specific_id}")
    return 0

# For debugging
if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
