from unittest import TestCase, main

from paxos.core.proposer import Proposer
from paxos.net.history_channel import HistoryChannel
from paxos.net.message import Request, Prepare, Promise, Accept, Accepted


class TestProposer(TestCase):
    def test_receive_request(self):
        channel = HistoryChannel()
        role = Proposer()

        role.receive(Request.create(), channel)

        self.assertTrue(type(channel.broadcast_messages[0]) is Prepare)

    def test_receive_promise(self):
        channel = HistoryChannel()
        role = Proposer()

        role.receive(Promise.create(), channel)

        self.assertTrue(type(channel.broadcast_messages[0]) is Accept)


if __name__ == "__main__":
    main()
