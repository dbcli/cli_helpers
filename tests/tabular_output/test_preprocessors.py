# -*- coding: utf-8 -*-
"""Test CLI Helpers' tabular output preprocessors."""

from __future__ import unicode_literals
from decimal import Decimal

from cli_helpers.tabular_output.preprocessors import (align_decimals,
                                                      bytes_to_string,
                                                      convert_to_string,
                                                      quote_whitespaces,
                                                      override_missing_value,
                                                      format_numbers)


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


def test_quote_whitespaces_non_spaces():
    """Test the quote_whitespaces() function with non-spaces."""
    data = [["\tbefore", "after \r"], ["\n both  ", "none"]]
    headers = ['h1', 'h2']
    expected = ([["'\tbefore'", "'after \r'"], ["'\n both  '", "'none'"]],
                ['h1', 'h2'])

    assert expected == quote_whitespaces(data, headers)


def test_format_integer():
    """Test formatting for an INTEGER datatype."""
    data = [[1], [1000], [1000000]]
    headers = ['h1']
    result = format_numbers(data,
                            headers,
                            column_types=(int,),
                            decimal_format=',d',
                            float_format=',')

    expected = [['1'], ['1,000'], ['1,000,000']]
    assert expected == result[0]


def test_format_decimal():
    """Test formatting for a DECIMAL(12, 4) datatype."""
    data = [[Decimal('1.0000')], [Decimal('1000.0000')], [Decimal('1000000.0000')]]
    headers = ['h1']
    result = format_numbers(data,
                            headers,
                            column_types=(float,),
                            decimal_format=',d',
                            float_format=',')

    expected = [['1.0000'], ['1,000.0000'], ['1,000,000.0000']]
    assert expected == result[0]


def test_format_float():
    """Test formatting for a REAL datatype."""
    data = [[1.0], [1000.0], [1000000.0]]
    headers = ['h1']
    result = format_numbers(data,
                            headers,
                            column_types=(float,),
                            decimal_format=',d',
                            float_format=',')
    expected = [['1.0'], ['1,000.0'], ['1,000,000.0']]
    assert expected == result[0]
