from pathlib import Path
from typing import Dict, Iterable, Optional

from ._types import DataType, Format, FormatType, SourceType
from .formats import object_loaders
from .open import as_opener

__all__ = ('load_data',)


file_extensions: Dict[str, Format] = {
    '.yml': 'yaml',
    '.ini': 'conf',
    '.xlsx': 'excel',
    '.pkl': 'pickle',
}
for fmt in Format.__args__:
    if fmt == 'excel':
        continue
    ext_ = f'.{fmt}'
    if ext_ not in file_extensions:
        file_extensions[ext_] = fmt

file_extensions_str = ' '.join(f'{k}->{v}' for k, v in file_extensions.items())
formats_str = ' '.join(Format.__args__)


def load_data(data: DataType, formats: FormatType, sources: SourceType, slow_try_multiple_formats: bool):
    if not sources:
        raise TypeError('"sources" maybe not be empty')
    if not formats:
        raise TypeError('"formats" maybe not be empty')

    if isinstance(sources, str):
        sources_: Iterable[str] = (sources,)
    else:
        sources_ = sources

    format_: Optional[Format] = None
    if 'file' in sources_:
        format_ = find_format(data)

    if slow_try_multiple_formats:
        raise NotImplementedError('slow_try_multiple_formats=True is not yet implemented')
    else:
        if format_ is None:
            format_ = formats[0]
            if format_ not in Format.__args__:
                raise TypeError(f'Unknown format "{format_}", supported formats: {formats_str}')
        elif format_ not in formats:
            raise ValueError(f'File format "{format_}", not in allowed formats: {" ".join(formats)}')

        loader = object_loaders[format_]
        opener = as_opener(data, sources)
        return loader(opener)


def find_format(data: DataType) -> Optional[Format]:
    if isinstance(data, Path):
        path = data
    elif isinstance(data, (str, bytes)):
        # no way to get the filename from strings or bytes
        return None
    else:
        try:
            path = Path(data.name)
        except AttributeError as e:
            raise TypeError('data must be a string, bytes, Path, DummyPath or IO object') from e

    suffixes = path.suffixes
    if suffixes[-1] == '.gz':
        raise NotImplementedError('decompression of ".gz" is not yet implemented')

    ext = suffixes[0]
    try:
        return file_extensions[ext]
    except KeyError as e:
        raise ValueError(f'Extension "{ext}" not supported, options: {file_extensions_str}') from e
