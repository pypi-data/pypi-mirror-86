import inspect
import logging
import multiprocessing as mp
import sys
from datetime import datetime

import fs
from graphviz import Digraph

from .. import Eventq
from ..filesystem import Filepath, Fpath
from ..worker import Task

log = logging.getLogger(__name__)


class Step:
    """
    Represents a step in the pipeline
    Identifies upstream tasks; executes or sends tasks to the taskq
    """

    def __init__(self, pipeline, func):
        """
        :param pipeline: pipeline that links all the steps
        :param func:    function to wrap
        """
        self.pipeline = pipeline
        self.func = func

        # output path. required here as pipe uses it as a unique id
        sig = inspect.signature(func)
        if sig.return_annotation != inspect.Parameter.empty:
            self.oname = sig.return_annotation
        elif self.func.__name__.startswith("make_"):
            self.oname = self.func.__name__[len("make_") :]
        elif self.func.__name__.startswith("get_"):
            self.oname = self.func.__name__[len("get_") :]
        else:
            self.oname = self.func.__name__

    def __repr__(self):
        """ :return func(**params)->output """
        params = ",".join(
            str(p) for p in inspect.signature(self.func).parameters.values()
        )
        return f"{self.func.__name__}({params})->{repr(self.parse_output())}"

    def __call__(self, *args, **kwargs):
        """ called in same way as underlying function would be called e.g. make_thing(5, a=3)
        used for initiating task only. upstream tasks called via run
        """
        log.debug(f"CALLED {self.oname} WITH {vars(self.pipeline)}")

        # validate
        if self.pipeline.mode not in ("s", "a"):
            raise Exception("Invalid pipeline.mode")

        # check output exists
        output = self.parse_output()
        if output.exists():
            if self.pipeline.mode == "a":
                return
            elif self.pipeline.mode == "s":
                return output.load()

        log.debug(f"running with mode={self.pipeline.mode}")

        # run task
        if self.pipeline.mode == "s":
            return self.run_s(*args, **kwargs)

        elif self.pipeline.mode == "a":
            self.run_a(*args, **kwargs)
            return self

    def run_s(self, *args, **kwargs):
        """ run tasks synchronously """
        inputs = self.parse_inputs(*args, **kwargs)
        self.output = self.parse_output()

        # load
        indata = dict()
        for k, v in inputs.items():
            if not isinstance(v, Filepath):
                indata[k] = v
            elif v.exists():
                indata[k] = v.load()
            else:
                utask = self.pipeline._output2step.get(k)
                if not utask:
                    log.error(f"missing {k}")
                    sys.exit(1)
                indata[k] = utask.run_s(*args, **kwargs)

        # execute and save
        log.info(f"creating {self.output.url}")
        outdata = self.func(**indata)
        self.output.save(outdata)
        return outdata

    def run_a(self, *args, **kwargs):
        """ submit tasks to taskqP for asynchronous processing on multiple cpus """
        # validate parameters including upstream pipe
        tasks = dict()
        missing = []
        self.get_tasks(tasks, missing, *args, **kwargs)
        if missing:
            log.error(f"Missing inputs {missing}")
            sys.exit(0)

        body = dict(
            tasks=tasks,
            time=datetime.now(),
            event="onRun",
            process=mp.current_process().name,
            source="Step",
        )
        self.pipeline.taskqP.put(body)

    def get_tasks(self, tasks, missing, *args, **kwargs):
        """ recursively get tasks and missing for upstream pipe
        enables all missing parameters to be identified before execution

        :param tasks: dict(url=task) that is populated recursively
        :param missing: list of missing parameters populated recursively
        :param args: args passed on execution
        :param kwargs: kwargs passed on execution
        """
        # create taskq task
        output = self.parse_output()
        inputs = self.parse_inputs(*args, **kwargs)
        task = Task(self.func.__module__, self.func.__name__, inputs, output)
        task.upstream = set()
        task.downstream = set()
        task.name = str(task.output)
        task.url = task.output.url

        tasks[task.url] = task

        # process inputs
        for k, v in inputs.items():
            # existing input data
            if not isinstance(v, Filepath) or v.exists():
                continue
            # get step to make data
            arg = self.pipeline._output2step.get(k)
            if not arg:
                # no step found i.e. missing input data
                missing.append(k)
            else:
                # add step to upstream tasks
                upstream_url = arg.parse_output().url
                if upstream_url not in tasks:
                    arg.get_tasks(tasks, missing)
                task.upstream.add(upstream_url)
                tasks.get(upstream_url).downstream.add(task.url)

    def wait(self):
        """ wait for task to finish
        Usage:: wait for output before proceeding to next cell in notebook
        """
        output = self.parse_output()
        if output.exists():
            return
        Eventq().get(output.url)

    def parse_output(self):
        """ path to output file """
        p = self.pipeline
        v = getattr(p, self.oname, p.fpath)
        if isinstance(v, Filepath):
            return v
        return Filepath(v.format(name=self.oname, **p.context))

    def parse_inputs(self, *args, **kwargs):
        """ return inputs

        :param args:    args passed to function at runtime
        :param kwargs:  kwargs passed to function at runtime
        :return:        dict of name=value where value is parameter value or filepath

        inputs can be data, Fpath or Filepath. They are populated from:

            * runtime args/kwargs
            * global parameter e.g. pipeline.input=2
            * default parameter e.g. def myfunc(input1=2)
            * default Fpath

        Each Fpath is formatted using pipeline.context to create a Filepath
        """
        p = self.pipeline

        # run_time args and arguments as passed above.
        sig = inspect.signature(self.func)

        # map *args, **kwargs onto signature. partial as some are set in env rather than passed directly.
        bind = sig.bind_partial(*args, **kwargs)
        arguments = bind.arguments.copy()

        # fill parameters. they can be data, Fpath or Filepath
        # iterate over sig to map parameters to env
        #     bind.args has no name so cannot map parameter name to Fpath. bind.kwargs cannot be updated.
        #     bind.arguments excludes default parameters and does not expose kwargs key
        for k, v in sig.parameters.items():
            # flatten kwargs
            if v.kind == v.VAR_KEYWORD:
                arguments.update(arguments[k])
                del arguments[k]
                continue

            # bound from function call
            if k in arguments:
                pass
            # global specific to parameter
            elif k in p.context:
                arguments[k] = p.context[k]
            # default parameter
            elif v.default != inspect.Parameter.empty:
                arguments[k] = v.default
            # global default
            else:
                arguments[k] = p.fpath

        # convert Fpath to Filepath
        arguments = {
            k: Filepath(v.format(name=k, **p.context)) if isinstance(v, Fpath) else v
            for k, v in arguments.items()
        }

        return arguments

    def reset_files(self):
        """ delete output and remove task """
        try:
            self.parse_output().remove()
        except fs.errors.ResourceNotFound:
            pass
        self.delete()

    def delete(self):
        """ delete task """
        body = dict(
            url=self.parse_output().url,
            time=datetime.now(),
            event="onDelete",
            process=mp.current_process().name,
        )
        self.pipeline.taskqP.put(body)

    def set_priority(self, priority):
        """ set priority for task and upstream """
        body = dict(
            url=self.parse_output().url,
            time=datetime.now(),
            event="onSetPriority",
            process=mp.current_process().name,
            priority=priority,
        )
        self.pipeline.taskqP.put(body)

    def view(self, g=None, parents=False):
        """ return graphviz display of upstream pipe

        :param g: existing graph. passed recursively to view parents
        :param parents: False views tasks that need to be run. True views all upstream tasks
        """
        p = self.pipeline

        # create graph on first call
        if g is None:
            g = Digraph(strict=True, comment=f"{self.func.__name__} pipe")

        # display formats
        func_style = dict(shape="oval", style="filled", fillcolor="lightgrey")
        exists_style = dict(
            shape="folder",
            height=".1",
            width=".1",
            style="filled",
            fillcolor="lightgreen",
        )
        missing_style = dict(shape="folder", height=".1", width=".1", style="")
        pexists_style = dict(shape="box", style="filled", fillcolor="lightgreen")
        pmissing_style = dict(shape="box", style="")

        # function
        g.node(self.func.__name__, **func_style)

        # inputs
        inputs = self.parse_inputs()
        for k, v in inputs.items():
            if isinstance(v, Filepath):
                if v.exists():
                    g.node(k, **exists_style)
                    g.edge(k, self.func.__name__)
                    if parents:
                        pw = p._output2step.get(k)
                        if pw is not None:
                            pw.view(g, parents)
                else:
                    upstream = p._output2step.get(k)
                    if upstream:
                        # no file but a task can create it
                        upstream.view(g, parents)
                        g.edge(k, self.func.__name__)
                    else:
                        # no parameter. no file. no task to create it.
                        g.node(k, **pmissing_style)
                        g.edge(k, self.func.__name__)
            else:
                # supplied parameter
                g.node(k, **pexists_style)
                g.edge(k, self.func.__name__)

        # output
        output = self.parse_output()
        if output.exists():
            g.node(str(output), **exists_style)
        else:
            g.node(str(output), **missing_style)

        g.edge(self.func.__name__, str(output))

        return g
