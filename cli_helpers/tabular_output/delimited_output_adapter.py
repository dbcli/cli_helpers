# -*- coding: utf-8 -*-
"""A delimited data output adapter (e.g. CSV, TSV)."""

from __future__ import unicode_literals
import contextlib
from io import StringIO

from cli_helpers.compat import csv
from cli_helpers.utils import filter_dict_by_key
from .preprocessors import bytes_to_string, override_missing_value

supported_formats = ('csv', 'tsv')
preprocessors = (override_missing_value, bytes_to_string)


def adapter(data, headers, table_format='csv', **kwargs):
    """Wrap the formatting inside a function for TabularOutputFormatter."""
    keys = ('dialect', 'delimiter', 'doublequote', 'escapechar',
            'lineterminator', 'quotechar', 'quoting', 'skipinitialspace',
            'strict')
    if table_format == 'csv':
        delimiter = ','
    elif table_format == 'tsv':
        delimiter = '\t'
    else:
        raise ValueError('Invalid table_format specified.')

    ckwargs = {'delimiter': delimiter}
    ckwargs.update(filter_dict_by_key(kwargs, keys))

    with contextlib.closing(StringIO()) as content:
        writer = csv.writer(content, **ckwargs)
        writer.writerow(headers)
        for row in data:
            writer.writerow(row)

        return content.getvalue()
