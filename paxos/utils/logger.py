import logging
from logging import StreamHandler

from paxos.config.configuration import LOG_LEVEL, LOG_DEBUG, LOG_INFO


class Logger(object):
    def __init__(self):
        self.logger = logging.getLogger("paxos_logger")
        handle = StreamHandler()

        self._set_level(self.logger)
        self._set_level(handle)

        self.logger.addHandler(handle)

    def _set_level(self, obj):
        if LOG_LEVEL == LOG_DEBUG:
            obj.setLevel(logging.DEBUG)
        elif LOG_LEVEL == LOG_INFO:
            obj.setLevel(logging.INFO)

    def debug(self, log):
        self.logger.debug(log)

    def info(self, log):
        self.logger.info(log)

LOG = Logger()
