# learner.py
from paxos.core.role import Role
from paxos.net.message import Accepted, Response


class Learner(Role):
    @Role.receive.register(Accepted)
    def _(self, message, channel):
        print("RECEIVED message {0}".format(message))
        reply = Response.create()
        channel.unicast(reply)
