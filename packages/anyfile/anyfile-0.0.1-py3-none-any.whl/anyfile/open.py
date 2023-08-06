import re
from io import BufferedReader, BytesIO, StringIO, TextIOWrapper
from pathlib import Path
from typing import AnyStr, BinaryIO, Iterable, Protocol, TextIO, TypeVar, Union

from ._types import DataType, DummyPath

__all__ = 'OpenProtocol', 'as_opener', 'OpenPath', 'OpenAnyStr', 'OpenMemoryIO', 'OpenFileIO'
T = TypeVar('T', str, bytes)


class OpenProtocol(Protocol):
    name: str

    def open_text(self) -> Union[StringIO, TextIO]:
        ...

    def open_binary(self) -> Union[BytesIO, BinaryIO]:
        ...

    def open_either(self) -> Union[StringIO, TextIO, BytesIO, BinaryIO]:
        ...


def as_opener(data: DataType, sources: Iterable[str]) -> OpenProtocol:  # noqa C901
    if isinstance(data, Path):
        if 'file' not in sources:
            raise TypeError('"file" not in sources, Path not allowed')
        return OpenPath(data)
    elif isinstance(data, str):
        for source in sources:
            if source == 'file':
                return OpenPath(Path(data))
            elif source == 'memory':
                return OpenAnyStr(data)
            elif source == 'http':
                if re.match('https?://', data):
                    raise NotImplementedError('http not yet implemented')

        raise TypeError(f'unable to interpret string as any of: {" ".join(sources)}')
    elif isinstance(data, bytes):
        if 'memory' not in sources:
            raise TypeError('"memory" not in sources, bytes not allowed')
        return OpenAnyStr(data)
    elif isinstance(data, DummyPath):
        if 'memory' not in sources:
            raise TypeError('"memory" not in sources, DummyPath not allowed')
        return OpenAnyStr(data.raw_data)
    elif isinstance(data, (TextIOWrapper, BufferedReader)):
        if 'file' not in sources:
            raise TypeError(f'"file" not in sources, {type(data).__name__} not allowed')
        return OpenFileIO(data)
    elif isinstance(data, (StringIO, BytesIO)):
        if 'memory' not in sources:
            raise TypeError(f'"memory" not in sources, {type(data).__name__} not allowed')
        return OpenMemoryIO(data)
    else:
        raise TypeError('data must be a string, bytes, Path, DummyPath or IO object')


class OpenAnyStr(OpenProtocol):
    def __init__(self, data: AnyStr):
        self._str_bytes = data

    def open_text(self) -> StringIO:
        if isinstance(self._str_bytes, str):
            s = self._str_bytes
        else:
            s = self._str_bytes.decode()
        return StringIO(s)

    def open_binary(self) -> BytesIO:
        if isinstance(self._str_bytes, str):
            b = self._str_bytes.encode()
        else:
            b = self._str_bytes
        return BytesIO(b)

    def open_either(self) -> Union[StringIO, BytesIO]:
        if isinstance(self._str_bytes, str):
            return StringIO(self._str_bytes)
        else:
            return BytesIO(self._str_bytes)


class OpenPath(OpenProtocol):
    def __init__(self, path: Path):
        self.name = path.name
        self._path = path

    def open_text(self) -> TextIO:
        return self._path.open(mode='r', newline='')

    def open_binary(self) -> BinaryIO:
        return self._path.open(mode='rb')

    def open_either(self) -> Union[TextIO, BinaryIO]:
        return self._path.open(mode='rb')


class OpenMemoryIO(OpenProtocol):
    def __init__(self, io: Union[StringIO, BytesIO]):
        self._io = io

    def open_text(self) -> StringIO:
        if isinstance(self._io, StringIO):
            str_io = self._io
        else:
            str_io = StringIO(self._io.read().decode())
        return str_io

    def open_binary(self) -> BytesIO:
        if isinstance(self._io, StringIO):
            bytes_io = BytesIO(self._io.read().encode())
        else:
            bytes_io = self._io
        return bytes_io

    def open_either(self) -> Union[StringIO, BytesIO]:
        return self._io


class DontCloseReadContext:
    def __init__(self, obj: Union[TextIO, BinaryIO]):
        self._obj = obj

    def __enter__(self):
        return self

    def read(self) -> T:
        return self._obj.read()

    def __iter__(self):
        return self._obj

    def __exit__(self, exc_type, exc_val, exc_tb) -> None:
        pass


class OpenFileIO(OpenProtocol):
    def __init__(self, io: Union[TextIO, BinaryIO]):
        self._io = io

    def open_text(self) -> Union[StringIO, TextIO]:
        if isinstance(self._io, TextIOWrapper):
            return DontCloseReadContext(self._io)
        else:
            return StringIO(self._io.read().decode())

    def open_binary(self) -> Union[BytesIO, BinaryIO]:
        if isinstance(self._io, TextIOWrapper):
            return BytesIO(self._io.read().encode())
        else:
            return DontCloseReadContext(self._io)

    def open_either(self) -> Union[StringIO, TextIO, BytesIO, BinaryIO]:
        return DontCloseReadContext(self._io)
