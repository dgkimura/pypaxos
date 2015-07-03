from functools import singledispatch


class Role(object):
    @singledispatch
    def receive(self, message):
        error = "No function handles message: {0}.".format(message)
        raise NotImplementedError(error)
