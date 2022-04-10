from logging import Logger
from core.engines.shockerSocket import ShockerSocket


class CoreEngine:
    def __init__(self, host: str, port: int, timeout: int = 5, buffsize: int = 8192,
                 reuse_socket: bool = False, is_ssl: bool = False, sleepingtime: int = 0.5,
                 log_file: str = None) -> None:

        self.host = host
        self.port = port
        self.reuse_socket = reuse_socket
        self.is_ssl = is_ssl
        self.timeout = timeout
        self.buffsize = buffsize
        self.sleepingtime = sleepingtime

        if self.reuse_socket:
            self.sock = ShockerSocket(
                host, port, timeout, buffsize, is_ssl)
            self.sock.plug()

        if log_file:
            self.logger = Logger(filename=log_file)
        else:
            self.logger = Logger()

    def launchCustomPayload(self, payload_body):

        # send the payload body and return the response from the servers
        if self.reuse_socket:
            cur_sock = self.sock
        else:
            cur_sock = ShockerSocket(
                self.host, self.port, self.timeout, self.buffsize, self.is_ssl)
            cur_sock.plug()

        cur_sock.send(payload_body)
        response = cur_sock.recv()
        return response