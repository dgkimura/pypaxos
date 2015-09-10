from unittest import TestCase, main

from paxos.core.proposer import Proposer
from paxos.core.role import Role
from paxos.net.history_channel import HistoryChannel
from paxos.net.message import Request, Prepare, Promise, Accept, Accepted
from paxos.net.proposal import Proposal

from tests.stubs import InMemoryState


class TestProposer(TestCase):
    def test_receive_request_without_value(self):
        channel = HistoryChannel()
        role = Proposer(state=InMemoryState())

        role.receive(Request.create(), channel)
        self.assertEqual(len(channel.broadcast_messages), 0)

    def test_receive_request_sends_initial_proposal(self):
        channel = HistoryChannel()
        role = Proposer(state=InMemoryState())

        role.receive(Request.create(value="myval"), channel)

        sent_message = channel.broadcast_messages[-1]
        self.assertTrue(type(sent_message) is Prepare)
        self.assertEqual(sent_message.proposal.number, 0)

    def test_receive_request_sends_subsequent_proposal(self):
        channel = HistoryChannel()
        role = Proposer(state=InMemoryState())

        role.receive(Request.create(value="myval"), channel)
        role.receive(Request.create(value="myval"), channel)
        role.receive(Request.create(value="myval"), channel)

        sent_message = channel.broadcast_messages[-1]
        self.assertEqual(sent_message.proposal.number, 0)

    def test_receive_promise_reaches_quorum(self):
        channel = HistoryChannel(replicas=['A', 'B', 'C'])
        role = Proposer(state=InMemoryState())

        role.receive(Promise.create(proposal=Proposal('A', 1), sender='A'), channel)
        role.receive(Promise.create(proposal=Proposal('A', 1), sender='B'), channel)
        role.receive(Promise.create(proposal=Proposal('A', 1), sender='C'), channel)

        self.assertTrue(type(channel.broadcast_messages[-1]) is Accept)

    def test_receive_promise_below_quorum(self):
        channel = HistoryChannel(replicas=['A', 'B', 'C'])
        role = Proposer(state=InMemoryState())

        role.receive(Promise.create(proposal=Proposal('A', 1), sender='A'), channel)

        self.assertEqual(len(channel.broadcast_messages), 0)

    def test_receive_promise_ignores_duplicates(self):
        channel = HistoryChannel(replicas=['A', 'B', 'C'])
        role = Proposer(state=InMemoryState())

        role.receive(Promise.create(proposal=Proposal('A', 1), sender='A'), channel)
        role.receive(Promise.create(proposal=Proposal('A', 1), sender='A'), channel)
        role.receive(Promise.create(proposal=Proposal('A', 1), sender='A'), channel)

        self.assertEqual(len(channel.broadcast_messages), 0)

        role.receive(Promise.create(proposal=Proposal('A', 1), sender='B'), channel)

        self.assertTrue(type(channel.broadcast_messages[-1]) is Accept)

    def test_receive_promise_ignores_descending_proposal(self):
        channel = HistoryChannel(replicas=['A'])
        state = InMemoryState()
        role = Proposer(state=state)

        role.receive(Promise.create(proposal=Proposal('A', 1), sender='A', value="a_1"), channel)
        self.assertEqual(role.highest_proposal, Proposal('A', 1))
        role.receive(Promise.create(proposal=Proposal('A', 0), sender='A', value="a_0"), channel)

        self.assertEqual(role.highest_proposal, Proposal('A', 1))
        self.assertEqual(channel.broadcast_messages[-1].value, "a_1")


if __name__ == "__main__":
    main()
