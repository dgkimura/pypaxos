# message.py


class Message(object):
    def __init__(self, sender, receiver, proposal=None,
                 accepted_proposal=None, value=None):
        self.sender = sender
        self.receiver = receiver
        self.proposal = proposal
        self.accepted_proposal = accepted_proposal
        self.value = value

    @classmethod
    def create(klass, sender=None, receiver=None, proposal=None,
               accepted_proposal=None, value=None):
        return klass(sender, receiver, proposal, accepted_proposal, value)


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
