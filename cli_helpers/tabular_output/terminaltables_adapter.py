# -*- coding: utf-8 -*-
"""Format adapter for the terminaltables module."""

import terminaltables
import itertools

from cli_helpers.utils import filter_dict_by_key
from .preprocessors import (convert_to_string, override_missing_value,
                            style_output, HAS_PYGMENTS, Terminal256Formatter, StringIO)

supported_formats = ('ascii', 'double', 'github')
preprocessors = (override_missing_value, convert_to_string, style_output)

table_format_handler = {
    'ascii': terminaltables.AsciiTable,
    'double': terminaltables.DoubleTable,
    'github': terminaltables.GithubFlavoredMarkdownTable,
}


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
                    oken.Output.SeparatorTable: '#ansigray'
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
        if style and HAS_PYGMENTS and format_name in supported_formats:
            formatter = Terminal256Formatter(style=style)

            def style_field(token, field):
                """Get the styled text for a *field* using *token* type."""
                s = StringIO()
                formatter.format(((token, field),), s)
                return s.getvalue()

            clss = table_format_handler[format_name]
            for char in [char for char in terminaltables.base_table.BaseTable.__dict__ if char.startswith("CHAR_")]:
                setattr(clss, char, style_field(
                    separator_table_token, getattr(clss, char)))

        return iter(data), headers
    return style_output


def adapter(data, headers, table_format=None, **kwargs):
    """Wrap terminaltables inside a function for TabularOutputFormatter."""
    keys = ('title', )

    table = table_format_handler[table_format]

    t = table([headers] + list(data), **filter_dict_by_key(kwargs, keys))

    dimensions = terminaltables.width_and_alignment.max_dimensions(
        t.table_data,
        t.padding_left,
        t.padding_right)[:3]
    for r in t.gen_table(*dimensions):
        yield u''.join(r)
