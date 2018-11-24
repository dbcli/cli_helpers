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
    output = delimited_output_adapter.adapter(iter(data), headers, dialect='unix')
    assert "\n".join(output) == dedent('''\
        "letters","number"\n\
        "abc","1"\n\
        "d","456"''')

    # Test tab-delimited output.
    data = [['abc', '1'], ['d', '456']]
    headers = ['letters', 'number']
    output = delimited_output_adapter.adapter(
        iter(data), headers, table_format='csv-tab', dialect='unix')
    assert "\n".join(output) == dedent('''\
        "letters"\t"number"\n\
        "abc"\t"1"\n\
        "d"\t"456"''')

    with pytest.raises(ValueError):
        output = delimited_output_adapter.adapter(
            iter(data), headers, table_format='foobar')
        list(output)


def test_unicode_with_csv():
    """Test that the csv wrapper can handle non-ascii characters."""
    data = [['观音', '1'], ['Ποσειδῶν', '456']]
    headers = ['letters', 'number']
    output = delimited_output_adapter.adapter(data, headers)
    assert "\n".join(output) == dedent('''\
        letters,number\n\
        观音,1\n\
        Ποσειδῶν,456''')

