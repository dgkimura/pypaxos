# basic.py
import socket
import time

from paxos.core.node import Node
from paxos.net.channel import Channel
from paxos.net.message import Request, Prepare, Promise, Accept, Accepted


def main():
    host = socket.gethostbyname(socket.gethostname())

    channel = Channel()
    channel.connect(Node())

    while True:
        print("fast requests...")
        send_requests(channel, host, 0)
        print()
        time.sleep(2)
        print("slow requests...")
        send_requests(channel, host, 1)
        time.sleep(15)

def send_requests(channel, host, interval=1):
    for v in ["a", "b", "c", "d", "e", "f", "g", "z"]:
        for n in range(1):
            val = v + str(n)
            channel.unicast(Request.create(sender=host, receiver=host, value=val))
            time.sleep(interval)


if __name__ == "__main__":
    main()
