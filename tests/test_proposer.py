from functools import partial
from unittest import TestCase, main
from unittest.mock import Mock, patch

from paxos.core.proposer import Proposer
from paxos.net.message import Request, Prepare, Promise, Accept, Accepted


class TestProposer(TestCase):
    def setUp(self):
        self.create_reply = lambda m, sender=None, receiver=None: m

    def test_receive_request(self):
        mock_channel = Mock()
        role = Proposer()

        message = Mock()
        role.receive(Request.create(), mock_channel,
                     partial(self.create_reply, m=message))

        mock_channel.broadcast.assert_called_with(message)

    def test_receive_promise(self):
        mock_channel = Mock()
        role = Proposer()

        message = Mock()
        role.receive(Promise.create(), mock_channel,
                     partial(self.create_reply, m=message))

        mock_channel.broadcast.assert_called_with(message)


if __name__ == "__main__":
    main()
