import logging
from logging.handlers import TimedRotatingFileHandler

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
handler = TimedRotatingFileHandler("debug.log", when="d", backupCount=7)
formatter = logging.Formatter(
    "%(asctime)s "
    + "[%(levelname)s] "
    + "%(funcName)s: "
    + "%(name)s: "
    + "%(message)s"
)
handler.setFormatter(formatter)
logger.addHandler(handler)
