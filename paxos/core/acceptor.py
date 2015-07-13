# acceptor.py
from paxos.core.role import Role
from paxos.net.message import Prepare, Promise, Accept, Nack, Accepted


class Acceptor(Role):
    def __init__(self, *args, **kwargs):
        super(Acceptor, self).__init__(*args, **kwargs)
        self.promised_proposal = None
        self.accepted_proposal = None
        self.accepted_value = None

    @Role.receive.register(Prepare)
    def _(self, message, channel, create_reply=Promise.create):
        """Promise Phase.

        If an acceptor receives a prepare request with number n greater than
        that of any prepare request to which it has already responded then it
        responds to the request with a promise not to accept any more
        proposals numbered less than n and with the highest-numbered proposal
        (if any) that it has accepted.

        """
        print("RECEIVED message {0}".format(message))
        if (self.promised_proposal is None or
            message.proposal.number >= self.promised_proposal.number):
            reply = create_reply(sender=message.receiver,
                                 receiver=message.sender,
                                 proposal=message.proposal,
                                 accepted_proposal=self.accepted_proposal,
                                 value=self.accepted_value)
            channel.unicast(reply)
            self.promised_proposal = message.proposal
        else:
            reply = Nack.create(sender=message.receiver,
                                receiver=message.sender)
            channel.unicast(reply)

    @Role.receive.register(Accept)
    def _(self, message, channel, create_reply=Accepted.create):
        """Accepted Phase.

        If an acceptor receives an accept request for a proposal numbered n,
        it accepts the proposal unless it has already responded to a prepare
        request having a number greater than n.

        """
        print("RECEIVED message {0}".format(message))
        if message.proposal.number >= self.promised_proposal.number:
            reply = create_reply(sender=message.receiver,
                                 value=message.value)
            channel.broadcast(reply)

            if (self.accepted_proposal is None or
                message.proposal.number > self.accepted_proposal.number):
                self.accepted_proposal = message.proposal
        else:
            reply = Nack.create(sender=message.receiver,
                                receiver=message.sender)
            channel.unicast(reply)
