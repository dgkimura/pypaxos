from linecache import getline, checkcache


class Storage(object):
    def __init__(self, filename):
        self._filename = filename

    def __getitem__(self, index):
        checkcache()
        return getline(self._filename, index + 1)

    def __iter__(self):
        for i in range(len(self)):
            yield self.__getitem__(i)

    def __len__(self):
        length = 0
        for line in open(self._filename): length += 1
        return length

    def append(self, line):
        with open(self._filename, 'a') as f:
            f.write("{0}\n".format(line))

    def get(self):
        with open(self._filename, 'r') as f:
            return f.read()

    def put(self, contents):
        with open(self._filename, 'w+') as f:
            f.write(contents)
            f.truncate()
