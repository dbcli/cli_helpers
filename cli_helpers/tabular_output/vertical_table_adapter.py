# -*- coding: utf-8 -*-
"""Format data into a vertical table layout."""

from __future__ import unicode_literals

from .preprocessors import convert_to_string, override_missing_value

supported_formats = ('vertical', )
preprocessors = (override_missing_value, convert_to_string)


def _get_separator(num, sep_title, sep_character, sep_length):
    """Get a row separator for row *num*."""
    return "{divider}[ {n}. {title} ]{divider}\n".format(
        divider=sep_character * sep_length, n=num + 1, title=sep_title)


def _format_row(headers, row):
    """Format a row."""
    formatted_row = [' | '.join(field) for field in zip(headers, row)]
    return '\n'.join(formatted_row)


def vertical_table(rows, headers, sep_title='row', sep_character='*',
                   sep_length=27):
    """Format *rows* and *headers* as an vertical table.

    The values in *rows* and *headers* must be strings.

    """
    header_len = max([len(x) for x in headers])
    padded_headers = [x.ljust(header_len) for x in headers]
    formatted_rows = [_format_row(padded_headers, row) for row in rows]

    output = []
    for i, result in enumerate(formatted_rows):
        output.append(_get_separator(i, sep_title, sep_character, sep_length))
        output.append(result)
        output.append('\n')

    return ''.join(output)


def adapter(rows, headers, **kwargs):
    """Wrap vertical table in a function for TabularOutputFormatter."""
    keys = ('sep_title', 'sep_character', 'sep_length')
    kwargs = {k: v for k, v in kwargs.items() if k in keys}
    return vertical_table(rows, headers, **kwargs)