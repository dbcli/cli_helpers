# -*- coding: utf-8 -*-
"""Format adapter for the tabulate module."""

from cli_helpers.utils import filter_dict_by_key
from .preprocessors import (convert_to_string, override_missing_value,
                            style_output, HAS_PYGMENTS, Terminal256Formatter, StringIO)

import tabulate

supported_markup_formats = ('mediawiki', 'html', 'latex', 'latex_booktabs',
                            'textile', 'moinmoin', 'jira')
supported_table_formats = ('plain', 'simple', 'grid', 'fancy_grid', 'pipe',
                           'orgtbl', 'psql', 'rst')
supported_formats = supported_markup_formats + supported_table_formats

preprocessors = (override_missing_value, convert_to_string, style_output)


def style_output_table(format_name=""):
    def style_output(data, headers, style=None,
                     separator_table_token='Token.Output.SeparatorTable', **_):
        """Style the *table* a(e.g. bold, italic, and colors)

        .. NOTE::
            This requires the `Pygments <http://pygments.org/>`_ library to
            be installed. You can install it with CLI Helpers as an extra::
                $ pip install cli_helpers[styles]

        Example usage::

            from cli_helpers.tabular_output.preprocessors import style_output
            from pygments.style import Style
            from pygments.token import Token

            class YourStyle(Style):
                default_style = ""
                styles = {
                    Token.Output.SeparatorTable: '#ansigray'
                }

            headers = ('First Name', 'Last Name')
            data = [['Fred', 'Roberts'], ['George', 'Smith']]

            data, headers = style_output(data, headers, style=YourStyle)

        :param iterable data: An :term:`iterable` (e.g. list) of rows.
        :param iterable headers: The column headers.
        :param str/pygments.style.Style style: A Pygments style. You can `create
            your own styles <http://pygments.org/docs/styles/#creating-own-styles>`_.
        :param str separator_table_token: The token type to be used for the separator table.
        :return: data and headers.
        :rtype: tuple

        """
        if style and HAS_PYGMENTS and format_name in supported_table_formats:
            formatter = Terminal256Formatter(style=style)

            def style_field(token, field):
                """Get the styled text for a *field* using *token* type."""
                s = StringIO()
                formatter.format(((token, field),), s)
                return s.getvalue()

            def addColorInElt(elt):
                if not elt:
                    return elt
                if elt.__class__ == tabulate.Line:
                    return tabulate.Line(*(style_field(separator_table_token, val) for val in elt))
                if elt.__class__ == tabulate.DataRow:
                    return tabulate.DataRow(*(style_field(separator_table_token, val) for val in elt))
                return elt

            srcfmt = tabulate._table_formats[format_name]
            newfmt = tabulate.TableFormat(
                *(addColorInElt(val) for val in srcfmt))
            tabulate._table_formats[format_name] = newfmt

        return iter(data), headers
    return style_output

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
