from paxos.net.proposal import Proposal
from paxos.utils.decorators import methoddispatch


class Role(object):
    def __init__(self, author="anonymous"):
        self.current_proposal = Proposal(author, 0)

        self.prepared_proposal = Proposal(author, 0)
        self.accepted_proposal = Proposal(author, 0)

        self.received_promises = dict()

    @methoddispatch
    def receive(self, message, channel):
        error = "No function handles message: {0}.".format(message)
        raise NotImplementedError(error)

    @property
    def next_proposal(self):
        author, number = self.current_proposal
        self.current_proposal = Proposal(author, number + 1)
        return self.current_proposal
