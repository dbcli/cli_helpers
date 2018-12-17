# -*- coding: utf-8 -*-
"""Various utility functions and helpers."""

import binascii
import re

from cli_helpers.compat import binary_type, text_type


def bytes_to_string(b):
    """Convert bytes *b* to a string.

    Hexlify bytes that can't be decoded.

    """
    if isinstance(b, binary_type):
        try:
            return b.decode('utf8')
        except UnicodeDecodeError:
            return '0x' + binascii.hexlify(b).decode('ascii')
    return b


def to_string(value):
    """Convert *value* to a string."""
    if isinstance(value, binary_type):
        return bytes_to_string(value)
    else:
        return text_type(value)


def truncate_string(value, max_width=None):
    """Truncate string values."""
    if isinstance(value, text_type) and max_width is not None and len(value) > max_width:
        return value[:max_width]
    return value


def intlen(n):
    """Find the length of the integer part of a number *n*."""
    pos = n.find('.')
    return len(n) if pos < 0 else pos


def filter_dict_by_key(d, keys):
    """Filter the dict *d* to remove keys not in *keys*."""
    return {k: v for k, v in d.items() if k in keys}


def unique_items(seq):
    """Return the unique items from iterable *seq* (in order)."""
    seen = set()
    return [x for x in seq if not (x in seen or seen.add(x))]


_ansi_re = re.compile('\033\[((?:\d|;)*)([a-zA-Z])')


def strip_ansi(value):
    """Strip the ANSI escape sequences from a string."""
    return _ansi_re.sub('', value)


def replace(s, replace):
    """Replace multiple values in a string"""
    for r in replace:
        s = s.replace(*r)
    return s
