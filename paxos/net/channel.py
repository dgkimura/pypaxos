# channel.py
from threading import Thread

from paxos.config.configuration import settings, ADDRESS_OF_REPLICAS
from paxos.net.socket import Socket


class Channel(object):
    def __init__(self, socket=None):
        self.socket = socket or Socket()
        self.replicas = settings[ADDRESS_OF_REPLICAS]
        self.listeners = []

    def unicast(self, message):
        self.socket.send(message.receiver, message)

    def loopback(self, message):
        for l in self.listeners:
            l.receive(message, self, async=False)

    def broadcast(self, message):
        for r in self.replicas:
            message.receiver = r
            self.socket.send(r, message)

    def connect(self, listener):
        """Connect listener to this Channel.
        
        When connected, messages sent to this channel will be routed using the
        listener's receive method. Socket receive is a blocking call.

        """
        self.listeners.append(listener)
        t = Thread(target=self.socket.receive, args=(listener, self))
        t.daemon = True
        t.start()
