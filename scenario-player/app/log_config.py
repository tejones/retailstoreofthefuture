import logging
import os


# TODO move to config
LOG_FILENAME = "messages.log"
LOG_FORMAT = "%(asctime)s [%(threadName)-12.12s] [%(levelname)-5.5s]\t%(message)s"
LOG_LEVEL = os.environ.get('LOG_LEVEL', 'DEBUG').upper()

assert LOG_LEVEL in ['DEBUG', 'INFO', 'WARNING', 'ERROR']


def configure_logger():
    logging.basicConfig(format=LOG_FORMAT, level=LOG_LEVEL)
    # Basic console logger
    logger = logging.getLogger("app")
    # File logger
    log_formatter = logging.Formatter(LOG_FORMAT)
    file_handler = logging.FileHandler(LOG_FILENAME, encoding='UTF-8')
    file_handler.setFormatter(log_formatter)
    logger.addHandler(file_handler)
    # Configuration done
    logger.debug("Logger configured...")
    return logger
