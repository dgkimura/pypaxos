from collections import MutableMapping
from os.path import isfile
from threading import Lock
from yaml import dump, load


class PersistedState(object):
    def __init__(self, _file, **kwargs):
        self._dict = dict()

        self._file = _file
        self._lock = Lock()

        self._refresh()

    def read(self, key):
        return self._dict[key]

    def write(self, key, value):
        self._dict[key] = value
        self._flush()

    def set_default(self, key, value):
        if not key in self._dict:
            self.write(key, value)

    def _refresh(self):
        if isfile(self._file):
            with open(self._file, 'r') as f:
                self._dict = load(f) or dict()

    def _flush(self):
        with open(self._file, 'w+') as f:
            dump(self._dict, f)
            f.flush()

    def lock(self):
        return self._lock
