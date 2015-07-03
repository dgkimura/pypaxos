# acceptor.py


class Acceptor(Role):
    def __init__(self, channel):
        self._channel = channel
        self._proposal_id

    @receive.register(Prepare)
    def _(self, message):
        reply = Promise()
        self._channel.unicast(reply)

    @receive.register(Accept)
    def _(self, message):
        reply = Accepted()
        self._channel.broadcast(reply)
