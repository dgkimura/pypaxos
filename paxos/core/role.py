from paxos.net.proposal import Proposal
from paxos.utils.decorators import methoddispatch


class Role(object):
    def __init__(self, author="anonymous"):
        self.current_proposal = Proposal(author, 0)
        self.last_proposal = Proposal(author, -1)

    @methoddispatch
    def receive(self, message, channel):
        error = "No function handles message: {0}.".format(message)
        raise NotImplementedError(error)
