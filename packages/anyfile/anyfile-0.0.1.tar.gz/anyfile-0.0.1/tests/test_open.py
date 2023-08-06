import csv
import json
from contextlib import contextmanager
from io import BytesIO, StringIO
from pathlib import Path

import pytest

from anyfile.open import OpenAnyStr, OpenFileIO, OpenMemoryIO, OpenPath


@contextmanager
def generate_open_path(string_value: str, tmp_path: Path):
    file_path = tmp_path / 'test.json'
    file_path.write_text(string_value)
    yield OpenPath(file_path)


@contextmanager
def generate_open_str(string_value: str, tmp_path):
    yield OpenAnyStr(string_value)


@contextmanager
def generate_open_bytes(string_value: str, tmp_path):
    yield OpenAnyStr(string_value)


@contextmanager
def generate_open_str_io(string_value: str, tmp_path):
    yield OpenMemoryIO(StringIO(string_value))


@contextmanager
def generate_open_bytes_io(string_value: str, tmp_path):
    yield OpenMemoryIO(BytesIO(string_value.encode()))


@contextmanager
def generate_open_file_obj_str(string_value: str, tmp_path: Path):
    file_path = tmp_path / 'test.json'
    file_path.write_text(string_value)
    with file_path.open('r') as f:
        yield OpenFileIO(f)


@contextmanager
def generate_open_file_obj_bytes(string_value: str, tmp_path: Path):
    file_path = tmp_path / 'test.json'
    file_path.write_text(string_value)
    with file_path.open('rb') as f:
        yield OpenFileIO(f)


generators = [
    generate_open_path,
    generate_open_str,
    generate_open_bytes,
    generate_open_str_io,
    generate_open_bytes_io,
    generate_open_file_obj_str,
    generate_open_file_obj_bytes,
]


@pytest.mark.parametrize('generator_function', generators)
def test_text(tmp_path: Path, generator_function):
    with generator_function('{"foo": 1}', tmp_path) as p:
        with p.open_text() as f:
            assert f.read() == '{"foo": 1}'


@pytest.mark.parametrize('generator_function', generators)
def test_binary(tmp_path: Path, generator_function):
    with generator_function('{"foo": 1}', tmp_path) as p:
        with p.open_binary() as f:
            assert f.read() == b'{"foo": 1}'


@pytest.mark.parametrize('generator_function', generators)
def test_either(tmp_path: Path, generator_function):
    with generator_function('{"foo": 1}', tmp_path) as p:
        with p.open_either() as f:
            assert f.read() in ('{"foo": 1}', b'{"foo": 1}')


@pytest.mark.parametrize('generator_function', generators)
def test_json(tmp_path: Path, generator_function):
    with generator_function('{"foo": 1}', tmp_path) as p:
        with p.open_binary() as f:
            assert json.load(f) == {'foo': 1}


@pytest.mark.parametrize('generator_function', generators)
def test_csv(tmp_path: Path, generator_function):
    with generator_function('foo,bar,spam\r\n1,2,3', tmp_path) as p:
        with p.open_text() as f:
            reader = csv.DictReader(f)
            assert list(reader) == [{'foo': '1', 'bar': '2', 'spam': '3'}]
