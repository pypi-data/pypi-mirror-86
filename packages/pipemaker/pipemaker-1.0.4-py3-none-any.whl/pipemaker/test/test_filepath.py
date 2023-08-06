import os
import sys

import pandas as pd
import pytest

from pipemaker.filesystem import Filepath


def test_root_exists(tmp_file):
    # local
    if sys.platform.startswith("win"):
        assert Filepath("d:").exists()
        assert not Filepath(f"{tmp_file}:").exists()

    # s3
    assert Filepath("s3://simonm3").exists()
    assert not Filepath(f"s3://{tmp_file}").exists()

    # googledrive
    assert Filepath(f"googledrive:/").exists()


@pytest.mark.parametrize(
    "fs1", ["", "s3://simonm3", "googledrive:"],
)
def test_exists(fs1, tmp_path, tmp_file):
    """ test folder and file """

    tmp_path = f"{fs1}/{str(tmp_path)}"

    # gitlab CI tmp_path=pytest-0 every time so need to reset.
    if "DOCKER" in os.environ:
        try:
            Filepath(tmp_path).removetree()
        except:
            pass

    # folder
    fp = Filepath(tmp_path)
    assert not fp.exists()
    fp.makedirs()
    assert fp.exists()

    # file
    fp = Filepath(f"{tmp_path}/{tmp_file}")
    assert not fp.exists()
    with fp.open("w") as f:
        f.write("")
    assert fp.exists()


@pytest.mark.parametrize(
    "fs1", ["", "s3://simonm3", "googledrive:"],
)
@pytest.mark.parametrize("ext", [".pkl", ".csv", ".xlsx"])
def test_saveload(fs1, ext, tmp_path, tmp_file):

    # define data. note explicitly set cols else in memory is range and fails assertion
    data = pd.DataFrame([dict(a=6, b=3), dict(a=7, b=9, c="hello")])

    # save
    fp = Filepath(f"{fs1}/{str(tmp_path)}/{tmp_file}{ext}")
    fp.save(data)
    assert fp.exists()

    # load
    loaded = fp.load()
    assert loaded.equals(data)
