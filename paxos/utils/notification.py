from threading import Condition, Lock


class Notification(object):
    def __init__(self):
        self.pending_proposals = {}
        self.finished_proposal = Condition(Lock())

    def wait(self, proposal):
        self.finished_proposal.acquire()
        try:
            while True:
                if proposal in self.pending_proposals:
                    response = self.pending_proposals[proposal]
                    if response is not None:
                        del self.pending_proposals[proposal]
                        return response
                self.finished_proposal.wait()
        finally:
            self.finished_proposal.release()

    def send(self, response):
        self.finished_proposal.acquire()
        try:
            self.pending_proposals[response.proposal] = response
            self.finished_proposal.notify()
        finally:
            self.finished_proposal.release()
