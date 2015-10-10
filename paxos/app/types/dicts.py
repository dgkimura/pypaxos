from collections import MutableSequence
from copy import deepcopy


class Dict(MutableSequence):
    def __init__(self, name, obj, protocol):
        self._obj = obj
        self._name = name
        self._protocol = protocol

    def __getitem__(self, key):
        self._protocol.sync(self._name)
        self._obj = self._protocol.get(key)
        return self._obj[key]

    def __setitem__(self, key, value):
        self._protocol.sync(self._name)
        self._obj.__setitem__(key, value)
        self._protocol.update(self._name, self._obj)

    def insert(self, key, value):
        self._protocol.sync(self._name)
        self._obj.__setitem__(key, value)
        self._protocol.update(self._name, self._obj)

    def __delitem__(self, key):
        self._protocol.sync(self._name)
        self._obj.__delitem__(key)
        self._protocol.update(self._name, self._obj)

    def __iter__(self):
        self._protocol.sync(self._name)
        self._obj = self._protocol.get(self._name)
        return iter(self._obj)

    def __len__(self):
        self._protocol.sync(self._name)
        self._obj = self._protocol.get(self._name)
        return len(self._obj)
