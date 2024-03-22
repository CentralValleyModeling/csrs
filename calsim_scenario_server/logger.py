import logging
from logging.handlers import RotatingFileHandler

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
handler = RotatingFileHandler("debug.log", maxBytes=10_000, backupCount=1)
formatter = logging.Formatter(
    "%(asctime)s "
    + "[%(levelname)s] "
    + "%(funcName)s: "
    + "%(name)s: "
    + "%(message)s"
)
handler.setFormatter(formatter)
logger.addHandler(handler)
