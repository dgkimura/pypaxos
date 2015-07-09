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
        _socket.connect(('', Socket.__PORT))
        _socket.sendall(self._serializer.dumps(data))
        _socket.close()

    def receive(self, listener, channel):
        pool = ThreadPoolExecutor(128)
        _socket = socket(AF_INET, SOCK_STREAM)
        _socket.bind(('', Socket.__PORT))
        _socket.listen(Socket.__MAX_BACKLOG_SIZE)
        while True:
            client_socket, client_address = _socket.accept()
            pool.submit(self._route_to_listener, client_socket, listener, channel)

    def _route_to_listener(self, _socket, listener, channel):
        data = _socket.recv(Socket.__MAX_MESSAGE_SIZE)
        _socket.close()
        listener.receive(self._serializer.loads(data), channel)
