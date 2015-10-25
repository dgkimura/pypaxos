from unittest import TestCase, main

from paxos.core.learner import Learner
from paxos.core.role import Role
from paxos.net.history_channel import HistoryChannel
from paxos.net.message import Accepted, Response, Request, Sync, Synced
from paxos.net.proposal import Proposal
from paxos.utils.ledger import Ledger, LedgerEntry
from paxos.utils.state import State

from tests.stubs import InMemoryStorage


class TestLearner(TestCase):
    def setUp(self):
        self.channel = HistoryChannel(replicas=['A', 'B', 'C'])
        self.state = State(storage=InMemoryStorage("fakefile"))
        self.ledger_storage = InMemoryStorage("fakefile2")
        self.ledger = Ledger(storage=self.ledger_storage)
        self.role = Learner(ledger=self.ledger, state=self.state)

    def test_learner_receives_quorum_of_accepteds(self):
        self.role.receive(Accepted.create(proposal=Proposal('A', 1), sender='A'), self.channel)
        self.role.receive(Accepted.create(proposal=Proposal('A', 1), sender='B'), self.channel)
        self.role.receive(Accepted.create(proposal=Proposal('A', 1), sender='C'), self.channel)

        self.assertTrue(type(self.channel.unicast_messages[0]) is Request)
        self.assertTrue(type(self.channel.unicast_messages[1]) is Response)

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

    def test_learner_receives_sync(self):
        self.ledger.append(LedgerEntry(number=1, value="value_1"))
        self.ledger.append(LedgerEntry(number=2, value="value_2"))
        self.ledger.append(LedgerEntry(number=3, value="value_3"))

        self.role.receive(Sync.create(proposal=Proposal('A', 1), sender='A'), self.channel)

        message = self.channel.unicast_messages[-1]
        self.assert_equal(message.proposal[0], LedgerEntry(number=1, value="value_1"))
        self.assert_equal(message.proposal[1], LedgerEntry(number=2, value="value_2"))
        self.assert_equal(message.proposal[2], LedgerEntry(number=3, value="value_3"))

    def test_learner_receives_synced(self):
        proposals = [LedgerEntry(number=1, value="v_1"),
                     LedgerEntry(number=2, value="v_2"),
                     LedgerEntry(number=3, value="v_3")]

        self.role.receive(Synced.create(proposal=proposals, sender='A'), self.channel)

        def get_entry(line):
            return LedgerEntry(*line.split(LedgerEntry.SEPARATOR))

        self.assert_equal(get_entry(self.ledger_storage[0]), LedgerEntry(number=1, value="v_1"))
        self.assert_equal(get_entry(self.ledger_storage[1]), LedgerEntry(number=2, value="v_2"))
        self.assert_equal(get_entry(self.ledger_storage[2]), LedgerEntry(number=3, value="v_3"))

    def test_learner_receives_synced_and_merges_results(self):
        self.ledger_storage.append(str(LedgerEntry(number=1, value="v_1")))

        proposals = [LedgerEntry(number=1, value="v_1"),
                     LedgerEntry(number=2, value="v_2"),
                     LedgerEntry(number=3, value="v_3")]

        self.role.receive(Synced.create(proposal=proposals, sender='A'), self.channel)

        def get_entry(line):
            return LedgerEntry(*line.split(LedgerEntry.SEPARATOR))

        self.assert_equal(get_entry(self.ledger_storage[0]), LedgerEntry(number=1, value="v_1"))
        self.assert_equal(get_entry(self.ledger_storage[1]), LedgerEntry(number=2, value="v_2"))
        self.assert_equal(get_entry(self.ledger_storage[2]), LedgerEntry(number=3, value="v_3"))

    def test_learner_sync_messages(self):
        for i in range(Learner.SYNC_SIZE + 1):
            self.ledger.append(LedgerEntry(number=i, value="value_{0}".format(i)))

        self.role.receive(Sync.create(proposal=Proposal('A', 1), sender='A'), self.channel)

        message = self.channel.unicast_messages[-1]
        self.assertEqual(Learner.SYNC_SIZE, len(message.proposal))
        self.assertTrue(not message.finished)

    def assert_equal(self, actual_entry, expected_entry):
        self.assertEqual(actual_entry.number, expected_entry.number)
        self.assertEqual(actual_entry.value, expected_entry.value)

if __name__ == "__main__":
    main()
