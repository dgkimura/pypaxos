from unittest import TestCase, main
from unittest.mock import Mock, patch

from paxos.core.proposer import Proposer
from paxos.net.message import Request, Prepare, Promise, Accept, Accepted


class TestProposer(TestCase):
    @patch.object(Prepare, "create")
    def test_receive_request(self, mock_create_prepare):
        message = Mock()
        mock_create_prepare.return_value = message

        mock_channel = Mock()
        role = Proposer(mock_channel)
        role.receive(Request.create())

        mock_channel.broadcast.assert_called_with(message)

    @patch.object(Accept, "create")
    def test_receive_promise(self, mock_create_accept):
        message = Mock()
        mock_create_accept.return_value = message

        mock_channel = Mock()
        role = Proposer(mock_channel)
        role.receive(Promise.create())

        mock_channel.broadcast.assert_called_with(message)


if __name__ == "__main__":
    main()
