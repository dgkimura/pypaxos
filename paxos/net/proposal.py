# proposal.py


def default_proposal():
    return Proposal("", 0)


class Proposal(object):
    def __init__(self, author, number):
        self.author = author
        self.number = number

    def __lt__(self, other):
        return self.number < other.number

    def __le__(self, other):
        return self.number <= other.number

    def __gt__(self, other):
        return self.number > other.number

    def __ge__(self, other):
        return self.number >= other.number

    def __eq__(self, other):
        if other:
            return self.number == other.number
        return False

    def __hash__(self):
        return (self.author, self.number).__hash__()

    def __str__(self):
        return "Proposal({0}, {1})".format(self.author, self.number)

    def next(self):
        return Proposal(self.author, self.number + 1)


class InitialProposal(Proposal):
    def __init__(self, author):
        super(InitialProposal, self).__init__(author, 0)
