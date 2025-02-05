import logging

import structlog

loggers = {}


# noinspection SpellCheckingInspection
class Logger(logging.Logger):
    def __init__(self, name, level=0):
        self._logger = structlog.get_logger(name)

    def setLevel(self, level):
        self._logger.setLevel(level)

    def isEnabledFor(self, level):
        return self._logger.isEnabledFor(level)

    def getEffectiveLevel(self):
        return self._logger.getEffectiveLevel()

    def getChild(self, suffix):
        return self._logger.getChild(suffix)

    def getChildren(self):
        return self._logger.getChildren()

    def debug(
        self, msg, *args, exc_info=None, stack_info=False, stacklevel=1, extra=None
    ):
        self._logger.debug(
            msg,
            *args,
            exc_info=exc_info,
            stack_info=stack_info,
            stacklevel=stacklevel,
            **extra,
        )

    def info(
        self, msg, *args, exc_info=None, stack_info=False, stacklevel=1, extra=None
    ):
        self._logger.info(
            msg,
            *args,
            exc_info=exc_info,
            stack_info=stack_info,
            stacklevel=stacklevel,
            **extra,
        )

    def warning(
        self, msg, *args, exc_info=None, stack_info=False, stacklevel=1, extra=None
    ):
        self._logger.warning(
            msg,
            *args,
            exc_info=exc_info,
            stack_info=stack_info,
            stacklevel=stacklevel,
            **extra,
        )

    def error(
        self, msg, *args, exc_info=None, stack_info=False, stacklevel=1, extra=None
    ):
        self._logger.error(
            msg,
            *args,
            exc_info=exc_info,
            stack_info=stack_info,
            stacklevel=stacklevel,
            **extra,
        )

    def exception(
        self, msg, *args, exc_info=True, stack_info=False, stacklevel=1, extra=None
    ):
        self._logger.exception(
            msg,
            *args,
            exc_info=exc_info,
            stack_info=stack_info,
            stacklevel=stacklevel,
            **extra,
        )

    def critical(
        self, msg, *args, exc_info=None, stack_info=False, stacklevel=1, extra=None
    ):
        self._logger.critical(
            msg,
            *args,
            exc_info=exc_info,
            stack_info=stack_info,
            stacklevel=stacklevel,
            **extra,
        )

    def log(
        self,
        level,
        msg,
        *args,
        exc_info=None,
        stack_info=False,
        stacklevel=1,
        extra=None,
    ):
        self._logger.log(
            level,
            msg,
            *args,
            exc_info=exc_info,
            stack_info=stack_info,
            stacklevel=stacklevel,
            **extra,
        )


def get_logger(name, level=0) -> Logger:
    if name not in loggers:
        loggers[name] = Logger(name, level)
    return loggers[name]
