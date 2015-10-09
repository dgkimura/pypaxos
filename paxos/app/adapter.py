from paxos.utils.ledger import Ledger
from paxos.utils.state import State
from paxos.utils.storage import Storage


class Adapter(object):
    def __init__(self):
        self.state = State(Storage("pypaxos.checkpoint"))
        self.ledger = Ledger()

    def read(self, key):
        obj = None
        for l in self.ledger:
            from yaml import load
            if "=" in l.value and l.value.split('=')[0] == key:
                obj = load(eval(l.value.split('=')[1]))
        #import pdb; pdb.set_trace()
        return obj
