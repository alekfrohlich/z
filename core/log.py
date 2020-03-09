""" Log events to console. """

from enum import Enum


class LogLevel(Enum):
    """
        Log levels are incremental:
            ERROR - Only logs errors.
            WARN  - Logs warnings and errors.
            INFO  - Logs everything.
    """

    INFO = 1
    WARN = 2
    ERROR = 3

class Logger():
    log_level = LogLevel.INFO

    @staticmethod
    def log(level, message):
        """" Log only if the message's log level is high enough. """
        if level.value >= Logger.log_level.value:
            print(message)
