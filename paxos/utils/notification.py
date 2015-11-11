import asyncio
from asyncio import Event


class Notification(object):
    def __init__(self):
        self.pending_proposals = {}
        self.loop = asyncio.new_event_loop()
        asyncio.set_event_loop(self.loop)
        self.event = Event(loop=self.loop)

    def wait(self, proposal):
        asyncio.set_event_loop(self.loop)
        self.loop.run_until_complete(self._wait(proposal))

    @asyncio.coroutine
    def _wait(self, proposal):
        while True:
            if (yield from self.event.wait()):
                if proposal in self.pending_proposals:
                    del self.pending_proposals[proposal]
                    return True

    def send(self, response):
        self.pending_proposals[response.proposal] = response
        self.loop.call_soon_threadsafe(self.event.set)
