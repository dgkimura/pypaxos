from unittest import TestCase, main
from unittest.mock import Mock, patch

from paxos.core.learner import Learner
from paxos.net.message import Accepted, Response


class TestLearner(TestCase):
    @patch.object(Response, "create")
    def test_receive_accepted(self, mock_create_response):
        message = Mock()
        mock_create_response.return_value = message

        mock_channel = Mock()
        role = Learner()
        role.receive(Accepted.create(), mock_channel)

        mock_channel.unicast.assert_called_with(message)


if __name__ == "__main__":
    main()
