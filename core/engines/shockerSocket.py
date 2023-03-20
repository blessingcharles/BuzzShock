
from pprint import pprint
import socket
import ssl


class ShockerSocket:
    def __init__(self, host: str, port: int = 80, timeout: int = 5,
                 buffsize: int = 8096, is_ssl: bool = False) -> None:
        """
            A simple pluggable socket for buzz shock

            Attributes
            -------------
            host : str
            port : int
            timeout : int
            buffsize : int
            is_ssl : bool

            Method
            -----------
            plug:
                connecting the socket
            send:
                sending the payload
            recv:
                receive atmost buffsize

        """
        self.host = host
        self.port = port
        self.timeout = timeout
        self.buffsize = buffsize
        self._sock = None
        self._sslsock = None
        self.is_ssl = is_ssl

    def plug(self):

        if (self.is_ssl):

            context: ssl.SSLContext = ssl.SSLContext(ssl.PROTOCOL_TLSv1_2)
            self._sock = socket.setdefaulttimeout(self.timeout)
            self._sock = socket.create_connection((self.host, int(self.port)))
            self._sslsock = context.wrap_socket(
                self._sock, server_hostname=self.host)
            self._sslsock.settimeout(self.timeout)

        else:
            self._sock = socket.setdefaulttimeout(self.timeout)
            self._sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self._sock.settimeout(self.timeout)
            self._sock.connect((self.host, self.port))

    def send(self, data: bytes):
        if self.is_ssl:
            return self._sslsock.send(data)
        else:
            return self._sock.sendall(data)

    def recvall(self, sock):
        data = b''
        while True:
            part = sock.recv(self.buffsize)
            data += part
            if len(part) < self.buffsize:
                # either 0 or end of data
                break
        return data

    def recv(self):
        try:
            if self.is_ssl:
                return self.recvall(self._sslsock)
            else:
                return self.recvall(self._sock)
        except Exception as e:
            return b""

    def __exit__(self):
        if self.is_ssl:
            self._sslsock.close()
        else:
            self._sock.close()
