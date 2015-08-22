from unittest import TestCase, main

from paxos.core.learner import Learner
from paxos.net.history_channel import HistoryChannel
from paxos.net.message import Accepted, Response
from paxos.net.proposal import Proposal

from tests.stubs import InMemoryState, NopLedger


class TestLearner(TestCase):
    def test_receive_accepted(self):
        channel = HistoryChannel(replicas=['A', 'B', 'C'])
        role = Learner(ledger=NopLedger(), state=InMemoryState())

        role.receive(Accepted.create(proposal=Proposal('A', 1), sender='A'), channel)
        role.receive(Accepted.create(proposal=Proposal('A', 1), sender='B'), channel)
        role.receive(Accepted.create(proposal=Proposal('A', 1), sender='C'), channel)

        self.assertTrue(type(channel.unicast_messages[0]) is Response)

    def test_receive_duplicate_accepted_proposals(self):
        channel = HistoryChannel(replicas=['A', 'B', 'C'])
        role = Learner(ledger=NopLedger(), state=InMemoryState())

        role.receive(Accepted.create(proposal=Proposal('A', 1), sender='A'), channel)
        role.receive(Accepted.create(proposal=Proposal('A', 1), sender='A'), channel)
        role.receive(Accepted.create(proposal=Proposal('A', 1), sender='A'), channel)

        self.assertFalse(channel.unicast_messages)


if __name__ == "__main__":
    main()
