# learner.py


class Learner(Role):
    def __init__(self, channel):
        self._channel = channel

    @receive.register(Accepted)
    def _(self, message):
        reply = Response()
        self._channel.unicast(reply)
