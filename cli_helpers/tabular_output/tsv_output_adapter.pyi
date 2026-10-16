from collections.abc import Iterable, Iterator, Sequence
from typing import Literal, Protocol

class _Preprocessor(Protocol):
    def __call__(
        self,
        data: Iterable[Sequence[object]],
        headers: Sequence[object],
        **kwargs: object
    ) -> tuple[Iterable[Sequence[object]], Sequence[object]]: ...

supported_formats: tuple[Literal["tsv"], Literal["tsv_noheader"]]
preprocessors: tuple[_Preprocessor, _Preprocessor, _Preprocessor]

def adapter(
    data: Iterable[Sequence[str]],
    headers: Sequence[str],
    table_format: Literal["tsv", "tsv_noheader"] = ...,
    **kwargs: object
) -> Iterator[str]: ...
