"""Log events to standard output."""
from enum import Enum


class LogLevel(Enum):
    """Enum representing incremental log levels.

    ERRO: Only logs errors.
    WARN: Logs warnings and errors.
    INFO: Logs everything.

    """

    INFO = 1
    WARN = 2
    ERRO = 3


class Logger:
    """Incremental logger class."""

    _LOG_LEVEL = LogLevel.INFO

    @staticmethod
    def log(level, message):
        """"Log only if the message's log level is high enough."""
        if level.value >= Logger._LOG_LEVEL.value:
            print(message)
