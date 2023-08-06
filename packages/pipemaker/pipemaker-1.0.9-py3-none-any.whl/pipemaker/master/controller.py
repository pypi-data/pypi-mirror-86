import inspect
import logging
import os
import shlex
import subprocess
from time import sleep

from .. import CONFIG, Eventq, FileHandler, SharedQueueHandler, Taskq, Workerq
from ..qrabbit import pika
from ..utils import get_name
from ..utils.share import create_client, create_server, port_used
from ..web import view
from .scheduler import Scheduler

log = logging.getLogger(__name__)


class Controller:
    """ controller for scheduler, workers
    """

    @classmethod
    def create(cls):
        """ controller, scheduler, workers shared between sessions and machines """

        if not port_used(CONFIG.controller_port):
            # primary session
            c = Controller()
            create_server(c, CONFIG.controller_port)
            if CONFIG.mode == "a":
                c.start()
            return c
        else:
            # secondary session uses shared workers, scheduler.
            return create_client(CONFIG.controller_port)

    def __init__(self):
        self.n_workers = os.cpu_count()
        # set explicitly or it logs info message
        os.environ["NUMEXPR_NUM_THREADS"] = str(os.cpu_count())

        # set on start
        self.scheduler = None
        self.ch = None
        self.workers = []
        self.filehandler = None

    def get_n_workers(self):
        """ expose to proxy client """
        return self.n_workers

    def set_n_workers(self, value):
        """ expose to proxy client """
        # avoid annoying warning
        os.environ["NUMEXPR_NUM_THREADS"] = str(value)
        self.n_workers = value

    def view(self):
        """ expose to proxy client """
        return self.scheduler.view()

    def start(self):
        """ start log, web view, taskq, workers
        """
        log.debug(f"starting controller with config: {CONFIG}")

        # web server thread. takes time so start early
        view.start()

        # queues
        if CONFIG.qtype == "python":
            # python queues need a server. these are started first otherwise later steps will fail.
            log.debug("starting servers")
            Workerq.start_server()
            Taskq.start_server()
            Eventq.start_server()
            SharedQueueHandler.start_server()
            log.debug("python queue servers running")
        else:
            # rabbitmq server is assumed already running so just need a channel.
            if not self.ch or self.ch.is_closed:
                self.ch = pika.get_channel(
                    heartbeat=0,
                    client_properties=dict(connection_name="controller_start"),
                )

        # logging
        log.debug(f"starting logging")
        self.filehandler = FileHandler(os.path.expanduser("~") + "/pipemaker.log")
        rootlog = logging.getLogger()
        rootlog.addHandler(SharedQueueHandler(ch=self.ch))

        # workers
        name = get_name()
        for i in range(self.n_workers):
            if i == 0:
                log.debug(f"starting workers {name} n={self.n_workers}")
            w = Workerq()
            w.start(f"{name}_{i}")
            self.workers.append(w)
        # wait for workers to start. tasks launched on rabbitmq before consumers ready will be ignored.
        # python queue does not reveal consumers
        if CONFIG.qtype == "rabbitmq":
            while Workerq.consumers(self.ch) < self.n_workers:
                sleep(1)

        # scheduler. this consumes taskq and can add, delete, view workers
        log.debug(f"starting scheduler")
        self.scheduler = Scheduler()
        self.scheduler.start(self.workers)

    def stop(self):
        """ close log, web view, taskq, workers; and delete temp files """
        # close web server
        if view.server:
            log.debug("stopping flask server")
            view.stop()

        # workers
        for w in self.workers:
            w.stop()

        # reset logging to remove any queue handlers before deleting queues
        if self.filehandler:
            self.filehandler.close()
            rootlog = logging.getLogger()
            rootlog.removeHandler(rootlog.handlers[-1])

        # rabbit queues
        if CONFIG.qtype == "rabbitmq":
            if not self.ch or self.ch.is_closed:
                self.ch = pika.get_channel(
                    heartbeat=0,
                    client_properties=dict(connection_name="controller_stop"),
                )
            ch = self.ch
            for q in ["Workerq", "Taskq", "Logq", "Eventq"]:
                ch.queue_delete(q)
            ch.connection.close()
            self.ch = None

        self.__init__()

    def kill(self):
        """ restart local rabbitmq server deleting all queues.
        
        .. warning:: this is the nuclear option for testing
        """

        def subprocess_run(cmd):
            cmd = shlex.split(cmd)
            subprocess.run(cmd, capture_output=True, check=True, shell=True)

        log.info("restarting rabbitmq broker")
        subprocess_run("rabbitmqctl stop_app")
        subprocess_run("rabbitmqctl reset")
        subprocess_run("rabbitmqctl start_app")
