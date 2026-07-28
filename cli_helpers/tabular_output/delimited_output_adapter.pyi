from collections.abc import Iterable, Iterator, Sequence
from typing import Literal, Protocol

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
    **kwargs: object
) -> Iterator[str]: ...
