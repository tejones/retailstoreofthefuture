from pydantic import ValidationError

from app import logger
from app.cache.cache_reader import CacheReader
from app.context_service_client.client import ContextServiceClient
from app.event_processors.model import EntryEvent


class EntryEventProcessor:

    def __init__(self, cache_reader: CacheReader, context_service_client: ContextServiceClient):
        self._cache_reader = cache_reader
        self._context_service_client = context_service_client

    async def process(self, message: str):
        try:
            entry_event = EntryEvent.parse_raw(message)
        except ValidationError as e:
            logger.error(f'Could not parse entry event message: "{message}": {e}')
            return
        logger.info(f'calling Get Client Context service with {entry_event.customer_id}')
        self._context_service_client.get_context(customer_id=entry_event.customer_id)
        # XXX TODO looks like EntryEventProcessor is a mock; make it work or describe why it's not needed
        return 7
