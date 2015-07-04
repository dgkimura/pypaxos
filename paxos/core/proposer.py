# proposer.py
from functools import singledispatch

from paxos.core.role import Role
from paxos.net.message import Request, Prepare, Promise, Accept, Accepted


class Proposer(Role):
    def __init__(self, channel):
        self._channel = channel

    @Role.receive.register(Request)
    def _(self, message):
        reply = Prepare.create(sender=message.receiver)
        self._channel.broadcast(reply)

    @Role.receive.register(Promise)
    def _(self, message):
        reply = Accept.create(sender=message.receiver)
        self._channel.broadcast(reply)

    #@Role.receive.register(Accepted)
    #def _(self, message):
    #    pass
