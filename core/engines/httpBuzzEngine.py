import os
import glob
from pprint import pprint
from core.engines.shockerSocket import ShockerSocket


class HttpBuzzEngine:
    def __init__(self, host: str, port: int, timeout: int = 5, buffsize: int = 8192, reuse_socket: bool = False, is_ssl: bool = False) -> None:

        self.host = host
        self.port = port
        self.reuse_socket = reuse_socket
        self.is_ssl = is_ssl
        self.timeout = timeout
        self.buffsize = buffsize

        if self.reuse_socket:
            self.sock = ShockerSocket(
                host, port, timeout, buffsize, is_ssl)
            self.sock.plug()

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

    def launchFromDb(self, db_path: str = "db/http"):
        
        possible_requests_path = [y for x in os.walk(
            db_path) for y in glob.glob(os.path.join(x[0], '*.req'))]
        
        pprint(possible_requests_path)
