#!/usr/bin/env python
import logging
import multiprocessing as mp
from importlib import reload
from queue import Queue

from .. import CONFIG
from ..utils.share import create_client, create_server

log = logging.getLogger(__name__)


class Workerq:
    """ a task queue that executes one task at a time """

    @classmethod
    def start_server(self):
        self.q = Queue()
        create_server(self.q, CONFIG.workerq_port)

    def start(self, name=""):
        """ create consumer process as workers need to utlise cpus
        """
        self.p = mp.Process(target=self.target, daemon=True, name=name)
        self.p.start()

    def target(self):
        from ..utils import defaultlog
        from .. import TaskqP, SharedQueueHandler

        # force reset else fork (linux) retains existing settings
        reload(defaultlog)
        logging.getLogger().addHandler(SharedQueueHandler())
        log = logging.getLogger(__name__)

        q = create_client(CONFIG.workerq_port)
        while True:
            body = q.get()
            log.debug(f"Workerq: {body}")
            if body == "_sentinel":
                break
            try:
                body.taskqP = TaskqP()
                body.run()
            except:
                log.exception(f"Unable to handle message={body}")

    def stop(self):
        self.q.put("_sentinel")
        self.p.join(1)
        self.p.kill()


class WorkerqP:
    def __init__(self, **kwargs):
        self.q = create_client(CONFIG.workerq_port)

    def put(self, body=""):
        self.q.put(body)
