import asyncio
from asyncio import Protocol

from paxos.utils.logger import LOG


try:
    import cPickle as pickle
except ImportError:
    import pickle


class Endpoint(object):
    def send(self, message):
        raise NotImplemented()


class RemoteProtocol(Protocol):
    def __init__(self, message, loop, serializer=pickle):
        self.message = message
        self.loop = loop
        self.serializer = serializer

    def connection_made(self, transport):
        transport.write(self.serializer.dumps(self.message))

    def connection_lost(self, exc):
        self.loop.stop()


class Remote(Endpoint):
    __DEFAULT_PORT = 8081

    def __init__(self, ip):
        ip_parts = ip.split(":")

        self.ip = ip_parts[0]
        self.port = len(ip_parts) > 1 and ip_parts[1] or Remote.__DEFAULT_PORT

    def send(self, message):
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        coro = loop.create_connection(lambda: RemoteProtocol(message, loop),
                                      self.ip, self.port)
        try:
            loop.run_until_complete(coro)
        except ConnectionRefusedError as e:
            LOG.debug("I/O send error({0}: {1}".format(message.receiver,
                                                       e.strerror))
            pass
        loop.close()


class Local(Endpoint):
    def __init__(self, node, channel):
        self.node = node
        self.channel = channel

    def send(self, message):
        self.node.receive(message, self.channel)
