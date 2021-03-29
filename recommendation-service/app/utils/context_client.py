from app.utils import logger
from app.utils.config import CLIENT_CONTEXT_URL
from app.utils.event_consumer import EventConsumer

scorer_url = f'{CLIENT_CONTEXT_URL}/get_context'


class EntryEventProcessor(EventConsumer):
    def set_cache_reader(self, cache_reader):
        self.cache_reader = cache_reader

    async def process(self, message: str):
        # XXX TODO unmarshall values
        customer_id = 1
        logger.info(f'calling Get Client Context service with {customer_id}')
        logger.warn(f'not implemented -- should invoke {scorer_url}')
        return 7
