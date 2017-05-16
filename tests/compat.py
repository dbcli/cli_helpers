# -*- coding: utf-8 -*-
"""Python compatibility support for CLI Helpers' tests."""

from __future__ import unicode_literals
import os as _os
import shutil as _shutil
import tempfile as _tempfile
import warnings as _warnings

from cli_helpers.compat import PY2


class _TempDirectory(object):
    """Create and return a temporary directory.  This has the same
    behavior as mkdtemp but can be used as a context manager.  For
    example:

        with TemporaryDirectory() as tmpdir:
            ...

    Upon exiting the context, the directory and everything contained
    in it are removed.

    NOTE: Copied from the Python 3 standard library.
    """

    # Handle mkdtemp raising an exception
    name = None
    _closed = False

    def __init__(self, suffix="", prefix='tmp', dir=None):
        self.name = _tempfile.mkdtemp(suffix, prefix, dir)

    def __repr__(self):
        return "<{} {!r}>".format(self.__class__.__name__, self.name)

    def __enter__(self):
        return self.name

    def cleanup(self, _warn=False, _warnings=_warnings):
        if self.name and not self._closed:
            try:
                _shutil.rmtree(self.name)
            except (TypeError, AttributeError) as ex:
                if "None" not in '%s' % (ex,):
                    raise
                self._rmtree(self.name)
            self._closed = True
            if _warn and _warnings.warn:
                _warnings.warn("Implicitly cleaning up {!r}".format(self),
                               ResourceWarning)

    def __exit__(self, exc, value, tb):
        self.cleanup()

    def __del__(self):
        # Issue a ResourceWarning if implicit cleanup needed
        self.cleanup(_warn=True)

    def _rmtree(self, path, _OSError=OSError, _sep=_os.path.sep,
                _listdir=_os.listdir, _remove=_os.remove, _rmdir=_os.rmdir):
        # Essentially a stripped down version of shutil.rmtree.  We can't
        # use globals because they may be None'ed out at shutdown.
        if not isinstance(path, str):
            _sep = _sep.encode()
        try:
            for name in _listdir(path):
                fullname = path + _sep + name
                try:
                    _remove(fullname)
                except _OSError:
                    self._rmtree(fullname)
            _rmdir(path)
        except _OSError:
            pass


TemporaryDirectory = _TempDirectory if PY2 else _tempfile.TemporaryDirectory
