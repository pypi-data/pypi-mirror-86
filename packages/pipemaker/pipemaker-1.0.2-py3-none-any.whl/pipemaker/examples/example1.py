""" simple example """

import inspect
import logging
from time import sleep

from tqdm.auto import trange

from pipemaker.worker.task import progress

log = logging.getLogger(__name__)


def _delay(delay=60, desc=None):
    """ add a delay to simulate long running task """
    # label bars as can be many at same time
    try:
        desc = inspect.currentframe().f_back.f_back.f_locals["self"].output.url
    except:
        # luigi raises exception as cannot access url as above. does not show progress bars anyway.
        desc = ""
    for i in trange(delay, desc=desc):
        sleep(1)
        progress(i, delay)


def make_odd(low, delay=60):
    """ return list of 3 odd numbers """
    if low % 2 == 0:
        low = low + 1
    r = range(low, low + 6, 2)
    _delay(delay)
    return list(r)


def make_even(low, delay=60):
    """ return list of 3 even numbers """
    if low % 2 != 0:
        low = low + 1
    r = range(low, low + 6, 2)
    _delay(delay)
    return list(r)


def make_oddeven(odd, even, delay=60):
    """ concatenate odd and even """
    r = odd + even
    _delay(delay)
    return sorted(r)
