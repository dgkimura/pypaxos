from paxos.utils.decorators import methoddispatch
from paxos.app.types.dicts import Dict
from paxos.app.types.lists import List
from paxos.app.types.numbers import Number


class Dispatcher(object):
    def __init__(self, channel):
        self.channel = channel

    @methoddispatch
    def create(self, obj, name):
        error = "No function handles object type: {0}".format(obj)
        raise NotImplementedError(error)


class Factory(Dispatcher):
    @Dispatcher.create.register(int)
    def _(self, obj, name):
        return Number(name, obj, self.channel)

    @Dispatcher.create.register(dict)
    def _(self, obj, name):
        return Dict(name, obj, self.channel)

    @Dispatcher.create.register(list)
    def _(self, obj, name):
        return List(name, obj, self.channel)
