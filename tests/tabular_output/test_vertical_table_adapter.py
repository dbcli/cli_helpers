# -*- coding: utf-8 -*-
"""Test the vertical table formatter."""

from textwrap import dedent

from cli_helpers.compat import text_type
from cli_helpers.tabular_output.vertical_table_adapter import vertical_table


def test_vertical_table():
    """Test the default settings for vertical_table()."""
    results = [('hello', text_type(123)), ('world', text_type(456))]

    expected = dedent("""\
        ***************************[ 1. row ]***************************
        name | hello
        age  | 123
        ***************************[ 2. row ]***************************
        name | world
        age  | 456
        """)
    assert expected == vertical_table(results, ('name', 'age'))


def test_vertical_table_customized():
    """Test customized settings for vertical_table()."""
    results = [('john', text_type(47)), ('jill', text_type(50))]

    expected = dedent("""\
        -----[ 1. person ]-----
        name | john
        age  | 47
        -----[ 2. person ]-----
        name | jill
        age  | 50
        """)
    assert expected == vertical_table(results, ('name', 'age'),
                                      sep_title='person', sep_character='-',
                                      sep_length=5)
