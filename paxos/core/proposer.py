# proposer.py
from paxos.core.role import Role
from paxos.net.message import Request, Prepare, Promise, Accept, Accepted


class Proposer(Role):
    def __init__(self, *args, **kwargs):
        super(Proposer, self).__init__(*args, **kwargs)
        self.highest_proposal = None
        self.proposed_value = None
        self.received_promises = dict()

    @Role.receive.register(Request)
    def _(self, message, channel, create_reply=Prepare.create):
        """Prepare Phase.

        A proposer selects a proposal number n and sends a prepare request
        with number n to a majority of acceptors.

        """
        print("RECEIVED message {0}".format(message))
        reply = create_reply(sender=message.receiver,
                             proposal=self.next_proposal)
        channel.broadcast(reply)
        self.proposed_value = message.value

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
        self.received_promises.setdefault(message.proposal, set()) \
            .add(message.sender)

        if (self.highest_proposal is None or
            message.accepted_proposal is not None and
            message.accepted_proposal.number >= self.highest_proposal.number):
            self.highest_proposal = message.proposal
            if message.value is not None:
                self.proposed_value = message.value

        minimum_quorum = len(channel.replicas) // 2 + 1
        received_promises = len(self.received_promises.get(message.proposal))

        if received_promises >= minimum_quorum:
            reply = create_reply(sender=message.receiver,
                                 proposal=message.proposal,
                                 value=self.proposed_value)
            channel.broadcast(reply)

    #@Role.receive.register(Accepted)
    #def _(self, message):
    #    pass
