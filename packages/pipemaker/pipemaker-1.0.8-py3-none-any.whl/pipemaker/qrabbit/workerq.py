#!/usr/bin/env python
import functools
import logging
import multiprocessing as mp
import pickle
from importlib import reload
from threading import Thread

from . import pika

log = logging.getLogger(__name__)

qdef = dict(queue="Workerq", auto_delete=True)


class Workerq:
    """ a task queue that executes one task at a time in a thread """

    @classmethod
    def consumers(cls, ch, **kwargs):
        return ch.queue_declare(**qdef).method.consumer_count

    def start(self, name=""):
        """ create background process as workers need to utlise cpus
        """
        self.p = mp.Process(target=self.target, daemon=True, name=name)
        self.p.start()

    def target(self):
        try:
            # consumer
            ch = pika.get_channel(
                client_properties=dict(
                    connection_name=f"workerq {mp.current_process().name}"
                )
            )
            ch.queue_declare(**qdef)
            ch.basic_qos(prefetch_count=1)
            self.tag = ch.basic_consume(
                queue="Workerq", on_message_callback=self.callback
            )
            ch.start_consuming()
            ch.connection.close()
        except:
            log.exception("Error in worker")

    def callback(self, ch, method, properties, body):
        """ callback when message received """

        def target():
            try:
                # windows must reset log settings. linux retains existing settings
                # reset both to keep common code
                from ..utils import defaultlog
                from .. import TaskqP, SharedQueueHandler

                reload(defaultlog)

                # taskqP and logqP share same channel
                chP = pika.get_channel(
                    client_properties=dict(
                        heartbeat=0,
                        connection_name=f"workerqP {mp.current_process().name}",
                    )
                )

                logging.getLogger().addHandler(SharedQueueHandler(ch=chP))
                log = logging.getLogger(__name__)

                body2 = pickle.loads(body)
                log.debug(f"Workerq: {body2}")
                if body2 == "_sentinel":
                    ch.basic_cancel(self.tag)
                    return

                body2.taskqP = TaskqP(ch=chP)
                body2.run()
            except:
                log.exception(f"Unable to handle message={body2}")
            finally:
                chP.close()
                cb = functools.partial(ch.basic_ack, method.delivery_tag)
                ch.connection.add_callback_threadsafe(cb)

        t = Thread(target=target, daemon=True, name=__name__)
        t.start()

    def stop(self):
        # note channel cannot be passed in init as process cannot pickle it
        chP = pika.get_channel()
        workerqP = WorkerqP(ch=chP)
        workerqP.put("_sentinel")
        chP.close()
        self.p.kill()


class WorkerqP:
    """ default exchange with routing to class name  """

    def __init__(self, ch=None):
        """
        :param ch: pika ch passed as parameter as can be shared by multiple queues in the same thread
        """
        self.name = self.__class__.__name__
        self.ch = ch
        ch.queue_declare(**qdef)

    def put(self, body=""):
        """ put a message on the queue
        :param body: message to send
        """
        body = pickle.dumps(body)
        self.ch.basic_publish(exchange="", routing_key="Workerq", body=body)
