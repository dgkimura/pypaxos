from unittest import TestCase, main

from paxos.core.learner import Learner
from paxos.core.role import Role
from paxos.net.history_channel import HistoryChannel
from paxos.net.message import Accepted, Response
from paxos.net.proposal import Proposal
from paxos.utils.state import State

from tests.stubs import InMemoryStorage, NopLedger


class TestLearner(TestCase):
    def setUp(self):
        self.channel = HistoryChannel(replicas=['A', 'B', 'C'])
        self.state = State(storage=InMemoryStorage("fakefile"))
        self.role = Learner(ledger=NopLedger(), state=self.state)

    def test_learner_receives_quorum_of_accepteds(self):
        self.role.receive(Accepted.create(proposal=Proposal('A', 1), sender='A'), self.channel)
        self.role.receive(Accepted.create(proposal=Proposal('A', 1), sender='B'), self.channel)
        self.role.receive(Accepted.create(proposal=Proposal('A', 1), sender='C'), self.channel)

        self.assertTrue(type(self.channel.unicast_messages[0]) is Response)

    def test_learner_receives_quorum_of_accepteds_causes_proposal_to_increment(self):
        self.role.receive(Accepted.create(proposal=Proposal('A', 1), sender='A'), self.channel)
        self.role.receive(Accepted.create(proposal=Proposal('A', 1), sender='B'), self.channel)
        self.role.receive(Accepted.create(proposal=Proposal('A', 1), sender='C'), self.channel)

        self.assertTrue(self.state.read(Role.PROPOSED), Proposal('A', 2))


    def test_learner_ignores_duplicate_accepteds(self):
        self.role.receive(Accepted.create(proposal=Proposal('A', 1), sender='A'), self.channel)
        self.role.receive(Accepted.create(proposal=Proposal('A', 1), sender='A'), self.channel)
        self.role.receive(Accepted.create(proposal=Proposal('A', 1), sender='A'), self.channel)

        self.assertFalse(self.channel.unicast_messages)


if __name__ == "__main__":
    main()
