# -*- coding: utf-8 -*-
"""Python compatibility support for CLI Helpers' tests."""

import shutil as _shutil
import tempfile as _tempfile
import warnings as _warnings
import weakref as _weakref

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

    def __init__(self, suffix=None, prefix=None, dir=None):
        self.name = _tempfile.mkdtemp(suffix, prefix, dir)
        self._finalizer = _weakref.finalize(
            self, self._cleanup, self.name,
            warn_message="Implicitly cleaning up {!r}".format(self))

    @classmethod
    def _cleanup(cls, name, warn_message):
        _shutil.rmtree(name)
        _warnings.warn(warn_message, ResourceWarning)

    def __repr__(self):
        return "<{} {!r}>".format(self.__class__.__name__, self.name)

    def __enter__(self):
        return self.name

    def __exit__(self, exc, value, tb):
        self.cleanup()

    def cleanup(self):
        if self._finalizer.detach():
            _shutil.rmtree(self.name)


TemporaryDirectory = _TempDirectory if PY2 else _tempfile.TemporaryDirectory
