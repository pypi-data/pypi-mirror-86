from pathlib import Path

import anyfile


def test_load_json(tmp_path: Path):
    f = tmp_path / 'file.json'
    f.write_text('{"foo": 1}')
    assert anyfile.load_object(f) == {'foo': 1}
