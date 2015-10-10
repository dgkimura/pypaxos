class Number(object):
    def __init__(self, name, obj, protocol):
        self._obj = obj
        self._name = name
        self._protocol = protocol

    def __add__(self, other):
        self._protocol.sync(self._name)
        return self._obj + other

    def __sub__(self, other):
        self._protocol.sync(self._name)
        return self._obj - other

    def __mul__(self, other):
        self._protocol.sync(self._name)
        return self._obj * other

    def __mod__(self, other):
        self._protocol.sync(self._name)
        return self._obj % other

    def __str__(self):
        return str(self._obj)
