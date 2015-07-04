# acceptor.py
from paxos.core.role import Role
from paxos.net.message import Prepare, Promise, Accept, Accepted


class Acceptor(Role):
    def __init__(self, channel):
        self._channel = channel

    @Role.receive.register(Prepare)
    def _(self, message):
        reply = Promise.create(sender=message.receiver, receiver=message.sender)
        self._channel.unicast(reply)

    @Role.receive.register(Accept)
    def _(self, message):
        reply = Accepted.create(sender=message.receiver)
        self._channel.broadcast(reply)
