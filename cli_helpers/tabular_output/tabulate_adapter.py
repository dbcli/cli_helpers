# -*- coding: utf-8 -*-
"""Format adapter for the tabulate module."""

from cli_helpers.utils import filter_dict_by_key
from .preprocessors import (convert_to_string, override_missing_value,
                            style_output)

import tabulate

import click
import click.termui

supported_markup_formats = ('mediawiki', 'html', 'latex', 'latex_booktabs',
                            'textile', 'moinmoin', 'jira')
supported_table_formats = ('plain', 'simple', 'grid', 'fancy_grid', 'pipe',
                           'orgtbl', 'psql', 'rst')
supported_formats = supported_markup_formats + supported_table_formats

preprocessors = (override_missing_value, convert_to_string, style_output)

def addColorInElt(elt, col):
    if not elt:
        return elt
    if elt.__class__ == tabulate.Line:
        return tabulate.Line(*(click.style(val,fg=col) for val in elt))
    if elt.__class__ == tabulate.DataRow:
        return tabulate.DataRow(*(click.style(val,fg=col) for val in elt))
    return elt

for tablefmt in supported_table_formats:
    for color in click.termui._ansi_colors:
        newfmt_name = "%s-%s" % (tablefmt,color)
        srcfmt = tabulate._table_formats[tablefmt]
        newfmt = tabulate.TableFormat(*( addColorInElt(val, color) for val in srcfmt))
        supported_formats = supported_formats + (newfmt_name, )
        tabulate._table_formats[newfmt_name] = newfmt

def adapter(data, headers, table_format=None, preserve_whitespace=False,
            **kwargs):
    """Wrap tabulate inside a function for TabularOutputFormatter."""
    keys = ('floatfmt', 'numalign', 'stralign', 'showindex', 'disable_numparse')
    tkwargs = {'tablefmt': table_format}
    tkwargs.update(filter_dict_by_key(kwargs, keys))

    if table_format in supported_markup_formats:
        tkwargs.update(numalign=None, stralign=None)

    tabulate.PRESERVE_WHITESPACE = preserve_whitespace

    return iter(tabulate.tabulate(data, headers, **tkwargs).split('\n'))
