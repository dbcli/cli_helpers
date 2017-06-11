# -*- coding: utf-8 -*-
"""Utility functions for CLI Helpers' tests."""

import re

_ansi_re = re.compile('\033\[((?:\d|;)*)([a-zA-Z])')


def strip_ansi(value):
    """Strip the ANSI escape sequences from a string."""
    return _ansi_re.sub('', value)
