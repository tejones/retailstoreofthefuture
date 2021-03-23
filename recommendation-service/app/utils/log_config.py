import logging
import os

LOG_FILENAME = "messages.log"
LOG_FORMAT = "%(asctime)s [%(threadName)-12.12s] [%(levelname)-5.5s]\t%(message)s"
LOG_LEVEL = os.environ.get('LOG_LEVEL', 'INFO').upper()

assert LOG_LEVEL in ['DEBUG', 'INFO', 'WARNING', 'ERROR']

logging.basicConfig(format=LOG_FORMAT, level=LOG_LEVEL)

# Basic console logger
logger = logging.getLogger("app.utils")

# File logger
logFormatter = logging.Formatter(LOG_FORMAT)

fileHandler = logging.FileHandler(LOG_FILENAME, encoding='UTF-8')
fileHandler.setFormatter(logFormatter)

logger.addHandler(fileHandler)

# Configuration done
logger.debug("Logger configured...")
