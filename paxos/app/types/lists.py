from collections import MutableSequence
from copy import deepcopy


class List(MutableSequence):
    def __init__(self, name, obj, protocol):
        self._obj = obj
        self._name = name
        self._protocol = protocol

    def __len__(self):
        return len(self._obj)

    def __getitem__(self, i):
        self._protocol.sync(self._name)
        self._obj = self._protocol.get(self._name)
        return self._obj[i]

    def __delitem__(self, i):
        obj = deepcopy(self._obj)
        del obj[i]
        self._protocol.update(self._name, obj)

    def __setitem__(self, i, v):
        obj = deepcopy(self._obj)
        obj[i] = v
        self._protocol.update(self._name, obj)

    def insert(self, i, v):
        obj = deepcopy(self._obj)
        obj.insert(i, v)
        self._protocol.update(self._name, obj)

    def __str__(self):
        return str(self._obj)
