# datalog.py


class Ledger(object):
    __FILENAME = "pypaxos.ledger"

    def __init__(self):
        self._fd = open(self.__FILENAME, "a")

    def append(self, log):
        self._fd.write("{0}\n".format(log))
        self._fd.flush()
