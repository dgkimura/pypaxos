# channel.py
from paxos.config.configuration import ADDRESS, ADDRESS_OF_REPLICAS
from paxos.core.node import Node
from paxos.net.receiver import Receiver
from paxos.net.endpoint import Remote, Local


class Channel(object):
    """Channel allows roles to communicate through messages.

    Outgoing messages are sent to roles through remote and local endpoints.
    Incoming messages are caught by the receiver and sent to local endpoints.

    """

    def __init__(self, replicas=None, receiver=None):
        self.receiver = receiver
        self.replicas = replicas

        if receiver is None:
            self.receiver = Receiver(ADDRESS, self)
        if replicas is None:
            self.replicas = dict((ip, Remote(ip)) for ip in ADDRESS_OF_REPLICAS)
            self.replicas[ADDRESS] = Local(Node(author=ADDRESS), self)

        self.receiver.start()

    def unicast(self, message):
        self.replicas[message.receiver].send(message)

    def loopback(self, message):
        self.replicas[ADDRESS].send(message)

    def broadcast(self, message):
        for ip, replica in self.replicas.items():
            message.receiver = ip
            replica.send(message)
