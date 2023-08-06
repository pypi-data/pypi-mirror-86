"""
convenience functions for sharing objects with multiple processes or machines
e.g.
    # initiate server
    obj = Something()
    s = create_server(obj, 9999)

    # initiate client in any process
    c = create_client(9999)
"""
import logging
import socket
from multiprocessing.managers import BaseManager
from threading import Thread

from .retry import Retry

log = logging.getLogger(__name__)


def port_used(address):
    """ return True/False if port responds
    :param address: tuple (ip, port) or int port
    """
    if isinstance(address, int):
        address = ("127.0.0.1", address)
    try:
        with socket.socket() as s:
            # 10 ms timeout
            s.settimeout(0.01)
            s.connect(address)
            return True
    except:
        return False


def create_server(obj, address, authkey=b"aaa"):
    """ start server to share object with multiple processes

    :param obj: object to publish on server
    :param address: tuple (ip, port) or int port
    :param authkey: binary key to be used by server and client
    """
    if isinstance(address, int):
        address = ("127.0.0.1", address)

    def target(obj):
        try:
            Manager.register("get_obj", callable=lambda: obj)
            m = Manager(address, authkey=authkey)
            try:
                s = m.get_server()
                s.serve_forever()
            except OSError:
                log.exception(
                    f"tried to start server but port in use. increase timeout {address}"
                )
        except:
            log.exception("error creating server")

    class Manager(BaseManager):
        pass

    # 5ms to check versus 2 seconds to start thread and server
    if port_used(address):
        log.debug(f"server already running at {address}")
        return

    t = Thread(target=target, daemon=True, args=(obj,), name=f"create_server {address}")
    t.start()

    # wait until running
    Retry()(create_client)(address, authkey)


def create_client(address, authkey=b"aaa"):
    """ return client to use object in multiple processes

    ::param address: tuple (ip, port) or int port
    :param authkey: binary key to be used by server and client
    :return: proxy_object for use in processes
    """
    if isinstance(address, int):
        address = ("127.0.0.1", address)

    # redefined here as must be different class to the create_server but with same name
    class Manager(BaseManager):
        pass

    Manager.register("get_obj")
    m = Manager(address, authkey=authkey)
    m.connect()
    return m.get_obj()
