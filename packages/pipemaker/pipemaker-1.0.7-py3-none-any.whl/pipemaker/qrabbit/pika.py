import logging

import pika

from .. import CONFIG, CREDS

log = logging.getLogger(__name__)


def get_channel(**params):
    """ return a new rabbit channel on a new connection
    :param params: additional parameters for connection

    connection is a tcp connection
    channel enables multiplexing over a single connection
    queue requires a channel
    
    amqp suggests producer connection/process and channel/thread
    in practice channels are not thread safe either
    ==> consumer connection/channel is blocking in a thread
    ==> producer connection/thread
    ==> can have multiple channels in a thread but no clear benefit

    connections can be named whereas channels cannot
    cloudamqp free plan has maximimum 20 connections
    """
    c = CREDS[CONFIG.qtype]
    params.update(
        host=c.host,
        credentials=pika.PlainCredentials(c.user, c.password),
        virtual_host=c.vhost,
        socket_timeout=5,
    )
    params = pika.connection.ConnectionParameters(**params)
    connection = pika.BlockingConnection(params)
    channel = connection.channel()
    return channel
