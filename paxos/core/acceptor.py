# acceptor.py
from paxos.core.role import Role
from paxos.net.message import Prepare, Promise, Accept, Accepted


class Acceptor(Role):
    @Role.receive.register(Prepare)
    def _(self, message, channel):
        print("RECEIVED message {0}".format(message))
        reply = Promise.create(sender=message.receiver, receiver=message.sender)
        channel.unicast(reply)

    @Role.receive.register(Accept)
    def _(self, message, channel):
        print("RECEIVED message {0}".format(message))
        reply = Accepted.create(sender=message.receiver)
        channel.broadcast(reply)
