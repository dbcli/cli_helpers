# -*- coding: utf-8 -*-
"""A tsv data output adapter"""

from __future__ import unicode_literals

from .preprocessors import bytes_to_string, override_missing_value, convert_to_string
from itertools import chain
from cli_helpers.utils import replace

supported_formats = ("tsv",)
preprocessors = (override_missing_value, bytes_to_string, convert_to_string)


def adapter(data, headers, **kwargs):
    """Wrap the formatting inside a function for TabularOutputFormatter."""
    for row in chain((headers,), data):
        yield "\t".join((replace(r, (("\n", r"\n"), ("\t", r"\t"))) for r in row))
