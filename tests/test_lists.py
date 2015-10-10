from unittest import TestCase, main

from paxos.app.adapter import Adapter
from paxos.app.protocol import Protocol
from paxos.app.store import Store
from paxos.app.types.lists import List
from paxos.core.node import Node
from paxos.net.mirror_channel import MirrorChannel
from paxos.utils.ledger import Ledger
from paxos.utils.state import State

from tests.stubs import InMemoryStorage


class TestLists(TestCase):
    def setUp(self):
        ledger = Ledger(storage=InMemoryStorage("fakefile_ledger"))
        state = State(storage=InMemoryStorage("fakefile_storage"))
        channel = MirrorChannel()
        channel.connect(Node(ledger=ledger, state=state))

        self.protocol = Protocol(channel, Adapter(ledger))

    def test_create_nonempty_list(self):
        a_list = List("a_list", ["Mickey", "Minnie"], self.protocol)
        self.assertEqual(len(a_list), 2)

    def test_append_item_to_list(self):
        a_list = List("a_list", [], self.protocol)
        a_list.append("Goofy")
        self.assertEqual(a_list[0], "Goofy")

    def test_delete_item_from_list(self):
        a_list = List("a_list", ["Mickey", "Minnie"], self.protocol)
        a_list.remove("Mickey")
        self.assertEqual(len(a_list), 1)

    def test_set_item_in_list(self):
        a_list = List("a_list", ["Mickey", "Minnie"], self.protocol)
        a_list[1] = "Minnie Mouse"
        self.assertEqual(a_list[1], "Minnie Mouse")


if __name__ == "__main__":
    main()
