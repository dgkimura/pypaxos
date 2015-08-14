# acceptor.py
from paxos.core.role import Role
from paxos.net.message import Prepare, Promise, Accept, Nack, Accepted
from paxos.utils.postit import PostIt


class Acceptor(Role):
    PROMISED = "promised.proposal"
    ACCEPTED = "accepted.proposal"
    VALUE = "value.str"

    def __init__(self, *args, postit=None, **kwargs):
        super(Acceptor, self).__init__(*args, **kwargs)
        self.postit = postit or PostIt("acceptor.postit")

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
        if message.proposal >= self.postit.read(Acceptor.PROMISED):
            self.postit.write(Acceptor.PROMISED, message.proposal)
            reply = create_reply(
                sender=message.receiver,
                receiver=message.sender,
                proposal=message.proposal,
                accepted_proposal=self.postit.read(Acceptor.ACCEPTED),
                value=message.value)
            channel.unicast(reply)
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
        if message.proposal >= self.postit.read(Acceptor.PROMISED):
            if message.proposal > self.postit.read(Acceptor.ACCEPTED):
                self.postit.write(Acceptor.ACCEPTED, message.proposal)
                self.postit.write(Acceptor.VALUE, message.value)

            reply = create_reply(sender=message.receiver,
                                 value=self.postit.read(Acceptor.VALUE))
            channel.broadcast(reply)
        else:
            reply = Nack.create(sender=message.receiver,
                                receiver=message.sender)
            channel.unicast(reply)
