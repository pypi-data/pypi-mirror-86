import importlib
import logging
import os
from functools import partial
from pathlib import Path
from urllib.parse import urlencode, urlparse
import sys

import fs
import fs.path
from fs.copy import copy_file

from pipemaker.utils.dotdict import dotdict

from .creds import gdrive

log = logging.getLogger(__name__)


class Fpath(str):
    """ a fstring that will be formatted into a Filepath. methods return Fpath objects
    Used to distinguish path strings from strings when passed to functions or printed
    """

    def __repr__(self):
        """ with class """
        return f"Fpath({self})"


class Filepath:
    """ single representation of file to wrap url, path, pyfs_url, pyfs_path

        * simpler api for most common usage. still can access underlying parts if needed.
        * one step methods e.g. exists, isdir
        * additional methods for interactive use in notebook e.g. load, save
    """

    # dict(fs=connection) cache as files on same filesystem can share one connection
    maxcache = 100
    cons = dict()

    def __init__(self, url):
        """
        splits fs, path, query for pyfilesystem:
        
        * fs includes url up to path e.g. "s3://bucket1"; "c:/"
        * path relative to fs
        * query incudes ? e.g. googledrivefs authorisation

        :param url: e.g. myfile, /myfile, c:/myfile, s3://simonm3/mypath, googledrive:///log.txt
        note:: aws requires netloc=bucket and googledrive netloc=folder
        """
        # convert from Path or Fpath
        url = str(url)
        url = url.replace("\\", "/")
        parsed = urlparse(url)

        # query creds
        self.query = ""
        if parsed.query:
            self.query = f"?{parsed.query}"
        # automatically add googledrive creds as with s3
        elif parsed.scheme == "googledrive":
            self.query = gdrive()

        # fs
        if not parsed.scheme:
            # local
            if parsed.path.startswith("/"):
                # absolute. / in fs enables paths outside current folder.
                self.fs = "/"
            else:
                # relative to current folder
                self.fs = ""
        elif sys.platform=="win32" and len(parsed.scheme) == 1:
            # windows local drive
            self.fs = f"{parsed.scheme}:/"
        elif parsed.scheme:
            # remote filesystem
            self.fs = f"{parsed.scheme}://{parsed.netloc}"

        # path. remove backrefs, duplicated separators
        self.path = fs.path.normpath(parsed.path)

    def __getstate__(self):
        """ required for pickle """
        return self.__dict__

    def __setstate__(self, d):
        """ required for pickle """
        self.__dict__ = d

    @property
    def ofs(self):
        """ return open filesystem here rather than __init__ as cannot be pickled """
        cons = self.cons

        # already in cache (share connection as many files use same filesystem)
        try:
            return cons[self.fs]
        except KeyError:
            pass

        # cache connections as 500ms overhead
        cons[self.fs] = fs.open_fs(f"{self.fs}{self.query}")
        if len(cons) > self.maxcache:
            cons.pop(cons.keys()[0])

        return cons[self.fs]

    @property
    def islocal(self):
        """ is local file system
        :return: True if local file system 
        """
        return isinstance(self.ofs, fs.osfs.OSFS)

    @property
    def url(self):
        """ filesystem and path. excludes query. excludes file://
        :return: standard format url (strips // if at the end of pyfs_url).
        Note the same file can have multiple urls with different filesystem roots
        """
        fs1 = self.fs.rstrip("/")
        return f"{fs1}{self.path}"

    def __repr__(self):
        """ class and url """
        return f"Filepath({self.url})"

    def __str__(self):
        """ basename without extension. useful for display as short name """
        filename = fs.path.basename(self.path)
        return fs.path.splitext(filename)[0]

    def _ipython_display_(self):
        """ define how jupyter notebook displays. Slow without this as tries multiple alternatives. """
        print(repr(self))

    def __hash__(self):
        """ unique key for dict """
        return hash(self.url)

    def __eq__(self, other):
        """ equal if have same url """
        return self.url == other.url

    def __getattr__(self, attr, *args, **kwargs):
        """ shortcut to ofs.method(path, *args, **kwargs) """
        if attr == "_ipython_canary_method_should_not_exist_":
            raise AttributeError
        if hasattr(self.ofs, attr) and callable(getattr(self.ofs, attr)):
            return partial(getattr(self.ofs, attr), self.path, *args, **kwargs)
        raise AttributeError

    def _get_driver(self, driver=None):
        """
        :param driver: name of driver to load/save. if None uses file extension or pkl
        :return: driver module
        """
        if driver is None:
            driver = fs.path.splitext(self.path)[-1] or ".pkl"
            driver = driver[1:]
        try:
            return importlib.import_module(f"pipemaker.filesystem.filedrivers.{driver}")
        except ModuleNotFoundError:
            log.error(
                f"No driver found for {driver}. You can _add_module one in the filedrivers folder."
            )
            raise

    def exists(self):
        if self.path in ["", "/"]:
            try:
                # use listdir as exists is always true for s3; and always fails for googledrive
                self.listdir()
                return True
            except:
                return False
        try:
            return self.ofs.exists(self.path)
        except:
            # fails for s3 bucket that exists but has no permissions
            return False

    def dirname(self):
        return fs.path.dirname(self.path)

    def load(self, driver=None):
        """ return file contents
        :param driver: function to load/save. if None uses file extension or pkl """
        driver = self._get_driver(driver)
        return driver.load(self)

    def save(self, obj, driver=None):
        """ save obj to file
        :param driver: function to load/save. if None uses file extension or pkl
        """
        path1, ext = fs.path.splitext(self.path)

        # save to temp file so file is not available until complete
        # remove pyfs // at end in case top level folder does not exist
        fs1 = self.fs.rstrip("/")
        temp = Filepath(f"{fs1}{path1}_TEMP123{ext}{self.query}")
        temp.ofs.makedirs(temp.dirname(), recreate=True)
        driver = self._get_driver(driver)
        driver.save(self, obj, temp)

        # release file
        temp.move(self.path)
