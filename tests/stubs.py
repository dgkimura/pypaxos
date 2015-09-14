from paxos.utils.state import State


class InMemoryStorage(object):
    def __init__(self, filename):
        self._contents = ""

    def __getitem__(self, index):
        return self._contents.splitlines()[index]

    def __len__(self):
        return len(self._contents.splitlines())

    def append(self, line):
        self._contents += "{0}\n".format(line)

    def get(self):
        return self._contents

    def put(self, contents):
        self._contents = contents
