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

    from cStringIO import StringIO
else:
    text_type = str
    binary_type = bytes
    long_type = int
    int_types = (int,)

    from io import StringIO


float_types = (float, Decimal)
