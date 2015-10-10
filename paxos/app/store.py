from paxos.app.adapter import Adapter
from paxos.app.factory import Factory
from paxos.app.protocol import Protocol
from paxos.core.node import Node
from paxos.net.channel import Channel


class Store(object):
    def __init__(self, adapter=None, channel=None):
        self.__dict__['adapter'] = adapter or Adapter()
        self.__dict__['channel'] = channel or Channel()
        self.__dict__['protocol'] = Protocol(self.channel)
        self.__dict__['factory'] = Factory(self.protocol)
        self.channel.connect(Node())

    def __getattr__(self, attribute):
        self.protocol.sync(attribute)
        raw_obj = self.adapter.read(attribute)
        obj = self.factory.create(raw_obj, attribute)
        return obj

    def __setattr__(self, name, value):
        self.protocol.update(name, value)
