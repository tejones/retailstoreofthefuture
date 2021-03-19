from app.utils import logger
from app.utils.config import CLIENT_CONTEXT_URL

scorer_url = f'{CLIENT_CONTEXT_URL}/get_context'


async def call_get_client_context(message: str):
    # XXX TODO unmarshall values
    customer_id = 1
    logger.info(f'calling Get Client Context service with {customer_id}')
    logger.warn(f'not implemented -- should invoke {scorer_url}')
    return 7
