# message.py
from paxos.config.configuration import ADDRESS
from paxos.net.proposal import default_proposal


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
        accepted_proposal = accepted_proposal or default_proposal()
        sender = sender or ADDRESS
        receiver = receiver or ADDRESS
        return klass(sender, receiver, proposal, accepted_proposal, value)

    def __str__(self):
        return "[{0}] src:{1} \tdst:{2} \tproposal:{3} \tvalue:{4}".format(
                self.__class__.__name__, self.sender, self.receiver, self.proposal, self.value)


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


class Sync(Message):
    pass


class Synced(Message):
    @classmethod
    def create(klass, finished=True, **kwargs):
        obj = super(Synced, klass).create(**kwargs)
        obj.finished = finished
        return obj
