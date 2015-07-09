# proposer.py
from paxos.core.role import Role
from paxos.net.message import Request, Prepare, Promise, Accept, Accepted


class Proposer(Role):
    @Role.receive.register(Request)
    def _(self, message, channel):
        print("RECEIVED message {0}".format(message))
        reply = Prepare.create(sender=message.receiver)
        channel.broadcast(reply)

    @Role.receive.register(Promise)
    def _(self, message, channel):
        print("RECEIVED message {0}".format(message))
        reply = Accept.create(sender=message.receiver)
        channel.broadcast(reply)

    #@Role.receive.register(Accepted)
    #def _(self, message):
    #    pass
