from unittest import TestCase, main

from paxos.core.node import Node
from paxos.net.history_channel import HistoryChannel
from paxos.net.message import Request, Prepare, Promise, Accept, Accepted, Sync
from paxos.net.proposal import Proposal

from tests.stubs import InMemoryState, NopLedger


class TestNode(TestCase):
    def test_receive_updates_highest_proposal(self):
        channel = HistoryChannel(replicas=['A', 'B', 'C'])
        postit = InMemoryState()
        role = Node(ledger=NopLedger(), state=postit)

        self.assertEqual(postit.read(Node.PROPOSED), Proposal(None, 0))

        role.receive(Prepare.create(proposal=Proposal('A', 1)), channel)
        self.assertEqual(postit.read(Node.PROPOSED), Proposal('A', 2))

        role.receive(Promise.create(proposal=Proposal('A', 3)), channel)
        self.assertEqual(postit.read(Node.PROPOSED), Proposal('A', 4))

        role.receive(Accept.create(proposal=Proposal('A', 5)), channel)
        self.assertEqual(postit.read(Node.PROPOSED), Proposal('A', 6))

        role.receive(Accepted.create(proposal=Proposal('A', 7)), channel)
        self.assertEqual(postit.read(Node.PROPOSED), Proposal('A', 8))

    def test_role_behind_sends_sync_message(self):
        channel = HistoryChannel()
        postit = InMemoryState()
        role = Node(ledger=NopLedger(), state=postit)

        role.receive(Prepare.create(proposal=Proposal('A', 2)), channel)

        self.assertTrue(type(channel.unicast_messages[-1]) is Sync)


if __name__ == "__main__":
    main()
