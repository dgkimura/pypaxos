# basic.py
import socket

from paxos.core.node import Node
from paxos.net.channel import Channel


def main():
    host = socket.gethostbyname(socket.gethostname())
    replicas = [socket.gethostbyname(socket.gethostname())]
    channel = Channel(host, replicas)

    node = Node(channel)
    channel.listen()


if __name__ == "__main__":
    main()
