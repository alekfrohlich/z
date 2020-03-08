""" Log events to console. """

from enum import Enum


class LogLevel(Enum):
    """
        Log levels are incremental:
            ERROR - only logs errors.
            WARN - logs warnings and errors.
            INFO - logs everything.
    """
    INFO = 1
    WARN = 2
    ERROR = 3

class Logger():
    LOG_LEVEL = LogLevel.INFO

    @staticmethod
    def log(level, message):
        if level.value >= Logger.LOG_LEVEL.value:
            print(message)
