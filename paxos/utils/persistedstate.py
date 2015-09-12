from threading import Lock
from yaml import dump, load

from paxos.utils.storage import Storage


class PersistedState(object):
    __FILENAME = "pypaxos.state"

    def __init__(self, storage=None):
        self._dict = dict()
        self._lock = Lock()
        self._storage = Storage(PersistedState.__FILENAME)

        if storage is not None:
            self._storage = storage

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
        try:
            self._dict = load(self._storage.get()) or dict()
        except FileNotFoundError:
            self._dict = dict()

    def _flush(self):
        self._storage.put(dump(self._dict))

    def lock(self):
        return self._lock
