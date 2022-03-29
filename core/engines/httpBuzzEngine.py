from http.client import HTTPResponse
from io import BytesIO
from logging import exception
import os
import glob
from pprint import pprint
from time import sleep
from typing import Dict

import urllib3
from core.engines.shockerSocket import ShockerSocket
from utils.logger import Logger


class BytesIOSocket:
    def __init__(self, content):
        self.handle = BytesIO(content)

    def makefile(self, mode):
        return self.handle

    @classmethod
    def response_from_bytes(cls,data):
        sock = BytesIOSocket(data)

        response = HTTPResponse(sock)
        response.begin()

        return urllib3.HTTPResponse.from_httplib(response)


class HttpBuzzEngine:
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

    def launchFromDb(self, db_path: str = "db/http", testing_server_name: str = None) -> Dict[str, str]:

        self.results = {}
        extension = "req"

        possible_request_paths = [y for x in os.walk(
            db_path) for y in glob.glob(os.path.join(x[0], f'*.{extension}'))]

        if self.reuse_socket:
            cur_sock = self.sock

        for path in possible_request_paths:
            try:
                with open(path, "r") as f:
                    payload = f.read()
                    if not self.reuse_socket:
                        cur_sock = ShockerSocket(
                            self.host, self.port, self.timeout, self.buffsize, self.is_ssl)
                        cur_sock.plug()
                    cur_sock.send(payload)
                    raw_response_obj = cur_sock.recv()
                    response = BytesIOSocket.response_from_bytes(
                        raw_response_obj)

                    if response.status < 400:
                        self.results[path] = f"Request\n\n{payload}\nResponse\n\n{response.getheaders()}\n\n{response.data}"
                        
                        self.logger.log("-"*100)
                        self.logger.log(f"Success : {path}")
                        self.logger.log(
                            f"Response\n\n{response.getheaders()}\n\n{response.data}")

                    sleep(self.sleepingtime)
            except Exception as exp:
                print(f"[-] {path}", exp)

