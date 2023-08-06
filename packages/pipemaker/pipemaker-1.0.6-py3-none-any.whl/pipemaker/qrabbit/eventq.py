import logging
import pickle

from . import pika

log = logging.getLogger(__name__)

# ttl enables producer to generate message before consumer has started. expires deletes queue if no consumers
qdef = dict(arguments={"x-message-ttl": 500, "x-expires": 1000})


class Eventq:
    """
    Usage:
        # wait for an event to happen
        data = Eventq().get("eventkey")

        # trigger event
        Eventq().put("eventkey", data)
    """

    def get(self, key, **kwargs):
        """ start for one event; close; return response (must be outside __init__)
        no need for thread as callback is short and only called once
        :param key: unique routing key e.g name of file OR random string
        :param timeout: if exceeded then call callback_timeout
        :return: response data captured
        """
        ch = pika.get_channel(client_properties=dict(connection_name="eventq"))
        timeout = kwargs.pop("timeout", None)
        if timeout:
            ch.connection.call_later(timeout, self.callback_timeout)

        # ttl enables producer to generate message before consumer has started
        # expires deletes queue if no consumers
        ch.queue_declare(queue=key, **qdef)
        ch.basic_consume(queue=key, on_message_callback=self.callback, **kwargs)
        ch.start_consuming()
        ch.connection.close()
        return self.response

    def callback(self, ch, method, properties, body):
        """ when message received then set response and close """
        self.response = None
        if body:
            self.response = pickle.loads(body)
        ch.basic_ack(method.delivery_tag)
        ch.stop_consuming()

    def callback_timeout(self):
        """ callback when timeout exceeded """
        raise TimeoutError()

    def put(self, key, body="", ch=None):
        """
        :param key: unique routing key e.g name of file OR random string
        :param ch: shared ch
        :param body: data to be returned to consumer. None if just notifying event happened.
        """
        ch.queue_declare(queue=key, **qdef)
        if body:
            body = pickle.dumps(body)
        ch.basic_publish(exchange="", routing_key=key, body=body)
