# channel.py
from paxos.net.socket import Socket


class Channel(object):
    def __init__(self, host, replicas, socket=None):
        self.host = host
        self.replicas = replicas
        self.socket = socket or Socket()

    def unicast(self, message):
        self.socket.send(message.receiver, message)

    def broadcast(self, message):
        for r in self.replicas:
            self.socket.send(r, message)

    def listen(self):
        return self.socket.receive(self.host)
