# proposer.py
from paxos.core.role import Role
from paxos.net.message import Request, Prepare, Promise, Accept, Accepted


class Proposer(Role):
    @Role.receive.register(Request)
    def _(self, message, channel, create_reply=Prepare.create):
        print("RECEIVED message {0}".format(message))
        reply = create_reply(sender=message.receiver)
        channel.broadcast(reply)

    @Role.receive.register(Promise)
    def _(self, message, channel, create_reply=Accept.create):
        print("RECEIVED message {0}".format(message))
        reply = create_reply(sender=message.receiver)
        channel.broadcast(reply)

    #@Role.receive.register(Accepted)
    #def _(self, message):
    #    pass
