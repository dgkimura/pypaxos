from paxos.utils.decorators import methoddispatch


class Role(object):
    @methoddispatch
    def receive(self, message):
        error = "No function handles message: {0}.".format(message)
        raise NotImplementedError(error)
