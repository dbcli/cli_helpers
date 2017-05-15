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


def test_additional_preprocessors():
    """Test that additional preprocessors are run."""
    def hello_world(data, headers, **_):
        for row in data:
            for i, value in enumerate(row):
                if value == 'hello':
                    row[i] = "{}, world".format(value)
        return data, headers

    data = [['foo', None], ['hello!', 'hello']]
    headers = 'ab'

    expected = dedent('''\
        +--------+--------------+
        | a      | b            |
        +--------+--------------+
        | foo    | hello        |
        | hello! | hello, world |
        +--------+--------------+''')

    assert expected == TabularOutputFormatter().format_output(
        data, headers, format_name='ascii', preprocessors=(hello_world,),
        missing_value='hello')
