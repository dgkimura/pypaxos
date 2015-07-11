# proposer.py
from paxos.core.role import Role
from paxos.net.message import Request, Prepare, Promise, Accept, Accepted


class Proposer(Role):
    @Role.receive.register(Request)
    def _(self, message, channel, create_reply=Prepare.create):
        """Prepare Phase.

        A proposer selects a proposal number n and sends a prepare request
        with number n to a majority of acceptors.

        """
        print("RECEIVED message {0}".format(message))
        reply = create_reply(sender=message.receiver)
        channel.broadcast(reply)

    @Role.receive.register(Promise)
    def _(self, message, channel, create_reply=Accept.create):
        """Accept Phase.

        If the proposer receives a response to its prepare requests (numbered
        n) from a majority of acceptors, then it sends an accept request to
        each of those acceptors for a proposal numbered n with a value v, where
        v is the value of the highest-numbered proposal among the responses, or
        is any value if the responses reported no proposals.

        """
        print("RECEIVED message {0}".format(message))
        reply = create_reply(sender=message.receiver)
        channel.broadcast(reply)

    #@Role.receive.register(Accepted)
    #def _(self, message):
    #    pass
