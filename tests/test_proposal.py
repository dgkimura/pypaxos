from unittest import TestCase, main

from paxos.net.proposal import Proposal


class TestProposal(TestCase):
    def test_proposal_equality(self):
        a_1 = Proposal("a", 1)
        a_2 = Proposal("a", 2)

        b_1 = Proposal("b", 1)
        b_2 = Proposal("b", 2)

        self.assertTrue(a_1 < a_2)
        self.assertTrue(a_2 > a_1)

        self.assertTrue(a_1 < b_2)
        self.assertTrue(a_2 > b_1)

        self.assertTrue(a_1 >= a_1)
        self.assertTrue(a_1 <= a_1)
        self.assertFalse(a_1 >= b_1)
        self.assertFalse(a_1 <= b_1)
