# -*- coding: utf-8 -*-
"""Test the sql output adapter."""

from __future__ import unicode_literals
from textwrap import dedent

from cli_helpers.tabular_output import sql_adapter


def test_sql_adapter():
    """Test the sql output adapter."""
    data = [['abc', '1'], ['d', '456']]
    headers = ['letters', 'number']
    output = sql_adapter.adapter(
        iter(data), headers, table_format='sql-insert')
    assert "\n".join(output) == dedent('''\
            insert into table (`letters`, `number`) values
              ('abc', '1')
            , ('d', '456')
            ;''')
    output = sql_adapter.adapter(
        iter(data), headers, table_format='sql-update')
    assert "\n".join(output) == dedent('''\
            update table set
              `letters` = '1'
            where `number` = 'abc';
            update table set
              `letters` = '456'
            where `number` = 'd';''')
