from functools import partial
from unittest import TestCase, main
from unittest.mock import Mock, patch

from paxos.core.acceptor import Acceptor
from paxos.net.message import Prepare, Promise, Accept, Accepted


class TestAcceptor(TestCase):
    def setUp(self):
        self.create_reply = lambda m, sender=None, receiver=None: m

    def test_receive_prepare(self):
        mock_channel = Mock()
        role = Acceptor()

        message = Mock()
        role.receive(Prepare.create(), mock_channel,
                     partial(self.create_reply, m=message))

        mock_channel.unicast.assert_called_with(message)

    def test_receive_accept(self):
        mock_channel = Mock()
        role = Acceptor()

        message = Mock()
        role.receive(Accept.create(), mock_channel,
                     partial(self.create_reply, m=message))

        mock_channel.broadcast.assert_called_with(message)


if __name__ == "__main__":
    main()

