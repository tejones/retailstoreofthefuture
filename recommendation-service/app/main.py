import asyncio
from typing import Optional

from fastapi import FastAPI
from fastapi.responses import PlainTextResponse

from app.utils import logger
from app.utils.db_client import create_cache_reader
from app.utils.kafka_clients import create_kafka_clients
from app.utils.model import EntryEvent, FocusEvent

app = FastAPI()


@app.on_event("startup")
async def startup_event():
    app.state.cache_reader = await create_cache_reader()

    entry_consumer, focus_consumer, prediction_producer = create_kafka_clients(app.state.cache_reader)
    app.state.entry_consumer = entry_consumer
    app.state.focus_consumer = focus_consumer
    app.state.prediction_producer = prediction_producer

    ####################
    # background tasks
    asyncio.create_task(entry_consumer.consume_messages())
    asyncio.create_task(focus_consumer.consume_messages())


####################
# web handlers
logger.info('Defining web service handlers...')


@app.get('/')
async def root():
    logger.debug('/')
    return {'message': 'Hello World'}


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

    message = event.json()
    
    result = await app.state.entry_consumer.process(message)
    return PlainTextResponse(str(result))


@app.post('/mock_focus')
async def mock_focus_event(event: FocusEvent) -> Optional[str]:
    """
    Test endpoint that simulates arrival of "focus event".
    """
    logger.info('mock_entry_event')
    logger.debug(event)

    message = event.json()

    result = await app.state.focus_consumer.process(message)
    return PlainTextResponse(str(result))
