# -*- coding: utf-8 -*-
"""Format adapter for the terminaltables module."""

import terminaltables
import itertools

import click
import click.termui

from cli_helpers.utils import filter_dict_by_key
from .preprocessors import (convert_to_string, override_missing_value,
                            style_output)

supported_formats = ('ascii', 'double', 'github')
preprocessors = (override_missing_value, convert_to_string, style_output)

def createClassColor(parent, color):
    class NewTable(parent):
        def __init__(self, *args, **kw):
            parent.__init__(self, *args, **kw)
            for char in [char for char in terminaltables.base_table.BaseTable.__dict__ if char.startswith("CHAR_")]:
                setattr(self, char, click.style(getattr(self,char), fg=color))
    return NewTable

for tablefmt in ('ascii', 'double', 'github'):
    for color in click.termui._ansi_colors:
        supported_formats = supported_formats + ("%s-%s" % (tablefmt,color), )

def adapter(data, headers, table_format=None, **kwargs):
    """Wrap terminaltables inside a function for TabularOutputFormatter."""
    keys = ('title', )

    table_format_handler = {
        'ascii': terminaltables.AsciiTable,
        'double': terminaltables.DoubleTable,
        'github': terminaltables.GithubFlavoredMarkdownTable,
    }

    for tablefmt in table_format_handler.keys():
        for color in click.termui._ansi_colors:
            table_format_handler["%s-%s" % (tablefmt,color)] = createClassColor(table_format_handler[tablefmt], color)

    table = table_format_handler[table_format]

    t = table([headers] + list(data), **filter_dict_by_key(kwargs, keys))

    dimensions = terminaltables.width_and_alignment.max_dimensions(
        t.table_data,
        t.padding_left,
        t.padding_right)[:3]
    for r in t.gen_table(*dimensions):
        yield u''.join(r)
