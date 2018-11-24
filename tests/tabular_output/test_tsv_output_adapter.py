# -*- coding: utf-8 -*-
"""Test the tsv delimited output adapter."""

from __future__ import unicode_literals
from textwrap import dedent

import pytest

from cli_helpers.tabular_output import tsv_output_adapter


def test_tsv_wrapper():
    """Test the tsv output adapter."""
    # Test tab-delimited output.
    data = [['ab\r\nc', '1'], ['d', '456']]
    headers = ['letters', 'number']
    output = tsv_output_adapter.adapter(
        iter(data), headers, table_format='tsv')
    assert "\n".join(output) == dedent('''\
        letters\tnumber\n\
        ab\r\\nc\t1\n\
        d\t456''')


def test_unicode_with_tsv():
    """Test that the tsv wrapper can handle non-ascii characters."""
    data = [['观音', '1'], ['Ποσειδῶν', '456']]
    headers = ['letters', 'number']
    output = tsv_output_adapter.adapter(data, headers)
    assert "\n".join(output) == dedent('''\
        letters\tnumber\n\
        观音\t1\n\
        Ποσειδῶν\t456''')
