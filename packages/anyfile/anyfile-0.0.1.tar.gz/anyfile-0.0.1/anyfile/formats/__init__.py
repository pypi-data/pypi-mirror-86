import configparser
import csv
import json
import pickle
from typing import Any, Callable, Dict

from ..open import OpenProtocol

__all__ = ('object_loaders',)


def load_json(opener: OpenProtocol) -> Any:
    with opener.open_either() as f:
        return json.load(f)


def load_conf(opener: OpenProtocol) -> Any:
    config = configparser.ConfigParser()
    with opener.open_text() as f:
        return config.read_file(f)


def load_csv(opener: OpenProtocol) -> Dict[str, str]:
    with opener.open_text() as f:
        reader = csv.DictReader(f)
        return next(reader)


def load_pickle(opener: OpenProtocol) -> Any:
    with opener.open_binary() as f:
        return pickle.load(f)


object_loaders: Dict[str, Callable[[OpenProtocol], Any]] = {
    'json': load_json,
    'csv': load_csv,
    # 'yaml':,
    # 'toml':,
    # 'json-lines':,
    # 'xml':,
    'conf': load_conf,
    # 'msgpack':,
    # 'excel':,
    'pickle': load_pickle,
    # 'zip':,
    # 'tar':,
}
