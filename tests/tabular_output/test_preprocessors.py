# -*- coding: utf-8 -*-
"""Test CLI Helpers' tabular output preprocessors."""

from __future__ import unicode_literals
from decimal import Decimal

import pytest

from cli_helpers.compat import HAS_PYGMENTS
from cli_helpers.tabular_output.preprocessors import (
    align_decimals, bytes_to_string, convert_to_string, quote_whitespaces,
    override_missing_value, style_output, format_numbers)

if HAS_PYGMENTS:
    from pygments.style import Style
    from pygments.token import Token


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
    column_types = (float, float)
    expected = ([['200', '1'], ['  1.00002', '1.0']], ['num1', 'num2'])

    assert expected == align_decimals(data, headers, column_types=column_types)


def test_align_decimals_empty_result():
    """Test align_decimals() with no results."""
    data = []
    headers = ['num1', 'num2']
    column_types = ()
    expected = ([], ['num1', 'num2'])

    assert expected == align_decimals(data, headers, column_types=column_types)


def test_align_decimals_non_decimals():
    """Test align_decimals() with non-decimals."""
    data = [[Decimal('200.000'), Decimal('1.000')], [None, None]]
    headers = ['num1', 'num2']
    column_types = (float, float)
    expected = ([['200.000', '1.000'], [None, None]], ['num1', 'num2'])

    assert expected == align_decimals(data, headers, column_types=column_types)


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


@pytest.mark.skipif(not HAS_PYGMENTS, reason='requires the Pygments library')
def test_style_output_no_styles():
    """Test that *style_output()* does not style without styles."""
    headers = ['h1', 'h2']
    data = [['1', '2'], ['a', 'b']]

    assert (data, headers) == style_output(data, headers)


@pytest.mark.skipif(HAS_PYGMENTS,
                    reason='requires the Pygments library be missing')
def test_style_output_no_pygments():
    """Test that *style_output()* does not try to style without Pygments."""
    headers = ['h1', 'h2']
    data = [['1', '2'], ['a', 'b']]

    assert (data, headers) == style_output(data, headers)


@pytest.mark.skipif(not HAS_PYGMENTS, reason='requires the Pygments library')
def test_style_output():
    """Test that *style_output()* styles output."""

    class CliStyle(Style):
        default_style = ""
        styles = {
            Token.Output.Header: 'bold #ansired',
            Token.Output.OddRow: 'bg:#eee #111',
            Token.Output.EvenRow: '#0f0'
        }
    headers = ['h1', 'h2']
    data = [['观音', '2'], ['Ποσειδῶν', 'b']]

    expected_headers = ['\x1b[31;01mh1\x1b[39;00m', '\x1b[31;01mh2\x1b[39;00m']
    expected_data = [['\x1b[38;5;233;48;5;7m观音\x1b[39;49m',
                      '\x1b[38;5;233;48;5;7m2\x1b[39;49m'],
                     ['\x1b[38;5;10mΠοσειδῶν\x1b[39m', '\x1b[38;5;10mb\x1b[39m']]

    assert (expected_data, expected_headers) == style_output(data, headers,
                                                             style=CliStyle)


@pytest.mark.skipif(not HAS_PYGMENTS, reason='requires the Pygments library')
def test_style_output_custom_tokens():
    """Test that *style_output()* styles output with custom token names."""

    class CliStyle(Style):
        default_style = ""
        styles = {
            Token.Results.Headers: 'bold #ansired',
            Token.Results.OddRows: 'bg:#eee #111',
            Token.Results.EvenRows: '#0f0'
        }
    headers = ['h1', 'h2']
    data = [['1', '2'], ['a', 'b']]

    expected_headers = ['\x1b[31;01mh1\x1b[39;00m', '\x1b[31;01mh2\x1b[39;00m']
    expected_data = [['\x1b[38;5;233;48;5;7m1\x1b[39;49m',
                      '\x1b[38;5;233;48;5;7m2\x1b[39;49m'],
                     ['\x1b[38;5;10ma\x1b[39m', '\x1b[38;5;10mb\x1b[39m']]

    output = style_output(
        data, headers, style=CliStyle,
        header_token='Token.Results.Headers',
        odd_row_token='Token.Results.OddRows',
        even_row_token='Token.Results.EvenRows')

    assert (expected_data, expected_headers) == output


def test_format_integer():
    """Test formatting for an INTEGER datatype."""
    data = [[1], [1000], [1000000]]
    headers = ['h1']
    result = format_numbers(data,
                            headers,
                            column_types=(int,),
                            integer_format=',',
                            float_format=',')

    expected = [['1'], ['1,000'], ['1,000,000']]
    assert expected, headers == result


def test_format_decimal():
    """Test formatting for a DECIMAL(12, 4) datatype."""
    data = [[Decimal('1.0000')], [Decimal('1000.0000')], [Decimal('1000000.0000')]]
    headers = ['h1']
    result = format_numbers(data,
                            headers,
                            column_types=(float,),
                            integer_format=',',
                            float_format=',')

    expected = [['1.0000'], ['1,000.0000'], ['1,000,000.0000']]
    assert expected, headers == result


def test_format_float():
    """Test formatting for a REAL datatype."""
    data = [[1.0], [1000.0], [1000000.0]]
    headers = ['h1']
    result = format_numbers(data,
                            headers,
                            column_types=(float,),
                            integer_format=',',
                            float_format=',')
    expected = [['1.0'], ['1,000.0'], ['1,000,000.0']]
    assert expected, headers == result


def test_format_integer_only():
    """Test that providing one format string works."""
    data = [[1, 1.0], [1000, 1000.0], [1000000, 1000000.0]]
    headers = ['h1', 'h2']
    result = format_numbers(data, headers, column_types=(int, float),
                            integer_format=',')

    expected = [['1', 1.0], ['1,000', 1000.0], ['1,000,000', 1000000.0]]
    assert expected, headers == result


def test_format_numbers_no_format_strings():
    """Test that numbers aren't formatted without format strings."""
    data = ((1), (1000), (1000000))
    headers = ('h1',)
    result = format_numbers(data, headers, column_types=(int,))
    assert data, headers == result


def test_format_numbers_no_column_types():
    """Test that numbers aren't formatted without column types."""
    data = ((1), (1000), (1000000))
    headers = ('h1',)
    result = format_numbers(data, headers, integer_format=',',
                            float_format=',')
    assert data, headers == result
