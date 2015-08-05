# datalog.py


class DataLog(object):
    __FILENAME = "pypaxos_datalog.txt"

    def __init__(self):
        self._fd = open(self.__FILENAME, "a")

    def append(self, log):
        self._fd.write("{0}\n".format(log))
        self._fd.flush()
