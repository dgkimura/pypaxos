# datalog.py
from datetime import datetime


class Ledger(object):
    __FILENAME = "pypaxos.ledger"

    def __init__(self):
        self._fd = open(self.__FILENAME, "a")

    def append(self, proposal, log):
        self._fd.write("{0},{1},{2}\n".format(proposal, datetime.now(), log))
        self._fd.flush()
