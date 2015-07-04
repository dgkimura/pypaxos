# node.py
from paxos.core.acceptor import Acceptor
from paxos.core.learner import Learner
from paxos.core.proposer import Proposer


class Node(Proposer, Acceptor, Learner):
    def __init__(self, channel):
        self._channel = channel
