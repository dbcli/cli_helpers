# -*- coding: utf-8 -*-
"""Python 2/3 compatibility support."""

from decimal import Decimal
import sys

PY2 = sys.version_info[0] == 2


if PY2:
    text_type = unicode
    binary_type = str
    long_type = long
    int_types = (int, long)

    from backports import csv

    from StringIO import StringIO
    from itertools import izip_longest as zip_longest
else:
    text_type = str
    binary_type = bytes
    long_type = int
    int_types = (int,)

    import csv
    from io import StringIO
    from itertools import zip_longest


HAS_PYGMENTS = True
try:
    from pygments.formatters.terminal256 import Terminal256Formatter
except ImportError:
    HAS_PYGMENTS = False
    Terminal256Formatter = None

float_types = (float, Decimal)
