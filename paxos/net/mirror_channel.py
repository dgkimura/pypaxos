# mirror_channel.py


class MirrorChannel(object):
    def __init__(self, replicas=None):
        self._listeners = []
        self.replicas = replicas or []

    def unicast(self, message):
        for l in self._listeners:
            l.receive(message, self)

    def broadcast(self, message):
        for l in self._listeners:
            l.receive(message, self)

    def loopback(self, message):
        for l in self._listeners:
            l.receive(message, self)

    def connect(self, listener):
        self._listeners.append(listener)
