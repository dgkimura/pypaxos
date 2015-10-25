from yaml import dump

from paxos.app.adapter import Adapter
from paxos.net.channel import Channel
from paxos.net.message import Request


class Protocol(object):
    def __init__(self, channel=None, adapter=None, serializer=dump):
        self._serialize = serializer
        self._channel = channel if channel is not None else Channel()
        self._adapter = adapter if adapter is not None else  Adapter()

    def sync(self, name):
        val = "READ({0})".format(name)
        self._channel.loopback(Request.create(value=val))

    def update(self, name, obj):
        val = "{0}={1}".format(name, repr(self._serialize(obj)))
        self._channel.loopback(Request.create(value=val))

    def get(self, name):
        return self._adapter.read(name)
