from concurrent.futures import ThreadPoolExecutor
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
        _socket = socket(AF_INET, SOCK_STREAM)
        print("SENDING {0}".format(data))
        _socket.connect(('', Socket.__PORT))
        _socket.sendall(self._serializer.dumps(data))
        _socket.close()

    def receive(self, listener):
        pool = ThreadPoolExecutor(128)
        _socket = socket(AF_INET, SOCK_STREAM)
        _socket.bind(('', Socket.__PORT))
        _socket.listen(Socket.__MAX_BACKLOG_SIZE)
        while True:
            client_sock, client_addr = _socket.accept()
            pool.submit(self.send_to_listener, client_sock, client_addr, listener)

    def send_to_listener(self, sock, client_addr, listener):
        data = sock.recv(Socket.__MAX_MESSAGE_SIZE)
        sock.close()
        print("Received {0}".format(data))
        listener.receive(self._serializer.loads(data))
