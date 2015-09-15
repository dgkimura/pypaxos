# learner.py
from paxos.core.role import Role
from paxos.net.message import Accepted, Response, Request, Sync, Synced
from paxos.net.proposal import Proposal
from paxos.utils.ledger import Ledger, LedgerEntry


class Learner(Role):
    def __init__(self, *args, ledger=None, **kwargs):
        super(Learner, self).__init__(*args, **kwargs)
        self.accepted_proposals = dict()
        self._ledger = ledger or Ledger()

    @Role.receive.register(Accepted)
    @Role.update_proposal
    def _(self, message, channel, create_reply=Response.create):
        """Learn Phase.

        To learn that a value has been chosen, a learner must find out that a
        proposal has been accepted by a majority of acceptors.

        """
        print("RECEIVED message {0}".format(message))
        self.accepted_proposals.setdefault(message.proposal, set()) \
            .add(message.sender)

        minimum_quorum = len(channel.replicas) // 2 + 1
        accepted_quorum = len(self.accepted_proposals.get(message.proposal))

        if accepted_quorum >= minimum_quorum:
            self._ledger.append(LedgerEntry(number=message.proposal.number,
                                            value=message.value))
            reply = create_reply(proposal=message.proposal)
            channel.unicast(reply)

        if accepted_quorum == minimum_quorum:
            # Here we reset for the next round.
            with self.state.lock():
                self.state.write(Role.PROPOSED,
                                 self.state.read(Role.PROPOSED).next())
            self.state.write(Role.VALUE, None)

            channel.unicast(Request.create(receiver=message.receiver,
                                           sender=message.receiver))

        if accepted_quorum == len(channel.replicas):
            del self.accepted_proposals[message.proposal]

    @Role.receive.register(Sync)
    def _(self, message, channel):
        """
        """
        with self._ledger.lock():
            sync_proposals = self._ledger.get_range(message.proposal, None)
            channel.unicast(Synced.create(receiver=message.sender,
                                          sender=message.receiver,
                                          proposal=sync_proposals))

    @Role.receive.register(Synced)
    def _(self, message, channel):
        """
        """
        synced_proposals = message.proposal
        with self._ledger.lock():
            self._ledger.extend(synced_proposals)

        with self.state.lock():
            self.state.write(Role.PROPOSED,
                             Proposal("sync", message.proposal[-1]))
