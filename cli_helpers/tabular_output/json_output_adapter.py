# -*- coding: utf-8 -*-
"""A JSON data output adapter"""

from decimal import Decimal
from itertools import chain
import json

from .preprocessors import bytes_to_string

supported_formats = ("json", "jsonl", "jsonl_escaped")
preprocessors = (bytes_to_string,)


class CustomEncoder(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, Decimal):
            return float(o)
        else:
            return super(CustomEncoder, self).default(o)


def adapter(data, headers, table_format="jsonl", **_kwargs):
    """Wrap the formatting inside a function for TabularOutputFormatter."""
    if table_format in ("json", "jsonl"):
        ensure_ascii = False
    elif table_format == "jsonl_escaped":
        ensure_ascii = True
    else:
        raise ValueError("Invalid table_format specified.")

    records = (dict(zip(headers, row, strict=True)) for row in chain(data))
    if table_format == "json":
        records = (list(records),)

    for record in records:
        yield json.dumps(
            record,
            cls=CustomEncoder,
            separators=(",", ":"),
            ensure_ascii=ensure_ascii,
        )
