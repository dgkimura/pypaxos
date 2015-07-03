# proposer.py
from paxos.core import baserole


class Proposer(BaseRole):
    def __init__(self, channel):
        self._channel = channel
        self._proposal_id

    @receive.register(Request)
    def _(self, message):
        reply = Prepare()
        self._channel.broadcast(reply)

    @receive.register(Promise)
    def _(self, message):
        reply = Accept()
        self._channel.broadcast(reply)

    @receive.register(Accepted)
    def _(self, message):
        pass
