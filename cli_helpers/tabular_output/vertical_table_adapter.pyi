from collections.abc import Iterable, Iterator, Sequence
from typing import Literal, Protocol

class _Preprocessor(Protocol):
    def __call__(
        self,
        data: Iterable[Sequence[object]],
        headers: Sequence[object],
        **kwargs: object
    ) -> tuple[Iterable[Sequence[object]], Sequence[object]]: ...

supported_formats: tuple[Literal["vertical"]]
preprocessors: tuple[_Preprocessor, _Preprocessor, _Preprocessor]

def vertical_table(
    data: Iterable[Sequence[str]],
    headers: Sequence[str],
    sep_title: str = ...,
    sep_character: str = ...,
    sep_length: int | tuple[int, int] = ...,
) -> Iterator[str]: ...
def adapter(
    data: Iterable[Sequence[str]],
    headers: Sequence[str],
    *,
    sep_title: str = ...,
    sep_character: str = ...,
    sep_length: int | tuple[int, int] = ...,
    **kwargs: object
) -> Iterator[str]: ...
