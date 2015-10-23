from threading import Lock


class Selector(object):
    def __init__(self):
        self.values = list()
        self.mapper = dict()
        self.lock = Lock()

    def add(self, value):
        self.values.append(value)

    def get(self, proposal):
        with self.lock:
            if not proposal in self.mapper:
                if self.values:
                    self.mapper[proposal] = self.values.pop(0)
                else:
                    self.mapper[proposal] = None
        return self.mapper[proposal]

    def set(self, proposal, value):
        self.mapper[proposal] = value

    def is_empty(self):
        return len(self.values) is 0
