# message.py
from paxos.config.configuration import settings, ADDRESS
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
        sender = sender or settings[ADDRESS]
        receiver = receiver or settings[ADDRESS]
        return klass(sender, receiver, proposal, accepted_proposal, value)

    def __str__(self):
        return "{0}: \tproposal:{1} \tvalue:{2}".format(
                self.__class__, self.proposal, self.value)


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
    pass
