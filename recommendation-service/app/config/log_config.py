import logging
import os

LOG_FILENAME = os.getenv('LOG_FILENAME', '')
LOG_FORMAT = "%(asctime)s [%(threadName)-12.12s] [%(levelname)-5.5s]\t%(message)s"
LOG_LEVEL = os.environ.get('LOG_LEVEL', 'INFO').upper()
LOGGER_NAME = 'app'

assert LOG_LEVEL in ['DEBUG', 'INFO', 'WARNING', 'ERROR']

logging.basicConfig(format=LOG_FORMAT, level=LOG_LEVEL)

# Basic console logger
logger = logging.getLogger(LOGGER_NAME)
logger.info(f"Configuring logger with LOG_LEVEL={LOG_LEVEL}")

# File logger
if LOG_FILENAME:
    logger.info("Configuring file logger...")
    fileHandler = logging.FileHandler(LOG_FILENAME, encoding='UTF-8')
    logFormatter = logging.Formatter(LOG_FORMAT)
    fileHandler.setFormatter(logFormatter)
    logger.addHandler(fileHandler)

# Configuration done
logger.debug("Logger configured...")
