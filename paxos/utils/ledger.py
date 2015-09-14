# datalog.py
from datetime import datetime

from paxos.utils.storage import Storage


class Ledger(object):
    __FILENAME = "pypaxos.ledger"

    def __init__(self, storage=None):
        self._storage = Storage(Ledger.__FILENAME)

        if storage is not None:
            self._storage = storage

    def append(self, ledger_entry):
        self._storage.append(ledger_entry)

    def extend(self, ledger_entries):
        for entry in ledger_entries:
            self.append(entry)

    def get_range(self, start, end=None):
        storage_range = []
        start_index = self._getindex(start)
        end_index = self._getindex(end)

        return [LedgerEntry(*l.split(LedgerEntry.SEPARATOR))
                for l in self._storage[start_index:end_index]]

    def _getindex(self, proposal):
        if proposal is None:
            return None

        # TODO: O(log n) Binary Search
        for index, line in enumerate(self._storage):
            entry = LedgerEntry(*line.split(LedgerEntry.SEPARATOR))
            if entry.number == proposal.number:
                return index
        return None


class LedgerEntry(object):
    SEPARATOR = ","

    def __init__(self, number=None, timestamp=None, value=None):
        self.number = int(number)
        self.timestamp = timestamp or datetime.now()
        self.value = value

    def __str__(self):
        return "{0},{1},{2}".format(self.number, self.timestamp, self.value)

    def __eq__(self, other):
        return self.__dict__ == other.__dict__
