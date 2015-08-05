# learner.py
from paxos.core.role import Role
from paxos.net.message import Accepted, Response
from paxos.utils.ledger import Ledger


class Learner(Role):
    def __init__(self, *args, ledger=None, **kwargs):
        super(Learner, self).__init__(*args, **kwargs)
        self.accepted_proposals = dict()
        self._ledger = ledger or Ledger()

    @Role.receive.register(Accepted)
    def _(self, message, channel, create_reply=Response.create):
        """Learn Phase.

        To learn that a value has been chosen, a learner must find out that a
        proposal has been accepted by a majority of acceptors.

        """
        print("RECEIVED message {0}".format(message))
        self.accepted_proposals.setdefault(message.proposal, set()) \
            .add(message.sender)

        minimum_quorum = len(channel.replicas) // 2 + 1
        accepted_proposals = len(self.accepted_proposals.get(message.proposal))

        if accepted_proposals >= minimum_quorum:
            self._ledger.append(message.value)
            reply = create_reply()
            channel.unicast(reply)
