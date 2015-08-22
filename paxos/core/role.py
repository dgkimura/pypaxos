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
        self.state.set_default(Role.PROMISED, Proposal(author, 0))
        self.state.set_default(Role.ACCEPTED, Proposal(author, 0))
        self.state.set_default(Role.VALUE, "")

    @methoddispatch
    def receive(self, message, channel):
        error = "No function handles message: {0}.".format(message)
        raise NotImplementedError(error)
