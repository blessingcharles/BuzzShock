from socket import socket


class BuzzEngine:
    def __init__(self, payload_body) -> None:
        self.payload_body = payload_body

    def run(self):
        plug = socket
