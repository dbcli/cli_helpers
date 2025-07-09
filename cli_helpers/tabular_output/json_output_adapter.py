# -*- coding: utf-8 -*-
"""A JSON data output adapter"""

from itertools import chain
import json

from .preprocessors import bytes_to_string, override_missing_value, convert_to_string

supported_formats = ("jsonl", "jsonl_escaped")
preprocessors = (override_missing_value, bytes_to_string, convert_to_string)


def adapter(data, headers, table_format="jsonl", **_kwargs):
    """Wrap the formatting inside a function for TabularOutputFormatter."""
    if table_format == "jsonl":
        ensure_ascii = False
    elif table_format == "jsonl_escaped":
        ensure_ascii = True
    else:
        raise ValueError("Invalid table_format specified.")

    for row in chain(data):
        yield json.dumps(
            dict(zip(headers, row, strict=True)),
            separators=(",", ":"),
            ensure_ascii=ensure_ascii,
        )
