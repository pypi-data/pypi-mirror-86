import logging
import pickle
from threading import Thread

from .. import WorkerqP
from . import pika

log = logging.getLogger(__name__)

qdef = dict(queue="Taskq", auto_delete=True)


class Taskq:
    """ Consumer for rabbitmq event queue """

    name = "Taskq"

    def start(self):
        def target():
            try:
                # producer for eventq and workerq
                chP = pika.get_channel(
                    heartbeat=0, client_properties=dict(connection_name="taskqP")
                )
                self.chP = chP
                self.workerqP = WorkerqP(ch=self.chP)

                # consumer
                ch = pika.get_channel(client_properties=dict(connection_name="taskq"))
                ch.queue_declare(**qdef)
                ch.basic_consume(queue=self.name, on_message_callback=self.callback)
                ch.start_consuming()
                ch.connection.close()
                chP.connection.close()
            except:
                log.exception("Error in taskq consumer")

        t = Thread(target=target, daemon=True, name=__name__)
        t.start()

    def callback(self, ch, method, properties, body):
        """ callback when message received """
        try:
            body = pickle.loads(body)
            if not body["event"] == "onProgress":
                log.debug(f"Taskq: {body}")
            getattr(self, body["event"])(body)
        except:
            log.exception(f"Error processing event {body}")
        finally:
            ch.basic_ack(method.delivery_tag)


class TaskqP:
    """ Producer for rabbitmq event queue """

    def __init__(self, ch=None):
        self.name = "Taskq"
        ch.queue_declare(**qdef)
        self.ch = ch

    def put(self, body=""):
        """ put a message on the queue
        :param body: message to send
        """
        body = pickle.dumps(body)
        self.ch.basic_publish(exchange="", routing_key=self.name, body=body)
