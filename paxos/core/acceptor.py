# acceptor.py
from paxos.core.role import Role
from paxos.net.message import Prepare, Promise, Accept, Nack, Accepted


class Acceptor(Role):
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
        if message.proposal.number >= self.prepared_proposal.number:
            reply = create_reply(sender=message.receiver,
                                 receiver=message.sender,
                                 proposal=message.proposal,
                                 accepted_proposal=self.accepted_proposal)
            channel.unicast(reply)
            self.prepared_proposal = message.proposal
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
        if message.proposal.number >= self.prepared_proposal.number:
            reply = create_reply(sender=message.receiver)
            channel.broadcast(reply)

            if message.proposal.number > self.accepted_proposal.number:
                self.accepted_proposal = message.proposal
        else:
            reply = Nack.create(sender=message.receiver,
                                receiver=message.sender)
            channel.unicast(reply)
