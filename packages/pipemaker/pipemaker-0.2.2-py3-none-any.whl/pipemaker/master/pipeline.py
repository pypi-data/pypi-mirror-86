import inspect
import logging
import os
import types

from fs.move import move_dir

from .. import CONFIG, TaskqP
from ..filesystem import Filepath, Fpath
from ..qrabbit import pika
from ..utils import dotdict
from .step import Step

log = logging.getLogger(__name__)

HOME = os.path.expanduser("~")


class Pipeline:
    """ pipeline of steps that convert inputs into outputs """

    def __init__(self):
        """
        fpath: user defined fstring that is formatted at runtime with name and pipeline.context).
        Default is "{root}/{path}/{name}{ext}"::

            root: root data path. can be relative, absolute or any pyfilesystem path.
            path: subpath to separate runs e.g. pilot, full; london, paris; january, february
            name: filled with name of function output often func.__name__
            ext: output file format e.g. .pkl, .xlsx

        rest of pipeline attributes are used to fill parameters at runtime. Example usage:

            * value used as a parameter for a function or any upstream function
            * Filepath to map a data item shared by multiple runs to a common location
            * Filepath to map a file to a remote location
        
        """
        self.mode = CONFIG.mode

        if CONFIG.qtype == "rabbitmq":
            self.ch = pika.get_channel(
                heartbeat=0, client_properties=dict(connection_name="pipeline"),
            )
            self.taskqP = TaskqP(ch=self.ch)
        else:
            self.taskqP = TaskqP()

        # format string for file locations
        self.fpath = Fpath("{root}/{path}/{name}{ext}")

        # recycle bin for deleted files
        self.recycle = CONFIG.recycle.replace("~", HOME)

        # these are the default used to fill fpath at runtime
        # the fpath can be set to any fstring. it will be filled at runtime by pipeline.context + name
        self.context = dotdict()
        c = self.context
        c.root = CONFIG.root
        c.path = ""
        c.ext = ".pkl"

        # map output to function that can produce it
        self._output2step = dict()

        # controller functions
        self.start = None
        self.stop = None

        # lock to new attributes. store in self.context instead
        self._lock = True

    def __setattr__(self, key, value):
        """ new variables added to pipeline after __init__ are put in context """
        # set var in object directly
        if (
            key in vars(self)
            or isinstance(vars(self.__class__).get(key), property)
            or key.startswith("_")
            or not self.__dict__.get("_lock")
        ):
            super().__setattr__(key, value)
            return

        # set var in self.context
        if not hasattr(self.context, key):
            # warning to highlight any spelling mistakes
            log.warning(f"added new variable {key} to context")
        setattr(self.context, key, value)

    def __getattr__(self, key):
        """ fallback to context if attribute does not exist """
        if hasattr(self.context, key):
            return self.context[key]
        else:
            # enable hasattr to return False
            raise AttributeError

    def add(self, step):
        """ add steps to the pipeline

        :param step: function or module

        ..warning:: refers to calling frame so if moved then need to update the code to refer to correct frame
        """
        try:
            frame = inspect.currentframe()
            bglobals = frame.f_back.f_globals

            if not inspect.ismodule(step) and not inspect.isfunction(step):
                raise Exception("add parameter should be either a module or a function")

            if step.__name__.startswith("_"):
                return

            # add function
            if inspect.isfunction(step):
                bglobals[step.__name__] = self._wrap_func(step)

            elif inspect.ismodule(step):
                # add all functions in module
                for k, v in inspect.getmembers(step, inspect.isfunction):
                    # exclude starting _ or functions imported inside module
                    if v.__name__.startswith("_") or (v.__module__ != step.__name__):
                        continue

                    # set module.func
                    setattr(step, k, self._wrap_func(v))

                    # set directly imported i.e, from module import *; from module import func
                    if k in bglobals:
                        bglobals[k] = self._wrap_func(v)
        finally:
            # recommended to avoid memory leaks
            del frame

    def name2filepath(self, name):
        """ convert name to filepath

        :param name: internal pipe name
        :return: pyfs filepath to physical location
        """
        path = getattr(self, name, self.fpath).format(name=name, **self.context)
        return Filepath(path)

    def load(self, name):
        """ load data
        :param name: internal pipe name
        :return: contents of file
        """
        fp = self.name2filepath(name)
        try:
            return fp.load()
        except FileNotFoundError:
            log.error(f"File not found {self.url}")

    def save(self, obj, name):
        """ save data
        
        :param obj: data to save
        :param name: filename or pyfs url
        """
        fp = self.name2filepath(name)
        fp.save(obj)

    def _wrap_func(self, f):
        """ wrap function to create a Step """
        step = Step(self, f)
        if not hasattr(step, "oname"):
            log.warning(f"{f.__name__} has no oname so not included in pipe")
            return f
        # store so steps can search for upstream steps to _add_func their inputs.
        self._output2step[step.oname] = step
        return step

    def reset_files(self, path=None):
        """ move files to self.recycle. mostly used for testing and examples to reset everything.
        :param path: path to reset. None means p.root.
        """
        if path is None:
            src = Filepath(self.root)
        else:
            src = Filepath(f"{self.root}/{path}")
        if src.exists() and src.isdir():
            dst = Filepath(f"{self.recycle}/{src.path}")
            dst.makedirs(recreate=True)
            log.info(f"moving {src.path} to {dst.path}")
            move_dir(src.fs, src.path, dst.fs, dst.path)

    def load_all(self, name):
        """ load all data """
        names = []
        for path in os.listdir(self.root):
            self.path = path
            res = None
            try:
                res = self.load(name)
            except:
                log.exception("")
            names.append(res)
        log.info(f"loaded {len(names)} {name}")
        return names

    def reset(self):
        """ reset wrapped functions
        mostly used for testing
        """
        # reset pipemaker objects and files
        self.__init__()

        # reset wrapped functions
        # typically relevant stack is 1 or 2 back so 5 should be plenty.
        currframe = inspect.currentframe()
        frame = currframe.f_back
        for _ in range(4):
            bglobals = frame.f_globals
            for k, v in bglobals.items():
                if isinstance(v, Step):
                    # from example import func
                    bglobals[k] = v.func
                elif hasattr(v, "__loader__"):
                    # import example
                    for k2, v2 in vars(v).items():
                        if isinstance(v2, Step):
                            setattr(v, k2, v2.func)
            frame = frame.f_back
            if not frame:
                break
        del currframe
