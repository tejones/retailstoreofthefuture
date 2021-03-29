from app.cache.read_cache import ReadCache
from app.utils import logger
from app.utils.config import TESTING_NO_POSTGRES
from app.utils.testing import DummyReadCache


async def create_cache_reader():
    if TESTING_NO_POSTGRES:
        logger.warn('- ' * 20)
        logger.warn('')
        logger.warn('Initializing fake postgres connection.')
        logger.warn('Please don\'t be fooled!')
        logger.warn('')
        logger.warn('- ' * 20)
        rc = DummyReadCache()
    else:
        logger.info('Initializing postgres connection.')
        rc = ReadCache()
        await rc.initialize()
    return rc
