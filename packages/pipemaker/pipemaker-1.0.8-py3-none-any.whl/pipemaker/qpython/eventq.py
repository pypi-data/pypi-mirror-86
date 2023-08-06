import logging
from queue import Queue

from .. import CONFIG
from ..utils.share import create_client, create_server

log = logging.getLogger(__name__)


class dictq(dict):
    """ dict where each value is a queue
    server owns the queues to synchronise across processes.
    server functions explicitly defined as cannot use index, dunder or properties with proxymanager.
    """

    def get(self, key, block=True, timeout=None):
        """ get from queue. if queue does not exist then create it and wait. """
        self.setdefault(key, Queue())
        return self[key].get(block, timeout)

    def put(self, key, body="", ch=None):
        """ add to queue. if queue does not exist then create it """
        self.setdefault(key, Queue())
        self[key].put(body)

    def get_all(self):
        """ return dict with queues as lists because queue cannot be pickled """
        return {k: list(v.queue) for k, v in self.items()}


class Eventq:
    """
    local proxy for dictq on server

    Usage:
        # wait for an event to happen
        data = Eventq().get("eventkey")

        # trigger event
        Eventq().put("eventkey", data)

        # get dict of all events
        Eventq().get_all()
    """

    @classmethod
    def start_server(self):
        create_server(dictq(), CONFIG.eventq_port)

    def __init__(self):
        self.dq = create_client(CONFIG.eventq_port)

    def __getattr__(self, attr):
        """ pass all calls to dq on server """
        try:
            return getattr(self.dq, attr)
        except KeyboardInterrupt:
            # reconnect else further calls to manager fail
            self.__init__()
