# -*- coding: utf-8 -*-
"""Format adapter for the terminaltables module."""

import terminaltables

from cli_helpers.utils import filter_dict_by_key
from .preprocessors import (convert_to_string, override_missing_value,
                            style_output)

supported_formats = ('ascii', 'double', 'github')
preprocessors = (override_missing_value, convert_to_string, style_output)


def adapter(data, headers, table_format=None, **kwargs):
    """Wrap terminaltables inside a function for TabularOutputFormatter."""
    keys = ('title', )

    table_format_handler = {
        'ascii': terminaltables.AsciiTable,
        'double': terminaltables.DoubleTable,
        'github': terminaltables.GithubFlavoredMarkdownTable,
    }

    table = table_format_handler[table_format]

    t = table([headers] + data, **filter_dict_by_key(kwargs, keys))
    return t.table
