# -*- coding: utf-8 -*-
"""Test the json output adapter."""

from __future__ import unicode_literals

from decimal import Decimal

from cli_helpers.tabular_output import json_output_adapter


def test_jsonl_wrapper():
    """Test the jsonl output adapter."""
    # Test jsonl output.
    data = [["ab\r\nc", 1], ["d", 456]]
    headers = ["letters", "number"]
    output = json_output_adapter.adapter(iter(data), headers, table_format="jsonl")
    assert (
        "\n".join(output)
        == """{"letters":"ab\\r\\nc","number":1}\n{"letters":"d","number":456}"""
    )


def test_unicode_with_jsonl():
    """Test that the jsonl wrapper can pass through non-ascii characters."""
    data = [["观音", 1], ["Ποσειδῶν", 456]]
    headers = ["letters", "number"]
    output = json_output_adapter.adapter(data, headers, table_format="jsonl")
    assert (
        "\n".join(output)
        == """{"letters":"观音","number":1}\n{"letters":"Ποσειδῶν","number":456}"""
    )


def test_decimal_with_jsonl():
    """Test that the jsonl wrapper can pass through Decimal values."""
    data = [["ab\r\nc", 1], ["d", Decimal(4.56)]]
    headers = ["letters", "number"]
    output = json_output_adapter.adapter(iter(data), headers, table_format="jsonl")
    assert (
        "\n".join(output)
        == """{"letters":"ab\\r\\nc","number":1}\n{"letters":"d","number":4.56}"""
    )


def test_null_with_jsonl():
    """Test that the jsonl wrapper can pass through null values."""
    data = [["ab\r\nc", None], ["d", None]]
    headers = ["letters", "value"]
    output = json_output_adapter.adapter(iter(data), headers, table_format="jsonl")
    assert (
        "\n".join(output)
        == """{"letters":"ab\\r\\nc","value":null}\n{"letters":"d","value":null}"""
    )


def test_unicode_with_jsonl_esc():
    """Test that the jsonl_escaped wrapper JSON-escapes non-ascii characters."""
    data = [["观音", 1], ["Ποσειδῶν", 456]]
    headers = ["letters", "number"]
    output = json_output_adapter.adapter(data, headers, table_format="jsonl_escaped")
    assert (
        "\n".join(output)
        == """{"letters":"\\u89c2\\u97f3","number":1}\n{"letters":"\\u03a0\\u03bf\\u03c3\\u03b5\\u03b9\\u03b4\\u1ff6\\u03bd","number":456}"""
    )
