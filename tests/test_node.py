from unittest import TestCase, main

from paxos.core.node import Node
from paxos.net.history_channel import HistoryChannel
from paxos.net.message import Request, Prepare, Promise, Accept, Accepted
from paxos.net.proposal import Proposal

from tests.stubs import InMemoryState, NopLedger


class TestNode(TestCase):
    def test_receive_updates_highest_proposal(self):
        channel = HistoryChannel()
        postit = InMemoryState()
        role = Node(ledger=NopLedger(), state=postit)

        self.assertEqual(postit.read(Node.PROPOSED), Proposal(None, 0))

        role.receive(Prepare.create(proposal=Proposal('A', 1)), channel)
        self.assertEqual(postit.read(Node.PROPOSED), Proposal('A', 1))

        role.receive(Promise.create(proposal=Proposal('A', 2)), channel)
        self.assertEqual(postit.read(Node.PROPOSED), Proposal('A', 2))

        role.receive(Accept.create(proposal=Proposal('A', 3)), channel)
        self.assertEqual(postit.read(Node.PROPOSED), Proposal('A', 3))

        role.receive(Accepted.create(proposal=Proposal('A', 4)), channel)
        self.assertEqual(postit.read(Node.PROPOSED), Proposal('A', 4))


if __name__ == "__main__":
    main()