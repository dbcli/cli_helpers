# -*- coding: utf-8 -*-
"""Test the generic output formatter interface."""

from __future__ import unicode_literals
from decimal import Decimal
from textwrap import dedent

import pytest

from cli_helpers.tabular_output import format_output, TabularOutputFormatter
from cli_helpers.compat import binary_type, text_type
from cli_helpers.utils import strip_ansi


def test_tabular_output_formatter():
    """Test the TabularOutputFormatter class."""
    headers = ["text", "numeric"]
    data = [
        ["abc", Decimal(1)],
        ["defg", Decimal("11.1")],
        ["hi", Decimal("1.1")],
        ["Pablo\rß\n", 0],
    ]
    expected = dedent(
        """\
        +-------+---------+
        | text  | numeric |
        +-------+---------+
        | abc   | 1       |
        | defg  | 11.1    |
        | hi    | 1.1     |
        | Pablo | 0       |
        | ß     |         |
        +-------+---------+"""
    )

    print(expected)
    print(
        "\n".join(
            TabularOutputFormatter().format_output(
                iter(data), headers, format_name="ascii"
            )
        )
    )
    assert expected == "\n".join(
        TabularOutputFormatter().format_output(iter(data), headers, format_name="ascii")
    )


def test_tabular_output_escaped():
    """Test the ascii_escaped output format."""
    headers = ["text", "numeric"]
    data = [
        ["abc", Decimal(1)],
        ["defg", Decimal("11.1")],
        ["hi", Decimal("1.1")],
        ["Pablo\rß\n", 0],
    ]
    expected = dedent(
        """\
        +------------+---------+
        | text       | numeric |
        +------------+---------+
        | abc        | 1       |
        | defg       | 11.1    |
        | hi         | 1.1     |
        | Pablo\\rß\\n | 0       |
        +------------+---------+"""
    )

    print(expected)
    print(
        "\n".join(
            TabularOutputFormatter().format_output(
                iter(data), headers, format_name="ascii_escaped"
            )
        )
    )
    assert expected == "\n".join(
        TabularOutputFormatter().format_output(
            iter(data), headers, format_name="ascii_escaped"
        )
    )


def test_tabular_output_mysql():
    """Test the mysql output format."""
    headers = ["text", "numeric"]
    data = [
        ["abc", Decimal(1)],
        ["defg", Decimal("11.1")],
        ["hi", Decimal("1.1")],
        ["Pablo\rß\n", 0],
    ]
    expected = dedent(
        """\
        +-------+---------+
        | text  | numeric |
        +-------+---------+
        | abc   |       1 |
        | defg  |    11.1 |
        | hi    |     1.1 |
        | Pablo |       0 |
        | ß     |         |
        +-------+---------+"""
    )

    print(expected)
    print(
        "\n".join(
            TabularOutputFormatter().format_output(
                iter(data), headers, format_name="mysql"
            )
        )
    )
    assert expected == "\n".join(
        TabularOutputFormatter().format_output(iter(data), headers, format_name="mysql")
    )


def test_tabular_output_mysql_unicode():
    """Test the mysql_unicode output format."""
    headers = ["text", "numeric"]
    data = [
        ["abc", Decimal(1)],
        ["defg", Decimal("11.1")],
        ["hi", Decimal("1.1")],
        ["Pablo\rß\n", 0],
    ]
    expected = dedent(
        """\
        ┌───────┬─────────┐
        │ text  │ numeric │
        ├───────┼─────────┤
        │ abc   │       1 │
        │ defg  │    11.1 │
        │ hi    │     1.1 │
        │ Pablo │       0 │
        │ ß     │         │
        └───────┴─────────┘"""
    )

    print(expected)
    print(
        "\n".join(
            TabularOutputFormatter().format_output(
                iter(data), headers, format_name="mysql_unicode"
            )
        )
    )
    assert expected == "\n".join(
        TabularOutputFormatter().format_output(
            iter(data), headers, format_name="mysql_unicode"
        )
    )


def test_tabular_format_output_wrapper():
    """Test the format_output wrapper."""
    data = [["1", None], ["2", "Sam"], ["3", "Joe"]]
    headers = ["id", "name"]
    expected = dedent(
        """\
        +----+------+
        | id | name |
        +----+------+
        | 1  | N/A  |
        | 2  | Sam  |
        | 3  | Joe  |
        +----+------+"""
    )

    assert expected == "\n".join(
        format_output(iter(data), headers, format_name="ascii", missing_value="N/A")
    )


def test_additional_preprocessors():
    """Test that additional preprocessors are run."""

    def hello_world(data, headers, **_):
        def hello_world_data(data):
            for row in data:
                for i, value in enumerate(row):
                    if value == "hello":
                        row[i] = "{}, world".format(value)
                yield row

        return hello_world_data(data), headers

    data = [["foo", None], ["hello!", "hello"]]
    headers = "ab"

    expected = dedent(
        """\
        +--------+--------------+
        | a      | b            |
        +--------+--------------+
        | foo    | hello        |
        | hello! | hello, world |
        +--------+--------------+"""
    )

    assert expected == "\n".join(
        TabularOutputFormatter().format_output(
            iter(data),
            headers,
            format_name="ascii",
            preprocessors=(hello_world,),
            missing_value="hello",
        )
    )


def test_format_name_attribute():
    """Test the the format_name attribute be set and retrieved."""
    formatter = TabularOutputFormatter(format_name="plain")
    assert formatter.format_name == "plain"
    formatter.format_name = "simple"
    assert formatter.format_name == "simple"

    with pytest.raises(ValueError):
        formatter.format_name = "foobar"


def test_headless_tabulate_format():
    """Test that a headless formatter doesn't display headers"""
    formatter = TabularOutputFormatter(format_name="minimal")
    headers = ["text", "numeric"]
    data = [["a"], ["b"], ["c"]]
    expected = "a\nb\nc"
    assert expected == "\n".join(
        TabularOutputFormatter().format_output(
            iter(data),
            headers,
            format_name="minimal",
        )
    )


def test_unsupported_format():
    """Test that TabularOutputFormatter rejects unknown formats."""
    formatter = TabularOutputFormatter()

    with pytest.raises(ValueError):
        formatter.format_name = "foobar"

    with pytest.raises(ValueError):
        formatter.format_output((), (), format_name="foobar")


def test_supported_json_formats():
    """Test that the JSONl formats are known."""
    formatter = TabularOutputFormatter()
    assert "jsonl" in formatter.supported_formats
    assert "jsonl_escaped" in formatter.supported_formats


def test_tabulate_ansi_escape_in_default_value():
    """Test that ANSI escape codes work with tabulate."""

    data = [["1", None], ["2", "Sam"], ["3", "Joe"]]
    headers = ["id", "name"]

    styled = format_output(
        iter(data),
        headers,
        format_name="psql",
        missing_value="\x1b[38;5;10mNULL\x1b[39m",
    )
    unstyled = format_output(
        iter(data), headers, format_name="psql", missing_value="NULL"
    )

    stripped_styled = [strip_ansi(s) for s in styled]

    assert list(unstyled) == stripped_styled


def test_get_type():
    """Test that _get_type returns the expected type."""
    formatter = TabularOutputFormatter()

    tests = (
        (1, int),
        (2.0, float),
        (b"binary", binary_type),
        ("text", text_type),
        (None, type(None)),
        ((), text_type),
    )

    for value, data_type in tests:
        assert data_type is formatter._get_type(value)


def test_provide_column_types():
    """Test that provided column types are passed to preprocessors."""
    expected_column_types = (bool, float)
    data = ((1, 1.0), (0, 2))
    headers = ("a", "b")

    def preprocessor(data, headers, column_types=(), **_):
        assert expected_column_types == column_types
        return data, headers

    format_output(
        data,
        headers,
        "csv",
        column_types=expected_column_types,
        preprocessors=(preprocessor,),
    )


def test_enforce_iterable():
    """Test that all output formatters accept iterable"""
    formatter = TabularOutputFormatter()
    loremipsum = (
        "lorem ipsum dolor sit amet consectetur adipiscing elit sed do eiusmod".split(
            " "
        )
    )

    for format_name in formatter.supported_formats:
        formatter.format_name = format_name
        try:
            formatted = next(formatter.format_output(zip(loremipsum), ["lorem"]))
        except TypeError:
            assert False, "{0} doesn't return iterable".format(format_name)


@pytest.mark.parametrize(
    "extra_kwargs",
    [
        {},
        {"style": "default"},
        {"style": "colorful"},
    ],
)
def test_all_text_type(extra_kwargs):
    """Test the TabularOutputFormatter class."""
    data = [[1, "", None, Decimal(2)]]
    headers = ["col1", "col2", "col3", "col4"]
    output_formatter = TabularOutputFormatter()
    for format_name in output_formatter.supported_formats:
        for row in output_formatter.format_output(
            iter(data), headers, format_name=format_name, **extra_kwargs
        ):
            assert isinstance(row, text_type), "not unicode for {}".format(format_name)
