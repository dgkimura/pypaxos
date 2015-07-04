from socket import socket, AF_INET, SOCK_STREAM


class Socket(object):
    __PORT = 8081
    __MESSAGE_SIZE = 4

    def send(self, ip, data):
        sock = socket(AF_INET, SOCK_STREAM)
        sock.connect((ip, port))
        sock.sendall(data)

    def receive(self, ip):
        # TODO: non-blocking w/gevent, greenlet, or zeromq
        sock = socket(AF_INET, SOCK_STREAM)
        sock.bind((ip, Socket.__PORT))
        sock.listen(1)

        conn, addr = sock.accept()

        message_size = int(conn.recv(Socket.__MESSAGE_SIZE))
        data = ""
        while len(data) < message_size:
            packet = conn.recv(message_size)
            data += packet

        return pickle.loads(data)
