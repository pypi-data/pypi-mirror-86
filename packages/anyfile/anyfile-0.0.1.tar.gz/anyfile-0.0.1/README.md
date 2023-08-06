# anyfile

[![CI](https://github.com/samuelcolvin/anyfile/workflows/ci/badge.svg?event=push)](https://github.com/samuelcolvin/anyfile/actions?query=event%3Apush+branch%3Amaster+workflow%3Aci)
[![Coverage](https://codecov.io/gh/samuelcolvin/anyfile/branch/master/graph/badge.svg)](https://codecov.io/gh/samuelcolvin/anyfile)
[![pypi](https://img.shields.io/pypi/v/anyfile.svg)](https://pypi.python.org/pypi/anyfile)
[![versions](https://img.shields.io/pypi/pyversions/anyfile.svg)](https://github.com/samuelcolvin/anyfile)
[![license](https://img.shields.io/github/license/samuelcolvin/anyfile.svg)](https://github.com/samuelcolvin/anyfile/blob/master/LICENSE)

**Work in progress, not ready for general use.**

Load (almost) any structured file, then parse its data with pydantic

Will supports:
* JSON
* CSV
* YAML
* TOML
* JSON lines
* config / ini
* msgpack
* Excel
* pickle
* zip
* tar gz

Perhaps one day:
* HTML
* HDF5
* parquet
* SQL

Data can be loaded from the local filesystem, URLs or memory (bytes, string, io).

