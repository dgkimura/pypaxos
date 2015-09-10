# proposer.py
from paxos.core.role import Role
from paxos.net.message import Request, Prepare, Promise, Accept, Accepted


class Proposer(Role):
    def __init__(self, *args, **kwargs):
        super(Proposer, self).__init__(*args, **kwargs)
        self.highest_proposal = None
        self.received_promises = dict()

    @Role.receive.register(Request)
    def _(self, message, channel, create_reply=Prepare.create):
        """Prepare Phase.

        A proposer selects a proposal number n and sends a prepare request
        with number n to a majority of acceptors.

        """
        print("RECEIVED message {0}".format(message))
        if message.value:
            self.requested_values.append(message.value)

        if self.requested_values:
            reply = create_reply(sender=message.receiver,
                                 proposal=self.state.read(Role.PROPOSED))
            channel.broadcast(reply)

    @Role.receive.register(Promise)
    @Role.update_proposal
    def _(self, message, channel, create_reply=Accept.create):
        """Accept Phase.

        If the proposer receives a response to its prepare requests (numbered
        n) from a majority of acceptors, then it sends an accept request to
        each of those acceptors for a proposal numbered n with a value v, where
        v is the value of the highest-numbered proposal among the responses, or
        is any value if the responses reported no proposals.

        """
        print("RECEIVED message {0}".format(message))
        self.received_promises.setdefault(message.proposal, set()) \
            .add(message.sender)

        value = self.requested_values and self.requested_values.pop(0) or None

        if (self.highest_proposal is None or
            message.accepted_proposal >= self.highest_proposal):
            self.highest_proposal = message.proposal
            if message.value:
                value = message.value
                self.requested_values.append(value)

        minimum_quorum = len(channel.replicas) // 2 + 1
        received_promises = len(self.received_promises.get(message.proposal))

        if received_promises >= minimum_quorum:
            reply = create_reply(sender=message.receiver,
                                 proposal=message.proposal,
                                 value=value)
            channel.broadcast(reply)

    #@Role.receive.register(Accepted)
    #def _(self, message):
    #    pass
