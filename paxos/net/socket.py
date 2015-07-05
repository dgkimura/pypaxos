from socket import socket, AF_INET, SOCK_STREAM


try:
    import cPickle as pickle
except ImportError:
    import pickle


class Socket(object):
    __PORT = 8081
    __MAX_MESSAGE_SIZE = 65536
    __MAX_BACKLOG_SIZE = 5

    def __init__(self, serializer=pickle):
        self._serializer = serializer

    def send(self, ip, data):
        sock = socket(AF_INET, SOCK_STREAM)
        sock.connect((ip, Socket.__PORT))
        sock.sendall(self._serializer.dumps(data))

    def receive(self, ip):
        sock = socket(AF_INET, SOCK_STREAM)
        sock.bind((ip, Socket.__PORT))
        sock.listen(Socket.__MAX_BACKLOG_SIZE)
        conn, addr = sock.accept()

        data = conn.recv(Socket.__MAX_MESSAGE_SIZE)
        return self._serializer.loads(data)
