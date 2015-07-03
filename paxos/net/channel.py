# channel.py


import cPickle as pickle
from socket import socket, AF_INET, SOCK_STREAM


class Channel(object):
    __MESSAGE_SIZE = 4
    __PORT = 8081

    def __init__(self, host):
        self.host = host

    def unicast(self, message):
        sock = socket(AF_INET, SOCK_STREAM)
        sock.connect((message.receiver, Channel.__PORT))
        sock.sendall(pickle.dumps(message))

    def broadcast(self, message):
        pass

    def listen(self):
        # TODO: non-blocking w/gevent, greenlet, or zeromq
        sock = socket(AF_INET, SOCK_STREAM)
        sock.bind((self.host, Channel.__PORT))
        sock.listen(1)

        conn, addr = sock.accept()

        message_size = int(conn.recv(CHANNEL.__MESSAGE_SIZE))
        data = ""
        while len(data) < message_size:
            packet = conn.recv(message_size)
            data += packet

        message = pickle.loads(data)

        # TODO: send message to paxos node
