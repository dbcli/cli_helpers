# -*- coding: utf-8 -*-
"""Test the delimited output adapter."""

from __future__ import unicode_literals
from textwrap import dedent

import pytest

from cli_helpers.tabular_output import delimited_output_adapter


def test_csv_wrapper():
    """Test the delimited output adapter."""
    # Test comma-delimited output.
    data = [['abc', '1'], ['d', '456']]
    headers = ['letters', 'number']
    output = delimited_output_adapter.adapter(data, headers)
    assert output == dedent('''\
        letters,number\r\n\
        abc,1\r\n\
        d,456\r\n''')

    # Test tab-delimited output.
    data = [['abc', '1'], ['d', '456']]
    headers = ['letters', 'number']
    output = delimited_output_adapter.adapter(
        data, headers, table_format='tsv')
    assert output == dedent('''\
        letters\tnumber\r\n\
        abc\t1\r\n\
        d\t456\r\n''')

    with pytest.raises(ValueError):
        output = delimited_output_adapter.adapter(
            data, headers, table_format='foobar')


def test_unicode_with_csv():
    """Test that the csv wrapper can handle non-ascii characters."""
    data = [['观音', '1'], ['Ποσειδῶν', '456']]
    headers = ['letters', 'number']
    output = delimited_output_adapter.adapter(data, headers)
    assert output == dedent('''\
        letters,number\r\n\
        观音,1\r\n\
        Ποσειδῶν,456\r\n''')

