from collections.abc import Iterable, Iterator, Mapping, Sequence
from typing import TypeVar, overload

from pygments.style import StyleMeta
from pygments.token import _TokenType

_T = TypeVar("_T")
_H = TypeVar("_H")

def truncate_string(
    data: Iterable[Sequence[_T]],
    headers: Sequence[_H],
    max_field_width: int | None = ...,
    skip_multiline_string: bool = ...,
    **_: object
) -> tuple[Iterator[list[_T]], list[_H]]: ...
def convert_to_string(
    data: Iterable[Sequence[object]], headers: Sequence[object], **_: object
) -> tuple[Iterator[list[str]], list[str]]: ...
def convert_to_undecoded_string(
    data: Iterable[Sequence[object]], headers: Sequence[object], **_: object
) -> tuple[Iterator[list[str | None]], list[str | None]]: ...
def override_missing_value(
    data: Iterable[Sequence[_T]],
    headers: Sequence[_H],
    style: str | StyleMeta | None = ...,
    missing_value_token: _TokenType | None = ...,
    missing_value: str = ...,
    **_: object
) -> tuple[Iterator[list[_T | str]], Sequence[_H]]: ...
def override_tab_value(
    data: Iterable[Sequence[_T]],
    headers: Sequence[_H],
    new_value: str = ...,
    **_: object
) -> tuple[Iterator[list[_T]], Sequence[_H]]: ...
def escape_newlines(
    data: Iterable[Sequence[_T]], headers: Sequence[_H], **_: object
) -> tuple[Iterator[list[_T]], Sequence[_H]]: ...
def bytes_to_string(
    data: Iterable[Sequence[_T]], headers: Sequence[_H], **_: object
) -> tuple[Iterator[list[_T | str]], list[_H | str]]: ...
def align_decimals(
    data: Iterable[Sequence[_T]],
    headers: Sequence[_H],
    column_types: Sequence[type[object]] = ...,
    **_: object
) -> tuple[Iterator[list[_T | str]], Sequence[_H]]: ...
def quote_whitespaces(
    data: Iterable[Sequence[object]],
    headers: Sequence[_H],
    quotestyle: str = ...,
    **_: object
) -> tuple[Iterator[list[str]], Sequence[_H]]: ...
@overload
def style_output(
    data: Iterable[Sequence[_T]],
    headers: Sequence[_H],
    style: None = ...,
    header_token: _TokenType | None = ...,
    odd_row_token: _TokenType | None = ...,
    even_row_token: _TokenType | None = ...,
    **_: object
) -> tuple[Iterator[Sequence[_T]], Sequence[_H]]: ...
@overload
def style_output(
    data: Iterable[Sequence[str]],
    headers: Sequence[str],
    style: str | StyleMeta,
    header_token: _TokenType | None = ...,
    odd_row_token: _TokenType | None = ...,
    even_row_token: _TokenType | None = ...,
    **_: object
) -> tuple[Iterator[Sequence[str]], Sequence[str]]: ...
def format_numbers(
    data: Iterable[Sequence[_T]],
    headers: Sequence[_H],
    column_types: Sequence[type[object]] = ...,
    integer_format: str | None = ...,
    float_format: str | None = ...,
    **_: object
) -> tuple[Iterator[list[_T | str]], Sequence[_H]]: ...
def format_timestamps(
    data: Iterable[Sequence[_T]],
    headers: Sequence[_H],
    column_date_formats: Mapping[_H, str] | None = ...,
    **_: object
) -> tuple[Iterator[list[_T | str]], Sequence[_H]]: ...
