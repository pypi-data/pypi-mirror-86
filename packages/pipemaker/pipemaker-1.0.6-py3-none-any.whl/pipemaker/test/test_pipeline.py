""" test end to end pipeline """
import shutil
from pathlib import Path
from time import sleep

import pytest
import requests
import yaml

from pipemaker.examples import example1
from pipemaker.examples.example1 import make_oddeven
from pipemaker.master import c, p
from pipemaker.utils.defaultlog import log


def test_sync(tmp_path):
    """ end2end test synchronous pipeline """

    p.mode = "s"

    # pipeline
    p.root = str(tmp_path)
    p.add(example1)
    # no delay as not testing progress reporting
    p.delay = 0
    # small number of items as sequential is slow.
    n = 3

    # execute
    for low in range(n):
        p.low = low
        p.path = f"low{p.low}"
        make_oddeven()

    # check results
    for low in range(n):
        p.low = low
        p.path = f"low{p.low}"
        assert p.load("oddeven") == list(range(low, low + 6))


def run_pipeline(tmp_path):
    """ target for process so each run starts from scratch """

    # pipeline
    p.mode = "a"
    p.root = str(tmp_path)
    p.add(example1)
    # small for fast run. large enough to test progress reporting.
    p.delay = 3
    # number of paths. each path has 3 tasks. larger provides better test for multiprocessing.
    n = 20

    # check view runs and correct number of items in chart.
    assert len(make_oddeven.view().body) == 21

    # execute
    for low in range(n):
        p.low = low
        p.path = f"low{p.low}"
        make_oddeven()

    # check web view
    r = requests.get("http://localhost:5000")
    assert r.status_code == 200

    # wait for finish
    for low in range(n):
        p.low = low
        p.path = f"low{p.low}"
        make_oddeven.wait()

    # can be delay between files available and tasks finished
    for _ in range(5):
        df = c.view()
        if all(df.status == "completed"):
            break
        log.warning("waiting for tasks in scheduler to complete")
        sleep(1)

    # check results
    for low in range(n):
        p.low = low
        p.path = f"low{p.low}"
        assert p.load("oddeven") == list(range(low, low + 6))

    # check all on task list, completed, used all cpus.
    df = c.view()
    assert len(df) == n * 3
    assert all(df.status == "completed")
    assert len(df.process.unique()) == c.n_workers

    c.stop()


def run_async(qtype, tmp_path):
    """ end2end test asynchronous pipeline """

    # create test config from default
    confpath = Path(".pipemaker/config.yaml")
    confpath.parent.mkdir(exist_ok=True)
    shutil.copy(Path(__file__).parent.parent.parent / confpath, confpath)
    with confpath.open() as f:
        config = yaml.safe_load(f)
    config["qtype"] = qtype
    with confpath.open("w") as f:
        f.write(yaml.dump(config))

    run_pipeline(tmp_path)
    shutil.rmtree(confpath.parent)


def test_async(tmp_path):
    run_async("python", tmp_path)
