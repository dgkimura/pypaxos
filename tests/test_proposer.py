from unittest import TestCase, main

from paxos.core.proposer import Proposer
from paxos.core.role import Role
from paxos.net.history_channel import HistoryChannel
from paxos.net.message import Request, Prepare, Promise, Accept, Accepted
from paxos.net.proposal import Proposal
from paxos.utils.state import State

from tests.stubs import InMemoryStorage


class TestProposer(TestCase):
    def setUp(self):
        self.channel = HistoryChannel(replicas=['A', 'B', 'C'])
        self.state = State(storage=InMemoryStorage("fakefile"))
        self.role = Proposer(state=self.state)

    def test_proposer_doesnt_send_prepare_if_no_value_in_request(self):
        self.role.receive(Request.create(), self.channel)
        self.assertEqual(len(self.channel.broadcast_messages), 0)

    def test_prposer_sends_initial_prepare(self):
        self.role.receive(Request.create(value="myval"), self.channel)

        sent_message = self.channel.broadcast_messages[-1]
        self.assertTrue(type(sent_message) is Prepare)
        self.assertEqual(sent_message.proposal.number, 0)

    def test_proposer_uses_one_proposal_at_a_time(self):
        self.role.receive(Request.create(value="myval_1"), self.channel)
        self.role.receive(Request.create(value="myval_2"), self.channel)
        self.role.receive(Request.create(value="myval_3"), self.channel)

        sent_message = self.channel.broadcast_messages[-1]
        self.assertEqual(sent_message.proposal.number, 0)

    def test_proposer_receives_quorum_of_promises(self):
        self.role.receive(Promise.create(proposal=Proposal('A', 1), sender='A'), self.channel)
        self.role.receive(Promise.create(proposal=Proposal('A', 1), sender='B'), self.channel)
        self.role.receive(Promise.create(proposal=Proposal('A', 1), sender='C'), self.channel)

        self.assertTrue(type(self.channel.broadcast_messages[-1]) is Accept)

    def test_proposer_doesnt_receive_quorum_or_promises(self):
        self.role.receive(Promise.create(proposal=Proposal('A', 1), sender='A'), self.channel)

        self.assertEqual(len(self.channel.broadcast_messages), 0)

    def test_proposer_ignores_duplicate_promises(self):
        self.role.receive(Promise.create(proposal=Proposal('A', 1), sender='A'), self.channel)
        self.role.receive(Promise.create(proposal=Proposal('A', 1), sender='A'), self.channel)
        self.role.receive(Promise.create(proposal=Proposal('A', 1), sender='A'), self.channel)

        self.assertEqual(len(self.channel.broadcast_messages), 0)

    def test_proposer_ignores_decending_promise(self):
        self.role.receive(Promise.create(proposal=Proposal('A', 1), sender='A', value="a_1"), self.channel)
        self.role.receive(Promise.create(proposal=Proposal('A', 1), sender='B', value="a_1"), self.channel)

        self.assertEqual(self.role.highest_proposal, Proposal('A', 1))
        self.role.receive(Promise.create(proposal=Proposal('A', 0), sender='A', value="a_0"), self.channel)

        self.assertEqual(self.role.highest_proposal, Proposal('A', 1))
        self.assertEqual(self.channel.broadcast_messages[-1].value, "a_1")


if __name__ == "__main__":
    main()
