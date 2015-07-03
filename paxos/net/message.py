# message.py


class Message(object):
    def __init__(self, sender, receiver):
        self.sender = sender
        self.receiver = receiver


class Request(Message):
    pass


class Prepare(Message):
    pass


class Promise(Message):
    pass


class Accept(Message):
    pass


class Accepted(Message):
    pass


class Response(Message):
    pass
