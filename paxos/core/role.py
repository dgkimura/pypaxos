from paxos.net.message import Sync
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
                latest_proposal = self.state.read(Role.PROPOSED)
                this_proposal = message.proposal

                if this_proposal.number == latest_proposal.number + 1:
                    self.state.write(Role.PROPOSED, this_proposal.next())

            if this_proposal.number > latest_proposal.number + 1:
                # we're behind and need to catch up
                channel.unicast(Sync.create(receiver=message.sender,
                                            proposal=latest_proposal))
            else:
                func(self, message, channel, **kw)
        return wrapper
