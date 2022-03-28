
import socket
import ssl


class ShockerSocket:
    def __init__(self, host: str, port: int = 80, timeout: int = 5,
                 buffsize: int = 4096, is_ssl: bool = False) -> None:

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

    def send(self , data : str):
        if self.is_ssl:
            return self._sslsock.send(data.encode('utf-8'))
        else :
            return self._sock.sendall(data.encode('utf-8'))

    def recv(self):
        if self.is_ssl:
            return self._sslsock.recv(self.buffsize)
        else:
            return self._sock.recv(self.buffsize)

    def __exit__(self):
        if self.is_ssl:
            self._sslsock.close()
        else:
            self._sock.close()
