# postit.py
from os.path import isfile
from threading import Lock
from yaml import dump, load

from paxos.net.proposal import default_proposal


DEFAULT_TYPES = {
    "proposal": default_proposal(),
    "str": "",
    "int": 0
}


class PostIt(object):
    def __init__(self, _file):
        self._file = _file
        self._lock = Lock()

        self._dict = dict()
        self._is_stale = True

    def read(self, key):
        if self._is_stale:
            self._refresh()

        if key in self._dict:
            return self._dict[key]

        for k, v in DEFAULT_TYPES.items():
            if key.endswith(k):
                return v

        return None

    def write(self, key, value):
        if self._is_stale:
            self._refresh()

        self._dict[key] = value
        self._flush()

    def _refresh(self):
        if isfile(self._file):
            with open(self._file, 'r') as f:
                self._dict = load(f) or dict()
        self._is_stale = False

    def _flush(self):
        try:
            self._lock.acquire()
            with open(self._file, 'w+') as f:
                dump(self._dict, f)
                f.flush()
        finally:
            self._lock.release()
