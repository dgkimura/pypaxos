# channel.py


import cPickle as pickle
from paxos.net.socket import Socket


class Channel(object):
    def __init__(self, host, replicas, socket=None):
        self.host = host
        self.replicas = replicas
        self.socket = socket or Socket()

    def unicast(self, message):
        self.socket.send(message.receiver,
                         pickle.dumps(message))

    def broadcast(self, message):
        for r in self.replicas:
            self.socket.send(r,
                             pickle.dumps(message))

    def listen(self):
        self.socket.receiver(self.host)

        # TODO: send message to paxos node
