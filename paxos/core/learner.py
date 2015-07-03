# learner.py


class Learner(BaseRole):
    def __init__(self, channel):
        self._channel = channel

    @receive.register(Accepted)
    def _(self, message):
        reply = Response()
        self._channel.unicast(reply)
