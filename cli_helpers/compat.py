# -*- coding: utf-8 -*-
"""OS and Python compatibility support."""

import sys

PY2 = sys.version_info[0] == 2
WIN = sys.platform.startswith('win')
MAC = sys.platform == 'darwin'


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


HAS_PYGMENTS = True
try:
    from pygments.formatters.terminal256 import Terminal256Formatter
except ImportError:
    HAS_PYGMENTS = False
    Terminal256Formatter = None
