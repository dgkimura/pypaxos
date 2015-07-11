from unittest import TestCase, main

from paxos.core.learner import Learner
from paxos.net.history_channel import HistoryChannel
from paxos.net.message import Accepted, Response


class TestLearner(TestCase):
    def test_receive_accepted(self):
        channel = HistoryChannel()
        role = Learner()

        role.receive(Accepted.create(), channel)

        self.assertTrue(type(channel.unicast_messages[0]) is Response)


if __name__ == "__main__":
    main()
