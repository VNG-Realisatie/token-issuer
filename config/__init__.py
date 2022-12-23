import logging

from fastapi.logger import logger as fastapi_logger

uvicorn_logger = logging.getLogger("uvicorn")
log_level = uvicorn_logger.level

root_logger = logging.getLogger()
uvicorn_access_logger = logging.getLogger("uvicorn.access")

root_logger.setLevel(log_level)
uvicorn_access_logger.setLevel(log_level)
fastapi_logger.setLevel(log_level)

logger = logging.getLogger()
handler = logging.StreamHandler()
handler.setLevel(log_level)

formatter = logging.Formatter(
    "%(asctime)s | %(levelname)s | %(message)s", datefmt="%d/%m/%Y %H:%M:%S"
)

if log_level is logging.DEBUG:
    formatter = logging.Formatter(
        "%(asctime)s - %(name)s - %(levelname)s - %(message)s (%(filename)s:%(lineno)d)",
        datefmt="%d/%m/%Y %H:%M:%S",
    )

handler.setFormatter(formatter)
logger.addHandler(handler)
