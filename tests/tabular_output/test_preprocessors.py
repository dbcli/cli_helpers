# -*- coding: utf-8 -*-
"""Test CLI Helpers' tabular output preprocessors."""

from __future__ import unicode_literals
from decimal import Decimal

from cli_helpers.tabular_output.preprocessors import (align_decimals,
                                                      bytes_to_string,
                                                      convert_to_string,
                                                      quote_whitespaces,
                                                      override_missing_value)


def test_convert_to_string():
    """Test the convert_to_string() function."""
    data = [[1, 'John'], [2, 'Jill']]
    headers = [0, 'name']
    expected = ([['1', 'John'], ['2', 'Jill']], ['0', 'name'])

    assert expected == convert_to_string(data, headers)


def test_override_missing_values():
    """Test the override_missing_values() function."""
    data = [[1, None], [2, 'Jill']]
    headers = [0, 'name']
    expected = ([[1, '<EMPTY>'], [2, 'Jill']], [0, 'name'])

    assert expected == override_missing_value(data, headers,
                                              missing_value='<EMPTY>')


def test_bytes_to_string():
    """Test the bytes_to_string() function."""
    data = [[1, 'John'], [2, b'Jill']]
    headers = [0, 'name']
    expected = ([[1, 'John'], [2, 'Jill']], [0, 'name'])

    assert expected == bytes_to_string(data, headers)


def test_align_decimals():
    """Test the align_decimals() function."""
    data = [[Decimal('200'), Decimal('1')], [
        Decimal('1.00002'), Decimal('1.0')]]
    headers = ['num1', 'num2']
    expected = ([['200', '1'], ['  1.00002', '1.0']], ['num1', 'num2'])

    assert expected == align_decimals(data, headers)


def test_align_decimals_empty_result():
    """Test align_decimals() with no results."""
    data = []
    headers = ['num1', 'num2']
    expected = ([], ['num1', 'num2'])

    assert expected == align_decimals(data, headers)


def test_quote_whitespaces():
    """Test the quote_whitespaces() function."""
    data = [["  before", "after  "], ["  both  ", "none"]]
    headers = ['h1', 'h2']
    expected = ([["'  before'", "'after  '"], ["'  both  '", "'none'"]],
                ['h1', 'h2'])

    assert expected == quote_whitespaces(data, headers)


def test_quote_whitespaces_empty_result():
    """Test the quote_whitespaces() function with no results."""
    data = []
    headers = ['h1', 'h2']
    expected = ([], ['h1', 'h2'])

    assert expected == quote_whitespaces(data, headers)
