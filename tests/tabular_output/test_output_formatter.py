# -*- coding: utf-8 -*-
"""Test the generic output formatter interface."""

from __future__ import unicode_literals
from decimal import Decimal
from textwrap import dedent

from cli_helpers.tabular_output import TabularOutputFormatter


def test_tabular_output_formatter():
    """Test the TabularOutputFormatter class."""
    data = [['abc', Decimal(1)], ['defg', Decimal('11.1')],
            ['hi', Decimal('1.1')]]
    headers = ['text', 'numeric']
    expected = dedent('''\
        +------+---------+
        | text | numeric |
        +------+---------+
        | abc  |  1      |
        | defg | 11.1    |
        | hi   |  1.1    |
        +------+---------+''')

    assert expected == TabularOutputFormatter().format_output(
        data, headers, format_name='ascii')
