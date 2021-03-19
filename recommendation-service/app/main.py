import asyncio

from pydantic import json
from typing import Optional

from app.utils import log_config

from fastapi import FastAPI
from fastapi.responses import PlainTextResponse

from app.utils import logger
from app.utils.kafka_clients import entry_consumer, focus_consumer
from app.utils.context_client import call_get_client_context
from app.utils.model import EntryEvent, FocusEvent
from app.utils.prediction_client import process_prediction_request
from app.cache.db_pool import DBPool


app = FastAPI()
db = DBPool()


@app.on_event("startup")
async def startup_event():
    await db.create_pool()

    ####################
    # background tasks

    # Implement event processing logic in call_get_client_context and call_score_coupons
    setattr(entry_consumer, 'process', call_get_client_context)
    setattr(entry_consumer, 'process_kwargs', {'db_pool': db.get_pool()})
    
    setattr(focus_consumer, 'process', process_prediction_request)
    setattr(focus_consumer, 'process_kwargs', {'db_pool': db.get_pool()})

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
    result = await call_get_client_context(message, db.get_pool())
    return PlainTextResponse(str(result))


@app.post('/mock_focus')
async def mock_focus_event(event: FocusEvent) -> Optional[str]:
    """
    Test endpoint that simulates arrival of "focus event".
    """
    logger.info('mock_entry_event')
    logger.debug(event)

    message = event.json()
    logger.warn(f'message: {message}')

    result = await process_prediction_request(message, db.get_pool())
    return PlainTextResponse(str(result))
