# message.py


class Message(object):
    def __init__(self, sender, receiver, proposal=None):
        self.sender = sender
        self.receiver = receiver
        self.proposal = proposal

    @classmethod
    def create(klass, sender=None, receiver=None, proposal=None):
        return klass(sender, receiver, proposal)


class Request(Message):
    pass


class Prepare(Message):
    pass


class Promise(Message):
    pass


class Accept(Message):
    pass


class Accepted(Message):
    pass


class Nack(Message):
    pass


class Response(Message):
    pass
