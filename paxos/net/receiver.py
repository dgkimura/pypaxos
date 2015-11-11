import asyncio
from asyncio import Protocol
from threading import Thread


try:
    import cPickle as pickle
except ImportError:
    import pickle


class ReceiverProtocol(Protocol):
    def __init__(self, channel, loop, serializer=pickle):
        self.channel = channel
        self.loop = loop
        self.serializer = serializer

    def connection_made(self, transport):
        self.transport = transport

    def data_received(self, data):
        message = self.serializer.loads(data)
        self.channel.unicast(message)


class Receiver(object):
    __DEFAULT_PORT = 8081

    def __init__(self, ip, channel):
        ip_parts = ip.split(":")

        self.ip = ip_parts[0]
        self.port = len(ip_parts) > 1 and ip_parts[1] or Receiver.__DEFAULT_PORT
        self.channel = channel

    def start(self):
        t = Thread(target=self._start)
        t.start()

    def _start(self):
        self.loop = asyncio.new_event_loop()
        asyncio.set_event_loop(self.loop)
        coro = self.loop.create_server(
            lambda: ReceiverProtocol(self.channel, self.loop),
            self.ip, self.port)
        self.loop.run_until_complete(coro)
        self.loop.run_forever()
