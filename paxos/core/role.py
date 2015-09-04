from paxos.net.proposal import Proposal
from paxos.utils.decorators import methoddispatch
from paxos.utils.persistedstate import PersistedState


class Role(object):
    PROPOSED = "proposed.proposal"
    PROMISED = "promised.proposal"
    ACCEPTED = "accepted.proposal"
    VALUE = "value.str"

    def __init__(self, state=None, author=None):
        self.state = state or PersistedState("pypaxos.state")
        self.state.set_default(Role.PROPOSED, Proposal(author, 0))
        self.state.set_default(Role.PROMISED, Proposal(author, -1))
        self.state.set_default(Role.ACCEPTED, Proposal(author, -1))
        self.state.set_default(Role.VALUE, "")

        # List of values to be associated with proposal
        self.requested_values = []

        # List of proposals in progress
        self.pending_proposals = []

    @methoddispatch
    def receive(self, message, channel):
        error = "No function handles message: {0}.".format(message)
        raise NotImplementedError(error)


    @staticmethod
    def update_proposal(func):
        def wrapper(self, message, channel, **kw):
            with self.state.lock():
                if message.proposal > self.state.read(Role.PROPOSED):
                    self.state.write(Role.PROPOSED, message.proposal.next())
            func(self, message, channel, **kw)
        return wrapper
