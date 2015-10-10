from yaml import load

from paxos.utils.ledger import Ledger
from paxos.utils.state import State
from paxos.utils.storage import Storage


class Adapter(object):
    def __init__(self, ledger=None, deserializer=load):
        self.state = State(Storage("pypaxos.checkpoint"))
        self.ledger = ledger or Ledger()
        self._deserialize = deserializer

    def read(self, key):
        obj = None
        for l in self.ledger:
            if "=" in l.value and l.value.split('=')[0] == key:
                obj = self._deserialize(eval(l.value.split('=')[1]))
        return obj
