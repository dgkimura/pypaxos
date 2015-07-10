# learner.py
from paxos.core.role import Role
from paxos.net.message import Accepted, Response


class Learner(Role):
    @Role.receive.register(Accepted)
    def _(self, message, channel, create_reply=Response.create):
        print("RECEIVED message {0}".format(message))
        reply = create_reply()
        channel.unicast(reply)
