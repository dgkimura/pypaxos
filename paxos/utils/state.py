from threading import Lock
from yaml import dump, load

from paxos.utils.sharedlock import SharedLock
from paxos.utils.storage import Storage


STATE_LOCK = SharedLock()


class State(object):
    __FILENAME = "pypaxos.state"

    def __init__(self, storage=None):
        self._dict = dict()
        self._lock = Lock()
        self._storage = Storage(State.__FILENAME)

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
        STATE_LOCK.acquire()
        try:
            self._dict = load(self._storage.get()) or dict()
        except FileNotFoundError:
            self._dict = dict()
        finally:
            STATE_LOCK.release()

    def _flush(self):
        STATE_LOCK.acquire()
        try:
            self._storage.put(dump(self._dict))
        finally:
            STATE_LOCK.release()
