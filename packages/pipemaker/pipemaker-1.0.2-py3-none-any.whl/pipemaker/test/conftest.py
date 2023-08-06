import logging
import os
from pathlib import Path

import pytest

log = logging.getLogger()

@pytest.fixture(scope="session", autouse=True)
def init_session():
    # run in test folder
    curr = os.getcwd()
    os.chdir(Path(__file__).parent)
    yield
    os.chdir(curr)


@pytest.fixture
def tmp_path(tmp_path):
    """ temporary path within test folder to avoid excessively long windows path
    e.g. pytest-23/test_saveload_csv_0
    """
    return Path().joinpath("pipemaker_test", *tmp_path.parts[-2:])


@pytest.fixture(scope="session")
def tmp_file():
    """ temp file name """
    return "temp1345736"
