import json
from pathlib import Path


class IdentityManager:
    def __init__(self, db_path: Path):
        try:
            self._data: dict = json.loads(db_path.read_text(encoding='utf8'))
        except FileNotFoundError:
            self._data = {}
        self._db_path = db_path
        self._has_changed = False

    def __getitem__(self, item) -> str:
        return self._data[item]

    def __setitem__(self, key, value):
        if not (key in self._data and self._data[key] == value):
            self._data[key] = value
            self._has_changed = True

    def __contains__(self, item) -> True:
        return item in self._data

    def items(self) -> tuple[str, str]:
        for key, value in self._data.items():
            yield key, value

    def save(self):
        if self._has_changed:
            self._db_path.parent.mkdir(exist_ok=True)
            self._db_path.write_text(json.dumps(self._data, ensure_ascii=False))
            self._has_changed = False
