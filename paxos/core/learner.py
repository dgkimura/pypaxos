# learner.py
from paxos.core.role import Role
from paxos.net.message import Accepted, Response, Request, Sync, Synced
from paxos.net.proposal import Proposal, SYNC_PROPOSAL
from paxos.utils.ledger import Ledger, LedgerEntry
from paxos.utils.logger import LOG


class Learner(Role):
    SYNC_SIZE = 8

    def __init__(self, *args, ledger=None, **kwargs):
        super(Learner, self).__init__(*args, **kwargs)
        self.accepted_proposals = dict()

        self._ledger = ledger if ledger is not None else Ledger()

    @Role.receive.register(Accepted)
    @Role.update_proposal
    def _(self, message, channel, create_reply=Response.create):
        """Learn Phase.

        To learn that a value has been chosen, a learner must find out that a
        proposal has been accepted by a majority of acceptors.

        """
        LOG.debug("RECEIVED message {0}".format(message))
        self.accepted_proposals.setdefault(message.proposal, set()) \
            .add(message.sender)

        minimum_quorum = len(channel.replicas) // 2 + 1
        accepted_quorum = len(self.accepted_proposals.get(message.proposal))

        if accepted_quorum == minimum_quorum:
            # Here we reset for the next round.
            self.state.write(Role.PROPOSED, self.state.read(Role.PROPOSED) \
                .next())
            self.state.write(Role.VALUE, None)

            channel.unicast(Request.create(receiver=message.receiver,
                                           sender=message.receiver))
            self.notification.send(create_reply(proposal=message.proposal))

        if accepted_quorum >= minimum_quorum:
            self._ledger.append(LedgerEntry(number=message.proposal.number,
                                            value=message.value))
            reply = create_reply(proposal=message.proposal)
            channel.unicast(reply)

        if accepted_quorum == len(channel.replicas):
            del self.accepted_proposals[message.proposal]

    @Role.receive.register(Sync)
    def _(self, message, channel):
        """Handle request from out-of-sync replica""" 

        LOG.debug("RECEIVED message {0}".format(message))
        proposals = self._ledger.get_range(message.proposal)[:Learner.SYNC_SIZE]
        is_finished = proposals[-1] == self.state.read(Role.ACCEPTED)

        channel.unicast(Synced.create(receiver=message.sender,
                                      sender=message.receiver,
                                      proposal=proposals,
                                      finished=is_finished))

    @Role.receive.register(Synced)
    def _(self, message, channel):
        """Handle response for updating this replica"""

        LOG.debug("RECEIVED message {0}".format(message))
        synced_proposals = message.proposal
        self._ledger.extend(synced_proposals)

        current_proposal = Proposal("sync", synced_proposals[-1].number)
        next_proposal = Proposal("sync", synced_proposals[-1].number + 1)

        self.state.write(Role.PROPOSED, current_proposal)
        self.state.write(Role.PROMISED, current_proposal)
        self.state.write(Role.ACCEPTED, current_proposal)

        if not message.finished:
            channel.unicast(Sync.create(
                receiver=message.sender,
                sender=message.receiver,
                proposal=self.state.read(Role.ACCEPTED)))
        else:
            self.state.write(Role.PROPOSED, next_proposal)
            self.notification.send(Response.create(proposal=SYNC_PROPOSAL))
