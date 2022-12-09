import logging
from fastapi.logger import logger

gunicorn_logger = logging.getLogger('gunicorn.error')
logger.handlers = gunicorn_logger.handlers
if __name__ != "main":
    logger.setLevel(gunicorn_logger.level)
else:
    logger.setLevel(logging.DEBUG)
# logging.config.fileConfig("logging.conf", disable_existing_loggers=False)
# logger = logging.getLogger(__name__)
