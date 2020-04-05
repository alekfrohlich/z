"""Log events to standard output."""
from enum import Enum


class LogLevel(Enum):
    """Enum representing incremental log levels."""

    INFO = 1
    """Logs everything."""
    WARN = 2
    """Logs warnings and errors."""
    ERRO = 3
    """Logs errors."""


class Logger:
    """Incremental logger class."""

    _LOG_LEVEL = LogLevel.INFO

    @staticmethod
    def log(level, message):
        """Log only if the message's log level is high enough."""
        if level.value >= Logger._LOG_LEVEL.value:
            print(message)
