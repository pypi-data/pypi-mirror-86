from typing import TYPE_CHECKING, Any, Optional, Tuple, Type, overload

from ._types import DataType, DummyPath, Format, FormatType, SourceType
from .main import load_data

if TYPE_CHECKING:
    from pydantic import BaseModel

    from ._types import ModelT


__all__ = 'Format', 'load_object', 'load_list', 'DummyPath'


LoadObjectDefaults: Tuple[Format, ...] = ('json', 'yaml', 'toml', 'xml', 'conf', 'msgpack', 'pickle')
SourceTypeDefaults: Tuple[Format, ...] = ('file', 'memory')


@overload
def load_object(
    data: DataType,
    model: None = None,
    *,
    formats: FormatType = LoadObjectDefaults,
    sources: SourceType = SourceTypeDefaults,
    slow_try_multiple_formats: bool = False,
) -> Any:
    ...


@overload
def load_object(
    data: DataType,
    model: Type['ModelT'],
    *,
    formats: FormatType = LoadObjectDefaults,
    sources: SourceType = SourceTypeDefaults,
    slow_try_multiple_formats: bool = False,
) -> 'ModelT':
    ...


def load_object(
    data: DataType,
    model: Optional[Type['BaseModel']] = None,
    *,
    formats: FormatType = LoadObjectDefaults,
    sources: SourceType = SourceTypeDefaults,
    slow_try_multiple_formats: bool = False,
):
    data = load_data(data, formats, sources, slow_try_multiple_formats)
    if model:
        return model.parse_obj(data)
    else:
        return data


ListObjectDefaults: Tuple[Format, ...] = (
    'csv',
    'excel',
    'json-lines',
    'json',
    'yaml',
    'toml',
    'xml',
    'conf',
    'msgpack',
    'pickle',
)


def load_list(
    data: DataType,
    model: Optional['ModelT'] = None,
    *,
    formats: FormatType = ListObjectDefaults,
    sources: SourceType = SourceTypeDefaults,
    heading_row: bool = True,
):
    pass


def load_inspect(data, model):
    pass
