
from core.engines.shockerSocket import ShockerSocket
from utils.logger import Logger


class CoreEngine:
    def __init__(self, host: str, port: int, timeout: int = 5, buffsize: int = 8192,
                 reuse_socket: bool = False, is_ssl: bool = False, sleepingtime: int = 0.5,
                 log_file: str = None) -> None:
        """
            Steering to run various plugins and engines to fuzz protocols

            Attributes
            -------------
            host : str
            port : int
            timeout : int
            buffsize : int
            reuse_socket : bool
            is_ssl : bool
            sleepingtime : int
            log_file : str

            Methods
            ------------
            launchCustomPayload:
                send the payload into the connected socket and return bytes response

        """

        self.host = host
        self.port = port
        self.reuse_socket = reuse_socket
        self.is_ssl = is_ssl
        self.timeout = timeout
        self.buffsize = buffsize
        self.sleepingtime = sleepingtime
        self.log_file = log_file

        self.sock = ShockerSocket(
            host, port, timeout, buffsize, is_ssl)
        self.sock.plug()

        if log_file:
            self.logger = Logger(filename=log_file)
        else:
            self.logger = Logger()

    def launchCustomPayload(self, payload_body: str) -> bytes:

        # send the payload body and return the response from the servers
        if not self.reuse_socket:
            self.sock.__exit__()
            self.sock = ShockerSocket(
                self.host, self.port, self.timeout, self.buffsize, self.is_ssl)
            self.sock.plug()

        cur_sock = self.sock
        # print("Sending : ", end="")
        # print(payload_body.__str__().encode('utf-8'))
        cur_sock.send(payload_body.__str__().encode('utf-8'))
        response = cur_sock.recv()
        return response
