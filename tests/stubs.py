from paxos.utils.state import State


class InMemoryStorage(object):
    def __init__(self, filename):
        self._contents = ""

    def __len__(self):
        return len(self._contents.split())

    def append(self, line):
        self._contents += "\n{0}".format(line)

    def get(self):
        return self._contents

    def put(self, contents):
        self._contents = contents


class NopLedger(object):
    def append(self, ledger_entry):
        pass
