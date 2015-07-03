# acceptor.py
from paxos.core.role import Role
from paxos.net.message import Prepare, Accept


class Acceptor(Role):
    def __init__(self, channel):
        self._channel = channel
        self._proposal_id

    @Role.receive.register(Prepare)
    def _(self, message):
        reply = Promise()
        self._channel.unicast(reply)

    @Role.receive.register(Accept)
    def _(self, message):
        reply = Accepted()
        self._channel.broadcast(reply)
