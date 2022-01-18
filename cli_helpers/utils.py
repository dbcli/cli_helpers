# -*- coding: utf-8 -*-
"""Various utility functions and helpers."""

import binascii
import re
from functools import lru_cache
from typing import Dict

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from pygments.style import StyleMeta

from cli_helpers.compat import binary_type, text_type, Terminal256Formatter, StringIO


def bytes_to_string(b):
    """Convert bytes *b* to a string.

    Hexlify bytes that can't be decoded.

    """
    if isinstance(b, binary_type):
        needs_hex = False
        try:
            result = b.decode("utf8")
            needs_hex = not result.isprintable()
        except UnicodeDecodeError:
            needs_hex = True
        if needs_hex:
            return "0x" + binascii.hexlify(b).decode("ascii")
        else:
            return result
    return b


def to_string(value):
    """Convert *value* to a string."""
    if isinstance(value, binary_type):
        return bytes_to_string(value)
    else:
        return text_type(value)


def truncate_string(value, max_width=None, skip_multiline_string=True):
    """Truncate string values."""
    if skip_multiline_string and isinstance(value, text_type) and "\n" in value:
        return value
    elif (
        isinstance(value, text_type)
        and max_width is not None
        and len(value) > max_width
    ):
        return value[: max_width - 3] + "..."
    return value


def intlen(n):
    """Find the length of the integer part of a number *n*."""
    pos = n.find(".")
    return len(n) if pos < 0 else pos


def filter_dict_by_key(d, keys):
    """Filter the dict *d* to remove keys not in *keys*."""
    return {k: v for k, v in d.items() if k in keys}


def unique_items(seq):
    """Return the unique items from iterable *seq* (in order)."""
    seen = set()
    return [x for x in seq if not (x in seen or seen.add(x))]


_ansi_re = re.compile("\033\\[((?:\\d|;)*)([a-zA-Z])")


def strip_ansi(value):
    """Strip the ANSI escape sequences from a string."""
    return _ansi_re.sub("", value)


def replace(s, replace):
    """Replace multiple values in a string"""
    for r in replace:
        s = s.replace(*r)
    return s


@lru_cache()
def _get_formatter(style) -> Terminal256Formatter:
    return Terminal256Formatter(style=style)


def style_field(token, field, style):
    """Get the styled text for a *field* using *token* type."""
    formatter = _get_formatter(style)
    s = StringIO()
    formatter.format(((token, field),), s)
    return s.getvalue()


def filter_style_table(style: "StyleMeta", *relevant_styles: str) -> Dict:
    """
    get a dictionary of styles for given tokens. Typical usage:

    filter_style_table(style, Token.Output.EvenRow, Token.Output.OddRow) == {
        Token.Output.EvenRow: "",
        Token.Output.OddRow: "",
    }
    """
    _styles_iter = ((key, val) for key, val in getattr(style, "styles", {}).items())
    _relevant_styles_iter = filter(lambda tpl: tpl[0] in relevant_styles, _styles_iter)
    return {key: val for key, val in _relevant_styles_iter}
