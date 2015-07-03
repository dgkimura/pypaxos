# proposer.py
from paxos.core.role import Role
from paxos.net.message import Request, Promise, Accepted


class Proposer(Role):
    def __init__(self, channel):
        self._channel = channel
        self._proposal_id

    @Role.receive.register(Request)
    def _(self, message):
        reply = Prepare()
        self._channel.broadcast(reply)

    @Role.receive.register(Promise)
    def _(self, message):
        reply = Accept()
        self._channel.broadcast(reply)

    @Role.receive.register(Accepted)
    def _(self, message):
        pass
