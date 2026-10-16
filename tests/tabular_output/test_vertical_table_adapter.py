# -*- coding: utf-8 -*-
"""Test the vertical table formatter."""

from textwrap import dedent

import pytest

from cli_helpers.compat import text_type
from cli_helpers.utils import strip_ansi
from cli_helpers.tabular_output import TabularOutputFormatter
from cli_helpers.tabular_output import vertical_table_adapter


@pytest.mark.parametrize(
    "headers, expected",
    [
        (["name", "age"], ["name | Alice", "age  | 30"]),
        (["名前", "age"], ["名前 | Alice", "age  | 30"]),
        (["e\u0301", "id"], ["e\u0301  | Alice", "id | 30"]),
    ],
)
def test_vertical_table_header_display_width(headers, expected):
    formatter = TabularOutputFormatter("vertical")
    output = list(formatter.format_output([["Alice", 30]], headers))
    assert output[0].splitlines()[1:] == expected


def test_vertical_table_styled_header_display_width():
    Style = pytest.importorskip("pygments.style").Style
    Token = pytest.importorskip("pygments.token").Token

    class HeaderStyle(Style):
        styles = {Token.Output.Header: "bold"}

    formatter = TabularOutputFormatter("vertical")
    output = list(
        formatter.format_output([["Alice", 30]], ["名前", "age"], style=HeaderStyle)
    )
    assert strip_ansi(output[0]).splitlines()[1:] == ["名前 | Alice", "age  | 30"]


def test_vertical_table():
    """Test the default settings for vertical_table()."""
    results = [("hello", text_type(123)), ("world", text_type(456))]

    expected = dedent(
        """\
        ***************************[ 1. row ]***************************
        name | hello
        age  | 123
        ***************************[ 2. row ]***************************
        name | world
        age  | 456"""
    )
    assert expected == "\n".join(
        vertical_table_adapter.adapter(results, ("name", "age"))
    )


def test_vertical_table_customized():
    """Test customized settings for vertical_table()."""
    results = [("john", text_type(47)), ("jill", text_type(50))]

    expected = dedent(
        """\
        -[ PERSON 1 ]-----
        name | john
        age  | 47
        -[ PERSON 2 ]-----
        name | jill
        age  | 50"""
    )
    assert expected == "\n".join(
        vertical_table_adapter.adapter(
            results,
            ("name", "age"),
            sep_title="PERSON {n}",
            sep_character="-",
            sep_length=(1, 5),
        )
    )
