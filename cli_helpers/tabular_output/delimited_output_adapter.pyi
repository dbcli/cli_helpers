import sys
from collections.abc import Iterable, Iterator, Sequence
from typing import Literal, Protocol

if sys.version_info >= (3, 12):
    _Quoting = Literal[0, 1, 2, 3, 4, 5]
else:
    _Quoting = Literal[0, 1, 2, 3]

class _Preprocessor(Protocol):
    def __call__(
        self,
        data: Iterable[Sequence[object]],
        headers: Sequence[object],
        **kwargs: object
    ) -> tuple[Iterable[Sequence[object]], Sequence[object]]: ...

supported_formats: tuple[
    Literal["csv"],
    Literal["csv-tab"],
    Literal["csv-noheader"],
    Literal["csv-tab-noheader"],
]
preprocessors: tuple[_Preprocessor, _Preprocessor]

class linewriter:
    line: str | None
    def __init__(self) -> None: ...
    def reset(self) -> None: ...
    def write(self, d: str) -> None: ...

def adapter(
    data: Iterable[Sequence[object]],
    headers: Sequence[object],
    table_format: Literal["csv", "csv-tab", "csv-noheader", "csv-tab-noheader"] = ...,
    *,
    dialect: object = ...,
    delimiter: str = ...,
    doublequote: bool = ...,
    escapechar: str | None = ...,
    quotechar: str | None = ...,
    quoting: _Quoting = ...,
    skipinitialspace: bool = ...,
    strict: bool = ...,
    **kwargs: object
) -> Iterator[str]: ...
