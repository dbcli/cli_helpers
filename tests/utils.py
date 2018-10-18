# -*- coding: utf-8 -*-
"""Utility functions for CLI Helpers' tests."""

from __future__ import unicode_literals
from functools import wraps

from .compat import TemporaryDirectory


def with_temp_dir(f):
    """A wrapper that creates and deletes a temporary directory."""
    @wraps(f)
    def wrapped(*args, **kwargs):
        with TemporaryDirectory() as temp_dir:
            return f(*args, temp_dir=temp_dir, **kwargs)
    return wrapped
