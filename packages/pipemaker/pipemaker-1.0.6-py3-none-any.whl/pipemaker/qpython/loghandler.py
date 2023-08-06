""" logging using shared objects
"""
import logging
from logging.handlers import DEFAULT_TCP_LOGGING_PORT, QueueHandler, QueueListener
from queue import Queue

from ..utils.share import create_client, create_server


class SharedQueueHandler(QueueHandler):
    """ handler to put messages on shared queue
    extends QueueHandler to multiple machines
    """

    @classmethod
    def start_server(cls):
        """ queue server listens for log messages on port """
        create_server(Queue(), DEFAULT_TCP_LOGGING_PORT)

    def __init__(self, **kwargs):
        logging.Handler.__init__(self)
        self.queue = create_client(logging.handlers.DEFAULT_TCP_LOGGING_PORT)


class FileHandler(logging.FileHandler):
    """ read messages from the log queue and write to file """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        log = logging.getLogger()
        if log.handlers:
            self.setFormatter(log.handlers[0].formatter)

        # listener
        q = create_client(logging.handlers.DEFAULT_TCP_LOGGING_PORT)
        self.listener = QueueListener(q, self)
        self.listener.start()
