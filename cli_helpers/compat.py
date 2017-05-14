# -*- coding: utf-8 -*-
"""OS and Python compatibility support."""

import sys

PY2 = sys.version_info[0] == 2
WIN = sys.platform.startswith('win')


if PY2:
    text_type = unicode
    binary_type = str

    from cStringIO import StringIO
    from UserDict import UserDict
else:
    text_type = str
    binary_type = bytes

    from collections import UserDict
    from io import StringIO
