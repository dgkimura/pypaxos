# history_channel.py

class HistoryChannel(object):
    def __init__(self, replicas=None):
        self.broadcast_messages = []
        self.unicast_messages = []
        self.replicas = replicas or []

    def unicast(self, message):
        self.unicast_messages.append(message)

    def broadcast(self, message):
        self.broadcast_messages.append(message)
