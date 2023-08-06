#!python

from pipemaker.master import p

import os
import sys
import yaml
import logging
log = logging.getLogger()

def f1(f1):
    log.info("f1")

def f2():
    log.info("f2")

def f3(f2):
    log.info("f3")

log.info("START")
mod = sys.modules[__name__]
log.info(mod)
p.add(mod)
#[v for v in list(globals().values()) if isinstance(v, types.FunctionType) and v.__module__=="__main__"]
f3()

