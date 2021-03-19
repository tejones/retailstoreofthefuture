import logging

LOG_FILENAME = "messages.log"
# logging.basicConfig(level=logging.DEBUG)
logging.basicConfig(level=logging.INFO)

# XXX TODO hardcoded logger name
logger = logging.getLogger("app.utils")

logFormatter = logging.Formatter("%(asctime)s [%(threadName)-12.12s] [%(levelname)-5.5s]  %(message)s")
# rootLogger = logging.getLogger()
fileHandler = logging.FileHandler(LOG_FILENAME, encoding='UTF-8')
fileHandler.setFormatter(logFormatter)
logger.addHandler(fileHandler)
consoleHandler = logging.StreamHandler()
consoleHandler.setFormatter(logFormatter)
logger.addHandler(consoleHandler)


logger.info("Logger configured...")
