# -*- coding: utf-8 -*-
"""Test the vertical table formatter."""

from textwrap import dedent

from cli_helpers.compat import text_type
from cli_helpers.tabular_output import vertical_table_adapter


def test_vertical_table():
    """Test the default settings for vertical_table()."""
    results = [('hello', text_type(123)), ('world', text_type(456))]

    expected = dedent("""\
        ***************************[ 1. row ]***************************
        name | hello
        age  | 123
        ***************************[ 2. row ]***************************
        name | world
        age  | 456""")
    assert expected == "\n".join(
        vertical_table_adapter.adapter(results, ('name', 'age')))


def test_vertical_table_customized():
    """Test customized settings for vertical_table()."""
    results = [('john', text_type(47)), ('jill', text_type(50))]

    expected = dedent("""\
        -[ PERSON 1 ]-----
        name | john
        age  | 47
        -[ PERSON 2 ]-----
        name | jill
        age  | 50""")
    assert expected == "\n".join(vertical_table_adapter.adapter(
        results, ('name', 'age'), sep_title='PERSON {n}',
        sep_character='-', sep_length=(1, 5)))
