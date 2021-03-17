import asyncio
from typing import Optional

from app.utils import log_config

from fastapi import FastAPI, Request
from fastapi.responses import PlainTextResponse

from app.utils import logger
from app.utils.kafka_clients import entry_consumer, focus_consumer
from app.utils.context_client import call_get_client_context
from app.utils.prediction_client import process_prediction_request

app = FastAPI()


@app.on_event("startup")
async def startup_event():
    ####################
    # background tasks

    # Implement event processing logic in call_get_client_context and call_score_coupons
    setattr(entry_consumer, 'process', call_get_client_context)
    setattr(focus_consumer, 'process', process_prediction_request)

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
    logger.info('verify healthcheck')
    return PlainTextResponse('OK')


@app.post('/action')
async def action(request: Request) -> Optional[str]:
    logger.debug('action')

    data = await request.json()
    return PlainTextResponse('NOT IMPLEMENTED')
