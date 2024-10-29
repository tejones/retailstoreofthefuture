from typing import Optional

from fastapi import FastAPI
from fastapi.responses import PlainTextResponse

from app import logger
from app.config import config
from app.cache.cache_reader import create_cache_reader
from app.context_service_client.client import create_context_service_client
from app.event_processors.entry_event_processor import EntryEventProcessor
from app.event_processors.focus_event_processor import FocusEventProcessor
from app.event_processors.model import EntryEvent, FocusEvent
from app.event_emitters.prediction_producer import PredictionProducer
from app.mqtt.mqtt import initialize_mqtt
from app.prediction_service_client.client import create_prediction_service_client


app = FastAPI()
mqtt = initialize_mqtt(app)


@app.on_event('startup')
async def startup_event():
    cache_reader = await create_cache_reader()
    prediction_service_client = create_prediction_service_client()
    context_service_client = create_context_service_client()
    prediction_producer = PredictionProducer(mqtt)
    app.state.entry_event_processor = EntryEventProcessor(cache_reader, context_service_client)
    app.state.focus_event_processor = FocusEventProcessor(cache_reader, prediction_service_client, prediction_producer)


####################
# web handlers
logger.info('Defining web service handlers...')


@app.get('/healthcheck')
async def healthcheck() -> Optional[str]:
    """
    Service health check endpoint.
    """
    logger.info('verify healthcheck')
    return PlainTextResponse('OK')


@app.post('/mock_entry')
async def mock_entry_event(event: EntryEvent) -> Optional[str]:
    """
    Test endpoint that simulates arrival of "entry event".
    """
    logger.info('mock_entry_event')
    logger.debug(event)

    result = await customer_enters(None, config.ENTER_TOPIC, event.json(by_alias=True).encode(), None, None)

    return PlainTextResponse(str(result))


@app.post('/mock_focus')
async def mock_focus_event(event: FocusEvent) -> Optional[str]:
    """
    Test endpoint that simulates arrival of "focus event".
    """
    logger.info('mock_focus_event')
    logger.debug(event)

    result = await customer_focuses(None, config.FOCUS_TOPIC, event.json(by_alias=True).encode(), None, None)

    return PlainTextResponse(str(result))


####################
# mqtt handlers


@mqtt.subscribe(config.ENTER_TOPIC)
async def customer_enters(client, topic, payload, qos, properties):
    logger.warning(f'Received message: {topic}, {payload.decode()}')
    await app.state.entry_event_processor.process(payload.decode())


@mqtt.subscribe(config.FOCUS_TOPIC)
async def customer_focuses(client, topic, payload, qos, properties):
    logger.warning(f'Received message: {topic}, {payload.decode()}')
    await app.state.focus_event_processor.process(payload.decode())
