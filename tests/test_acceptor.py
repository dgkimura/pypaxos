from unittest import TestCase, main
from unittest.mock import Mock, patch

from paxos.core.acceptor import Acceptor
from paxos.net.message import Prepare, Promise, Accept, Accepted


class TestAcceptor(TestCase):
    @patch.object(Promise, "create")
    def test_receive_prepare(self, mock_create_promise):
        message = Mock()
        mock_create_promise.return_value = message

        mock_channel = Mock()
        role = Acceptor()
        role.receive(Prepare.create(), mock_channel)

        mock_channel.unicast.assert_called_with(message)

    @patch.object(Accepted, "create")
    def test_receive_accept(self, mock_create_accepted):
        message = Mock()
        mock_create_accepted.return_value = message

        mock_channel = Mock()
        role = Acceptor()
        role.receive(Accept.create(), mock_channel)

        mock_channel.broadcast.assert_called_with(message)


if __name__ == "__main__":
    main()

