# -*- coding: utf-8 -*-
"""Test the terminaltables output adapter."""

from __future__ import unicode_literals
from textwrap import dedent

from cli_helpers.tabular_output import terminaltables_adapter


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
