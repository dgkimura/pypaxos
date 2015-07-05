# node.py
from concurrent.futures import ThreadPoolExecutor
from threading import Thread

from paxos.core.acceptor import Acceptor
from paxos.core.learner import Learner
from paxos.core.proposer import Proposer


class Node(Proposer, Acceptor, Learner):
    def __init__(self, channel):
        self._channel = channel

    def start(self):
        self.keep_alive = True
        t = Thread(target=self._run)
        t.daemon = True
        t.start()

    def stop(self):
        self.keep_alive = False

    def _run(self):
        while self.keep_alive:
            pool = ThreadPoolExecutor(max_workers=128)
            future = pool.submit(self._channel.listen)
            message = future.result()
            self.receive(message)
