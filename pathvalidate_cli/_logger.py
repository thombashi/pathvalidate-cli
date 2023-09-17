import sys
from typing import Final

from loguru import logger

from ._const import MODULE_NAME


class LogLevel:
    DEBUG: Final[str] = "DEBUG"
    INFO: Final[str] = "INFO"
    QUIET: Final[str] = "QUIET"


logger.disable(MODULE_NAME)


def set_logger(is_enable: bool, propagation_depth: int = 1) -> None:
    if is_enable:
        logger.enable(MODULE_NAME)
    else:
        logger.disable(MODULE_NAME)


def initialize_logger(name: str, log_level: str) -> None:
    logger.remove()

    if log_level == LogLevel.QUIET:
        logger.disable(name)
        return

    if log_level == LogLevel.DEBUG:
        log_format = (
            "<level>{level: <8}</level> | "
            "<cyan>{name}</cyan>:"
            "<cyan>{function}</cyan>:"
            "<cyan>{line}</cyan> - <level>{message}</level>"
        )
    else:
        log_format = "<level>[{level}]</level> {message}"

    logger.add(sys.stderr, colorize=True, format=log_format, level=log_level)
    logger.enable(name)
