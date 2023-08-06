from pathlib import Path
from typing import IO, TYPE_CHECKING, AnyStr, List, Literal, Tuple, TypeVar, Union

__all__ = 'Format', 'FormatType', 'Sources', 'SourceType', 'DataType', 'ModelT', 'DummyPath'

Format = Literal[
    'json',
    'csv',
    'yaml',
    'toml',
    'json-lines',
    'xml',
    'conf',
    'msgpack',
    'excel',
    'pickle',
    'zip',
    'tar',
]


FormatType = Union[Format, List[Format], Tuple[Format, ...]]
Sources = Literal['file', 'http', 'memory']
SourceType = Union[Sources, List[Sources], Tuple[Sources, ...]]

if TYPE_CHECKING:
    from pydantic import BaseModel

    ModelT = TypeVar('ModelT', bound=BaseModel)


class DummyPath:
    __slots__ = 'name', 'raw_data'

    def __init__(self, name: str, data: AnyStr):
        self.name = name
        self.raw_data = data


DataType = Union[str, bytes, Path, DummyPath, IO]
