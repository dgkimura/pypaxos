from unittest import TestCase, main

from paxos.core.acceptor import Acceptor
from paxos.net.history_channel import HistoryChannel
from paxos.net.message import Prepare, Promise, Accept, Nack, Accepted
from paxos.net.proposal import Proposal
from paxos.utils.state import State

from tests.stubs import InMemoryStorage


class TestAcceptor(TestCase):
    def setUp(self):
        self.channel = HistoryChannel()
        self.state = State(storage=InMemoryStorage("fakefile"))
        self.role = Acceptor(state=self.state)

    def test_acceptor_receives_higher_prepare(self):
        self.role.receive(Prepare.create(proposal=Proposal('A', 1)), self.channel)
        self.role.receive(Prepare.create(proposal=Proposal('A', 2)), self.channel)

        self.assertEqual(len(self.channel.unicast_messages), 2)
        self.assertEqual(self.state.read(Acceptor.PROMISED), Proposal('A', 2))
        self.assertTrue(type(self.channel.unicast_messages[-1]) is Promise)

    def test_acceptor_receives_lower_prepare(self):
        self.role.receive(Prepare.create(proposal=Proposal('A', 1)), self.channel)
        self.role.receive(Prepare.create(proposal=Proposal('A', 0)), self.channel)

        self.assertEqual(len(self.channel.unicast_messages), 2)
        self.assertEqual(self.state.read(Acceptor.PROMISED), Proposal('A', 1))
        self.assertTrue(type(self.channel.unicast_messages[-1]) is Nack)

    def test_acceptor_receives_lower_prepare_and_then_receives_accept(self):
        self.role.receive(Prepare.create(proposal=Proposal('A', 1)), self.channel)
        self.role.receive(Prepare.create(proposal=Proposal('A', 0)), self.channel)
        self.role.receive(Accept.create(proposal=Proposal('A', 1)), self.channel)

        self.assertTrue(type(self.channel.broadcast_messages[0]) is Accepted)

    def test_acceptor_receives_prepare_and_then_receives_lower_accept(self):
        self.role.receive(Prepare.create(proposal=Proposal('A', 1)), self.channel)
        self.role.receive(Accept.create(proposal=Proposal('A', 0)), self.channel)

        self.assertTrue(type(self.channel.unicast_messages[-1]) is Nack)


if __name__ == "__main__":
    main()
