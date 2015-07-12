from unittest import TestCase, main

from paxos.core.proposer import Proposer
from paxos.net.history_channel import HistoryChannel
from paxos.net.message import Request, Prepare, Promise, Accept, Accepted
from paxos.net.proposal import Proposal


class TestProposer(TestCase):
    def test_receive_request_sends_initial_proposal(self):
        channel = HistoryChannel()
        role = Proposer()

        role.receive(Request.create(), channel)

        sent_message = channel.broadcast_messages[-1]
        self.assertTrue(type(sent_message) is Prepare)
        self.assertEqual(sent_message.proposal.number, 1)

    def test_receive_request_sends_subsequent_proposal(self):
        channel = HistoryChannel()
        role = Proposer()

        role.receive(Request.create(), channel)
        role.receive(Request.create(), channel)
        role.receive(Request.create(), channel)

        sent_message = channel.broadcast_messages[-1]
        self.assertEqual(sent_message.proposal.number, 3)

    def test_receive_promise_reaches_quorum(self):
        channel = HistoryChannel(replicas=['A', 'B', 'C'])
        role = Proposer()

        role.receive(Promise.create(proposal=Proposal('A', 1), sender='A'), channel)
        role.receive(Promise.create(proposal=Proposal('A', 1), sender='B'), channel)
        role.receive(Promise.create(proposal=Proposal('A', 1), sender='C'), channel)

        self.assertTrue(type(channel.broadcast_messages[-1]) is Accept)

    def test_receive_promise_below_quorum(self):
        channel = HistoryChannel(replicas=['A', 'B', 'C'])
        role = Proposer()

        role.receive(Promise.create(proposal=Proposal('A', 1), sender='A'), channel)
        role.receive(Promise.create(proposal=Proposal('A', 1), sender='A'), channel)
        role.receive(Promise.create(proposal=Proposal('A', 1), sender='A'), channel)

        self.assertEqual(len(channel.broadcast_messages), 0)


if __name__ == "__main__":
    main()
