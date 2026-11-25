import json
from collections.abc import Iterable, Iterator, Sequence
from typing import Literal, Protocol

class _Preprocessor(Protocol):
    def __call__(
        self,
        data: Iterable[Sequence[object]],
        headers: Sequence[object],
        **kwargs: object
    ) -> tuple[Iterable[Sequence[object]], Sequence[object]]: ...

supported_formats: tuple[Literal["jsonl"], Literal["jsonl_escaped"]]
preprocessors: tuple[_Preprocessor,]

class CustomEncoder(json.JSONEncoder):
    def default(self, o: object) -> float: ...

def adapter(
    data: Iterable[Sequence[object]],
    headers: Iterable[str | int | float | bool | None],
    table_format: Literal["jsonl", "jsonl_escaped"] = ...,
    **_kwargs: object
) -> Iterator[str]: ...
