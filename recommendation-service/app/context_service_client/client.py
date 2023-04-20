from app import logger
from app.config import config


class ContextServiceClient:
    _service_url = f'{config.CLIENT_CONTEXT_URL}/get_context'

    def __init__(self):
        logger.info(f'Using context service at {self._service_url}')

    def get_context(self, customer_id: int):
        logger.warning(f'not implemented -- should invoke {self._service_url}')


def create_context_service_client():
    return ContextServiceClient()
