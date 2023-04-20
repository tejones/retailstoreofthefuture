import logging
import os

LOG_FILENAME = os.getenv('LOG_FILENAME', '')
LOG_FORMAT = "%(asctime)s [%(threadName)-12.12s] [%(levelname)-5.5s]\t%(message)s"
LOG_LEVEL = os.environ.get('LOG_LEVEL', 'INFO').upper()
LOGGER_NAME = 'app'

assert LOG_LEVEL in ['DEBUG', 'INFO', 'WARNING', 'ERROR']


def configure_logger(logger_name=LOGGER_NAME):
    logging.basicConfig(format=LOG_FORMAT, level=LOG_LEVEL)
    # Basic console logger
    logger = logging.getLogger(logger_name)
    # File logger
    if LOG_FILENAME:
        logger.info("Configuring file logger...")
        fileHandler = logging.FileHandler(LOG_FILENAME, encoding='UTF-8')
        logFormatter = logging.Formatter(LOG_FORMAT)
        fileHandler.setFormatter(logFormatter)
        logger.addHandler(fileHandler)

    logger.debug("Logger configured...")
    return logger
