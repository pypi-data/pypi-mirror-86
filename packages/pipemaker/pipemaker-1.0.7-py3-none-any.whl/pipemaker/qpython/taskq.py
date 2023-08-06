import logging
from queue import Queue
from threading import Thread

from .. import CONFIG, WorkerqP
from ..utils.share import create_client, create_server

log = logging.getLogger(__name__)


class Taskq:
    """ Consumer for python event queue """

    @classmethod
    def start_server(self):
        self.q = Queue()
        create_server(self.q, CONFIG.taskq_port)

    def start(self):
        self.workerqP = WorkerqP()

        # not needed for pythonq but must exist
        self.chP = None

        def target():
            try:
                while True:
                    body = self.q.get()
                    if body == "_sentinel":
                        break
                    if not body["event"] == "onProgress":
                        log.debug(f"Taskq: {body}")
                    getattr(self, body["event"])(body)
            except:
                log.exception(f"Error processing event {body}")

        t = Thread(target=target, daemon=True, name=__name__)
        t.start()

    def stop(self):
        self.q.put("_sentinel")


class TaskqP:
    """ Producer for python event queue """

    def __init__(self, **kwargs):
        self.q = create_client(CONFIG.taskq_port)

    def put(self, body):
        self.q.put(body)
