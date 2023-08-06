"""
This is the core file to import into any notebook or program to create a pipeline.
It is not required for the worker
"""
# import here to include in autogen (setup.py and requirements.txt)
import fs.googledrivefs
import fs_s3fs
import ipywidgets
import jupyter
import openpyxl

from pipemaker.utils.defaultlog import log
from .controller import Controller
from .pipeline import Pipeline

#  controller (scheduler, workers, view) shared by all processes
c = Controller.create()

# pipeline local to current process as wraps local functions
p = Pipeline()
"""
todo test step.set_priority
include environment in task and worker e.g. conda, python requirements, docker image + files
use delayed as joblib?
simplify pythonq rather than use same api for both
use simplequeue?
"""
