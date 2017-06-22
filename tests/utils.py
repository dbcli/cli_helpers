# -*- coding: utf-8 -*-
"""Utility functions for CLI Helpers' tests."""

from __future__ import unicode_literals
from functools import wraps
import re

from .compat import TemporaryDirectory

_ansi_re = re.compile('\033\[((?:\d|;)*)([a-zA-Z])')


def strip_ansi(value):
    """Strip the ANSI escape sequences from a string."""
    return _ansi_re.sub('', value)


def with_temp_dir(f):
    """A wrapper that creates and deletes a temporary directory."""
    @wraps(f)
    def wrapped(*args, **kwargs):
        with TemporaryDirectory() as temp_dir:
            return f(*args, temp_dir=temp_dir, **kwargs)
    return wrapped
