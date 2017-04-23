# -*- coding: utf-8 -*-
"""A delimited data output adapter (e.g. CSV, TSV)."""

import contextlib
import csv

from cli_helpers.compat import StringIO
from .preprocessors import bytes_to_string, override_missing_value

supported_formats = ('csv', 'tsv')
preprocessors = (override_missing_value, bytes_to_string)


def adapter(data, headers, table_format='csv', **_):
    """Wrap the formatting inside a function for TabularOutputFormatter."""
    with contextlib.closing(StringIO()) as content:
        if table_format == 'csv':
            writer = csv.writer(content, delimiter=',')
        elif table_format == 'tsv':
            writer = csv.writer(content, delimiter='\t')
        else:
            raise ValueError('Invalid table_form specified.')

        writer.writerow(headers)
        for row in data:
            writer.writerow(row)

        return content.getvalue()
