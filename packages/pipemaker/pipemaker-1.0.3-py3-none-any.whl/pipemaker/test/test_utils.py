import logging
import pickle

from pipemaker.utils.dotdict import autodict, dotdict

log = logging.getLogger()


def test_dotdict():
    """ test create, pickle, unpickle, start """

    # create
    dt = dotdict()
    dt.a = 123
    dt.b = "hello"

    # pickle and unpickle
    dt = pickle.loads(pickle.dumps(dt))

    # check results
    assert isinstance(dt, dotdict)
    assert dt.a == 123
    assert dt.b == "hello"


def test_autodict():
    """ test create, pickle, unpickle, start """

    def check(dt):
        assert isinstance(dt, autodict)
        assert dt.a == 123
        assert dt.b == "hello"
        assert dt.c.d == "goodbye"
        assert isinstance(dt.c, autodict)

    # create
    dt = autodict()
    dt.a = 123
    dt.b = "hello"
    dt.c.d = "goodbye"
    check(dt)

    # pickle and unpickle
    dt = pickle.loads(pickle.dumps(dt))
    check(dt)
