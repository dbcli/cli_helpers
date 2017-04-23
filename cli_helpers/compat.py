# -*- coding: utf-8 -*-
"""Python 2/3 compatibility support."""

import sys

PY2 = sys.version_info[0] == 2


if PY2:
    text_type = unicode
    binary_type = str

    from cStringIO import StringIO
else:
    text_type = str
    binary_type = bytes

    from io import StringIO
