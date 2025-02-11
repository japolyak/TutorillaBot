import logging

from .config import log_level as ll
from enum import StrEnum


LOG_FORMAT_DEBUG = "%(levelname)s:%(message)s:%(pathname)s:%(funcName)s:%(lineno)d"


class LogLevels(StrEnum):
    info = "INFO"
    warn = "WARN"
    error = "ERROR"
    debug = "DEBUG"


def configure_logger():
    log_level = str(ll).upper()
    log_levels = list(LogLevels)

    if log_level not in log_levels:
        logging.basicConfig(level=LogLevels.error)
        return

    if log_level == LogLevels.debug:
        logging.basicConfig(encoding='utf-8', level=log_level, format='%(asctime)s %(levelname)s: %(message)s')
        return

    logging.basicConfig(level=log_level)

log = logging.getLogger(__name__)
configure_logger()