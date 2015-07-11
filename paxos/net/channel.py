# channel.py
from threading import Thread

from paxos.net.socket import Socket


class Channel(object):
    def __init__(self, replicas, socket=None):
        self.replicas = replicas
        self.socket = socket or Socket()

    def unicast(self, message):
        self.socket.send(message.receiver, message)

    def broadcast(self, message):
        for r in self.replicas:
            message.receiver = r
            self.socket.send(r, message)

    def connect(self, listener):
        """Connect listener to this Channel.
        
        When connected, messages sent to this channel will be routed using the
        listener's receive method. Socket receive is a blocking call.

        """
        t = Thread(target=self.socket.receive, args=(listener, self))
        t.daemon = True
        t.start()
