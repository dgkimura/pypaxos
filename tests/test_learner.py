from functools import partial
from unittest import TestCase, main
from unittest.mock import Mock, patch

from paxos.core.learner import Learner
from paxos.net.message import Accepted, Response


class TestLearner(TestCase):
    def setUp(self):
        self.create_reply = lambda m, sender=None, receiver=None: m

    def test_receive_accepted(self):
        mock_channel = Mock()
        role = Learner()

        message = Mock()
        role.receive(Accepted.create(), mock_channel,
                     partial(self.create_reply, message))

        mock_channel.unicast.assert_called_with(message)


if __name__ == "__main__":
    main()
