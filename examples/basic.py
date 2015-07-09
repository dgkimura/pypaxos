# basic.py
import socket
import time

from paxos.core.node import Node
from paxos.net.channel import Channel
from paxos.net.message import Request, Prepare, Promise, Accept, Accepted


def main():
    host = socket.gethostbyname(socket.gethostname())
    replicas = [socket.gethostbyname(socket.gethostname())]
    channel = Channel(replicas)

    node = Node()
    channel.connect(node)

    message = Request(host, host)
    channel.unicast(message)
    channel.unicast(Request(host, host))
    channel.unicast(Request(host, host))
    channel.unicast(Request(host, host))
    channel.unicast(Request(host, host))
    channel.unicast(Request(host, host))

    time.sleep(15)

if __name__ == "__main__":
    main()
