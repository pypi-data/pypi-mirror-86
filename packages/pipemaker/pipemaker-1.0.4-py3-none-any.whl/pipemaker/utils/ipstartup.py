"""
setup jupyter for data analysis. 
"""
import logging

################## common ################################
import os
import sys
import warnings
from os.path import expanduser, join

import numpy as np

################## analysis ################################
import pandas as pd
from IPython import get_ipython
from IPython.display import HTML, Image
from IPython.display import display as d
from tqdm.notebook import tqdm

from .defaultlog import log

if log.getEffectiveLevel() > logging.DEBUG:
    warnings.filterwarnings("ignore")


def flog(text):
    """ for finding logging problems """
    with open("c:/flog.txt", "a") as f:
        f.write(str(text))


################## extensions ################################
try:
    get_ipython().magic("load_ext autoreload")
except:
    log.exception("")
try:
    get_ipython().magic("autoreload 2")  # autoreload all modules
except:
    log.exception("")


def wide():
    """ makes notebook fill screen width """
    d(HTML("<style>.container { width:100% !important; }</style>"))
