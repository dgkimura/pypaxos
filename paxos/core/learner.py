# learner.py
from paxos.core.role import Role
from paxos.net.message import Accepted, Response


class Learner(Role):
    def __init__(self, channel):
        self._channel = channel

    @Role.receive.register(Accepted)
    def _(self, message):
        reply = Response.create()
        self._channel.unicast(reply)
