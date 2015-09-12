# datalog.py
from datetime import datetime

from paxos.utils.storage import Storage


class Ledger(object):
    __FILENAME = "pypaxos.ledger"

    def __init__(self, storage=None):
        self._storage = storage or Storage(Ledger.__FILENAME)

    def append(self, ledger_entry):
        self._storage.append(ledger_entry)

    def extend(self, ledger_entries):
        for entry in ledger_entries:
            self.append(entry)

    def __getitem__(self, search):
        minline = 0
        maxline = len(self._storage)
        midline = maxline / 2

        found = None

        while found != search or (midline < minline or midline > maxline):
            midline = (maxline - minline) / 2 + minline

            ledger_entry = LedgerEntry(self._storage[midline].split(
                LedgerEntry.SEPARATOR))
            found = ledger_entry.number

            if found < search:
                maxline = midline
            elif found > search:
                minline = midline

        if found == search:
            return ledger_entry
        raise IndexError("Index proposal {0} not in ledger.".format(search))


class LedgerEntry(object):
    SEPARATOR = ","

    def __init__(self, number=None, timestamp=None, value=None):
        self.number = number
        self.timestamp = timestamp or datetime.now()
        self.value = value

    def __str__(self):
        return "{0},{1},{2}".format(self.number, self.timestamp, self.value)
