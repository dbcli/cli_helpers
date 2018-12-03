# -*- coding: utf-8 -*-
"""Test CLI Helpers' utility functions and helpers."""

from __future__ import unicode_literals

from cli_helpers import utils


def test_bytes_to_string_hexlify():
    """Test that bytes_to_string() hexlifies binary data."""
    assert utils.bytes_to_string(b'\xff') == '0xff'


def test_bytes_to_string_decode_bytes():
    """Test that bytes_to_string() decodes bytes."""
    assert utils.bytes_to_string(b'foobar') == 'foobar'


def test_bytes_to_string_non_bytes():
    """Test that bytes_to_string() returns non-bytes untouched."""
    assert utils.bytes_to_string('abc') == 'abc'
    assert utils.bytes_to_string(1) == 1


def test_to_string_bytes():
    """Test that to_string() converts bytes to a string."""
    assert utils.to_string(b"foo") == 'foo'


def test_to_string_non_bytes():
    """Test that to_string() converts non-bytes to a string."""
    assert utils.to_string(1) == '1'
    assert utils.to_string(2.29) == '2.29'


def test_truncate_string():
    """Test string truncate preprocessor."""
    val = 'x' * 1000
    assert utils.truncate_string(val, 10) == 'x' * 10


def test_intlen_with_decimal():
    """Test that intlen() counts correctly with a decimal place."""
    assert utils.intlen('11.1') == 2
    assert utils.intlen('1.1') == 1


def test_intlen_without_decimal():
    """Test that intlen() counts correctly without a decimal place."""
    assert utils.intlen('11') == 2


def test_filter_dict_by_key():
    """Test that filter_dict_by_key() filter unwanted items."""
    keys = ('foo', 'bar')
    d = {'foo': 1, 'foobar': 2}
    fd = utils.filter_dict_by_key(d, keys)
    assert len(fd) == 1
    assert all([k in keys for k in fd])
