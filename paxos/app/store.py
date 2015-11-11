from paxos.app.adapter import Adapter
from paxos.app.factory import Factory
from paxos.app.protocol import Protocol
from paxos.net.channel import Channel


class Store(object):
    def __init__(self, adapter=None, channel=None):
        self.__dict__['adapter'] = adapter if adapter is not None else Adapter()
        self.__dict__['channel'] = channel if channel is not None else Channel()
        self.__dict__['protocol'] = Protocol(self.channel)
        self.__dict__['factory'] = Factory(self.protocol)

    def __getattr__(self, attribute):
        raw_obj = self.adapter.read(attribute)
        obj = self.factory.create(raw_obj, attribute)
        return obj

    def __setattr__(self, name, value):
        self.protocol.update(name, value)
