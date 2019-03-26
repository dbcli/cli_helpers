# -*- coding: utf-8 -*-
"""Test CLI Helpers' tabular output preprocessors."""

from __future__ import unicode_literals
from decimal import Decimal

import pytest

from cli_helpers.compat import HAS_PYGMENTS
from cli_helpers.tabular_output.preprocessors import (
    align_decimals, bytes_to_string, convert_to_string, quote_whitespaces,
    override_missing_value, override_tab_value, style_output, format_numbers)

if HAS_PYGMENTS:
    from pygments.style import Style
    from pygments.token import Token

import inspect
import cli_helpers.tabular_output.preprocessors
import types


def test_convert_to_string():
    """Test the convert_to_string() function."""
    data = [[1, 'John'], [2, 'Jill']]
    headers = [0, 'name']
    expected = ([['1', 'John'], ['2', 'Jill']], ['0', 'name'])
    results = convert_to_string(data, headers)

    assert expected == (list(results[0]), results[1])


def test_override_missing_values():
    """Test the override_missing_values() function."""
    data = [[1, None], [2, 'Jill']]
    headers = [0, 'name']
    expected = ([[1, '<EMPTY>'], [2, 'Jill']], [0, 'name'])
    results = override_missing_value(data, headers, missing_value='<EMPTY>')

    assert expected == (list(results[0]), results[1])


def test_override_tab_value():
    """Test the override_tab_value() function."""
    data = [[1, '\tJohn'], [2, 'Jill']]
    headers = ['id', 'name']
    expected = ([[1, '    John'], [2, 'Jill']], ['id', 'name'])
    results = override_tab_value(data, headers)

    assert expected == (list(results[0]), results[1])


def test_bytes_to_string():
    """Test the bytes_to_string() function."""
    data = [[1, 'John'], [2, b'Jill']]
    headers = [0, 'name']
    expected = ([[1, 'John'], [2, 'Jill']], [0, 'name'])
    results = bytes_to_string(data, headers)

    assert expected == (list(results[0]), results[1])


def test_align_decimals():
    """Test the align_decimals() function."""
    data = [[Decimal('200'), Decimal('1')], [
        Decimal('1.00002'), Decimal('1.0')]]
    headers = ['num1', 'num2']
    column_types = (float, float)
    expected = ([['200', '1'], ['  1.00002', '1.0']], ['num1', 'num2'])
    results = align_decimals(data, headers, column_types=column_types)

    assert expected == (list(results[0]), results[1])


def test_align_decimals_empty_result():
    """Test align_decimals() with no results."""
    data = []
    headers = ['num1', 'num2']
    column_types = ()
    expected = ([], ['num1', 'num2'])
    results = align_decimals(data, headers, column_types=column_types)

    assert expected == (list(results[0]), results[1])


def test_align_decimals_non_decimals():
    """Test align_decimals() with non-decimals."""
    data = [[Decimal('200.000'), Decimal('1.000')], [None, None]]
    headers = ['num1', 'num2']
    column_types = (float, float)
    expected = ([['200.000', '1.000'], [None, None]], ['num1', 'num2'])
    results = align_decimals(data, headers, column_types=column_types)

    assert expected == (list(results[0]), results[1])


def test_quote_whitespaces():
    """Test the quote_whitespaces() function."""
    data = [["  before", "after  "], ["  both  ", "none"]]
    headers = ['h1', 'h2']
    expected = ([["'  before'", "'after  '"], ["'  both  '", "'none'"]],
                ['h1', 'h2'])
    results = quote_whitespaces(data, headers)

    assert expected == (list(results[0]), results[1])


def test_quote_whitespaces_empty_result():
    """Test the quote_whitespaces() function with no results."""
    data = []
    headers = ['h1', 'h2']
    expected = ([], ['h1', 'h2'])
    results = quote_whitespaces(data, headers)

    assert expected == (list(results[0]), results[1])


def test_quote_whitespaces_non_spaces():
    """Test the quote_whitespaces() function with non-spaces."""
    data = [["\tbefore", "after \r"], ["\n both  ", "none"]]
    headers = ['h1', 'h2']
    expected = ([["'\tbefore'", "'after \r'"], ["'\n both  '", "'none'"]],
                ['h1', 'h2'])
    results = quote_whitespaces(data, headers)

    assert expected == (list(results[0]), results[1])


@pytest.mark.skipif(not HAS_PYGMENTS, reason='requires the Pygments library')
def test_style_output_no_styles():
    """Test that *style_output()* does not style without styles."""
    headers = ['h1', 'h2']
    data = [['1', '2'], ['a', 'b']]
    results = style_output(data, headers)

    assert (data, headers) == (list(results[0]), results[1])


@pytest.mark.skipif(HAS_PYGMENTS,
                    reason='requires the Pygments library be missing')
def test_style_output_no_pygments():
    """Test that *style_output()* does not try to style without Pygments."""
    headers = ['h1', 'h2']
    data = [['1', '2'], ['a', 'b']]
    results = style_output(data, headers)

    assert (data, headers) == (list(results[0]), results[1])


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
    results = style_output(data, headers, style=CliStyle)

    assert (expected_data, expected_headers) == (list(results[0]), results[1])

@pytest.mark.skipif(not HAS_PYGMENTS, reason='requires the Pygments library')
def test_style_output_with_newlines():
    """Test that *style_output()* styles output with newlines in it."""

    class CliStyle(Style):
        default_style = ""
        styles = {
            Token.Output.Header: 'bold #ansired',
            Token.Output.OddRow: 'bg:#eee #111',
            Token.Output.EvenRow: '#0f0'
        }
    headers = ['h1', 'h2']
    data = [['观音\nLine2', 'Ποσειδῶν']]

    expected_headers = ['\x1b[31;01mh1\x1b[39;00m', '\x1b[31;01mh2\x1b[39;00m']
    expected_data = [
        ['\x1b[38;5;233;48;5;7m观音\x1b[39;49m\n\x1b[38;5;233;48;5;7m'
         'Line2\x1b[39;49m',
         '\x1b[38;5;233;48;5;7mΠοσειδῶν\x1b[39;49m']]
    results = style_output(data, headers, style=CliStyle)


    assert (expected_data, expected_headers) == (list(results[0]), results[1])

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

    assert (expected_data, expected_headers) == (list(output[0]), output[1])


def test_format_integer():
    """Test formatting for an INTEGER datatype."""
    data = [[1], [1000], [1000000]]
    headers = ['h1']
    result_data, result_headers = format_numbers(data,
                                                 headers,
                                                 column_types=(int,),
                                                 integer_format=',',
                                                 float_format=',')

    expected = [['1'], ['1,000'], ['1,000,000']]
    assert expected == list(result_data)
    assert headers == result_headers


def test_format_decimal():
    """Test formatting for a DECIMAL(12, 4) datatype."""
    data = [[Decimal('1.0000')], [Decimal('1000.0000')], [Decimal('1000000.0000')]]
    headers = ['h1']
    result_data, result_headers = format_numbers(data,
                                                 headers,
                                                 column_types=(float,),
                                                 integer_format=',',
                                                 float_format=',')

    expected = [['1.0000'], ['1,000.0000'], ['1,000,000.0000']]
    assert expected == list(result_data)
    assert headers == result_headers


def test_format_float():
    """Test formatting for a REAL datatype."""
    data = [[1.0], [1000.0], [1000000.0]]
    headers = ['h1']
    result_data, result_headers = format_numbers(data,
                                                 headers,
                                                 column_types=(float,),
                                                 integer_format=',',
                                                 float_format=',')
    expected = [['1.0'], ['1,000.0'], ['1,000,000.0']]
    assert expected == list(result_data)
    assert headers == result_headers


def test_format_integer_only():
    """Test that providing one format string works."""
    data = [[1, 1.0], [1000, 1000.0], [1000000, 1000000.0]]
    headers = ['h1', 'h2']
    result_data, result_headers = format_numbers(data, headers, column_types=(int, float),
                                                 integer_format=',')

    expected = [['1', 1.0], ['1,000', 1000.0], ['1,000,000', 1000000.0]]
    assert expected == list(result_data)
    assert headers == result_headers


def test_format_numbers_no_format_strings():
    """Test that numbers aren't formatted without format strings."""
    data = ((1), (1000), (1000000))
    headers = ('h1',)
    result_data, result_headers = format_numbers(data, headers, column_types=(int,))
    assert list(data) == list(result_data)
    assert headers == result_headers


def test_format_numbers_no_column_types():
    """Test that numbers aren't formatted without column types."""
    data = ((1), (1000), (1000000))
    headers = ('h1',)
    result_data, result_headers = format_numbers(data, headers, integer_format=',',
                                  float_format=',')
    assert list(data) == list(result_data)
    assert headers == result_headers

def test_enforce_iterable():
    preprocessors = inspect.getmembers(cli_helpers.tabular_output.preprocessors, inspect.isfunction)
    loremipsum = 'lorem ipsum dolor sit amet consectetur adipiscing elit sed do eiusmod'.split(' ')
    for name, preprocessor in preprocessors:
        preprocessed = preprocessor(zip(loremipsum), ['lorem'], column_types=(str,))
        try:
            first = next(preprocessed[0])
        except StopIteration:
            assert False, "{} gives no output with iterator data".format(name)
        except TypeError:
            assert False, "{} doesn't return iterable".format(name)
        if isinstance(preprocessed[1], types.GeneratorType):
            assert False, "{} returns headers as iterator".format(name)
