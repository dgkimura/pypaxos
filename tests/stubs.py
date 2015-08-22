from paxos.utils.persistedstate import PersistedState


class InMemoryState(PersistedState):
    def __init__(self):
        super(InMemoryState, self).__init__("fake_file_name")

    def _refresh(self):
        pass

    def _flush(self):
        pass


class NopLedger(object):
    def append(self, log):
        pass
