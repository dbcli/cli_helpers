# -*- coding: utf-8 -*-
"""Test the terminaltables output adapter."""

from __future__ import unicode_literals
from textwrap import dedent

import pytest

from cli_helpers.compat import HAS_PYGMENTS
from cli_helpers.tabular_output import terminaltables_adapter

if HAS_PYGMENTS:
    from pygments.style import Style
    from pygments.token import Token


def test_terminal_tables_adapter():
    """Test the terminaltables output adapter."""
    data = [['abc', 1], ['d', 456]]
    headers = ['letters', 'number']
    output = terminaltables_adapter.adapter(
        iter(data), headers, table_format='ascii')
    assert "\n".join(output) == dedent('''\
        +---------+--------+
        | letters | number |
        +---------+--------+
        | abc     | 1      |
        | d       | 456    |
        +---------+--------+''')


@pytest.mark.skipif(not HAS_PYGMENTS, reason='requires the Pygments library')
def test_style_output_table():
    """Test that *style_output_table()* styles the output table."""

    class CliStyle(Style):
        default_style = ""
        styles = {
            Token.Output.TableSeparator: '#ansired',
        }
    headers = ['h1', 'h2']
    data = [['观音', '2'], ['Ποσειδῶν', 'b']]
    style_output_table = terminaltables_adapter.style_output_table('ascii')

    style_output_table(data, headers, style=CliStyle)
    output = terminaltables_adapter.adapter(iter(data), headers, table_format='ascii')

    assert "\n".join(output) == dedent('''\
        \x1b[31;01m+\x1b[39;00m''' + (
          ('\x1b[31;01m-\x1b[39;00m' * 10) +
          '\x1b[31;01m+\x1b[39;00m' +
          ('\x1b[31;01m-\x1b[39;00m' * 4)) +
        '''\x1b[31;01m+\x1b[39;00m
        \x1b[31;01m|\x1b[39;00m h1       \x1b[31;01m|\x1b[39;00m''' +
        ''' h2 \x1b[31;01m|\x1b[39;00m
        ''' + '\x1b[31;01m+\x1b[39;00m' + (
          ('\x1b[31;01m-\x1b[39;00m' * 10) +
          '\x1b[31;01m+\x1b[39;00m' +
          ('\x1b[31;01m-\x1b[39;00m' * 4)) +
        '''\x1b[31;01m+\x1b[39;00m
        \x1b[31;01m|\x1b[39;00m 观音     \x1b[31;01m|\x1b[39;00m''' +
        ''' 2  \x1b[31;01m|\x1b[39;00m
        \x1b[31;01m|\x1b[39;00m Ποσειδῶν \x1b[31;01m|\x1b[39;00m''' +
        ''' b  \x1b[31;01m|\x1b[39;00m
        ''' + '\x1b[31;01m+\x1b[39;00m' + (
          ('\x1b[31;01m-\x1b[39;00m' * 10) +
          '\x1b[31;01m+\x1b[39;00m' +
          ('\x1b[31;01m-\x1b[39;00m' * 4)) +
        '\x1b[31;01m+\x1b[39;00m')
