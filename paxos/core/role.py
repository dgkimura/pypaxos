from paxos.net.proposal import Proposal
from paxos.utils.decorators import methoddispatch


class Role(object):
    def __init__(self, author="anonymous"):
        self._current_proposal = Proposal(author, 0)

    @methoddispatch
    def receive(self, message, channel):
        error = "No function handles message: {0}.".format(message)
        raise NotImplementedError(error)

    @property
    def next_proposal(self):
        author, number = self._current_proposal
        self._current_proposal = Proposal(author, number + 1)
        return self._current_proposal
