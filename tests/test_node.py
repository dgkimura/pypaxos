from unittest import TestCase, main

from paxos.core.node import Node
from paxos.net.history_channel import HistoryChannel
from paxos.net.message import Request, Prepare, Promise, Accept, Accepted, Sync
from paxos.net.proposal import Proposal
from paxos.utils.ledger import Ledger
from paxos.utils.state import State

from tests.stubs import InMemoryStorage


class TestNode(TestCase):
    def setUp(self):
        self.channel = HistoryChannel(replicas=['A', 'B', 'C'])
        self.state = State(storage=InMemoryStorage("fakefile"))
        self.ledger = Ledger(storage=InMemoryStorage("fakefile2"))
        self.role = Node(ledger=self.ledger, state=self.state)

    def test_node_receives_higher_proposals(self):
        self.assertEqual(self.state.read(Node.PROPOSED), Proposal(None, 0))

        self.role.receive(Prepare.create(proposal=Proposal('A', 1)), self.channel)
        self.assertEqual(self.state.read(Node.PROPOSED), Proposal('A', 2))

        self.role.receive(Promise.create(proposal=Proposal('A', 3)), self.channel)
        self.assertEqual(self.state.read(Node.PROPOSED), Proposal('A', 4))

        self.role.receive(Accept.create(proposal=Proposal('A', 5)), self.channel)
        self.assertEqual(self.state.read(Node.PROPOSED), Proposal('A', 6))

        self.role.receive(Accepted.create(proposal=Proposal('A', 7)), self.channel)
        self.assertEqual(self.state.read(Node.PROPOSED), Proposal('A', 8))

    def test_role_behind_sends_sync_message(self):
        self.role.receive(Prepare.create(proposal=Proposal('A', 2)), self.channel)

        self.assertTrue(type(self.channel.unicast_messages[-1]) is Sync)


if __name__ == "__main__":
    main()
