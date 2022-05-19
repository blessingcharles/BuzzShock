from asyncio.log import logger
from distutils import log
from http.client import HTTPResponse
from io import BytesIO

import os
import glob
from pprint import pprint
from time import sleep
from typing import Dict
import urllib3
from core.engines.coreEngine import CoreEngine
from core.engines.shockerSocket import ShockerSocket
from utils.logger import Logger


class BytesIOSocket:
    def __init__(self, content):
        self.handle = BytesIO(content)

    def makefile(self, mode):
        return self.handle

    @classmethod
    def response_from_bytes(cls, data):
        sock = BytesIOSocket(data)

        response = HTTPResponse(sock)
        response.begin()

        return urllib3.HTTPResponse.from_httplib(response)


class HttpBuzzEngine(CoreEngine):
    def __init__(self, host: str, port: int, timeout: int = 5, buffsize: int = 8192,
                 reuse_socket: bool = False, is_ssl: bool = False, sleepingtime: int = 0.5,
                 log_file: str = None , verbose : bool = False) -> None:
        """
            Http text based protocol fuzz engine

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
            launch_from_db
                launch http payloads from the given path 
        """

        super().__init__(host=host, port=port, reuse_socket=reuse_socket, is_ssl=is_ssl,
                         timeout=timeout, buffsize=buffsize, sleepingtime=sleepingtime , log_file=log_file)

        self.verbose = verbose

    def launch_from_db(self, db_path: str = "db/http", testing_server_name: str = None) -> Dict[str, str]:

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
                    raw_response_obj = self.launchCustomPayload(payload_body=payload)
                    response = BytesIOSocket.response_from_bytes(
                        raw_response_obj)

                    
                    if response.status < 400:
                        self.results[path] = f"Request\n\n{payload}\nResponse\n\n{response.getheaders()}\n\n{response.data}"
                        if self.verbose:
                            self.logger.log("-"*100)
                            self.logger.log("Success : {path}")
                            self.logger.log(
                                f"Response\n\n{self.__extractHeaders(response.getheaders())}\n{response.data}")
                        elif self.logger:
                            self.logger.logTofile(f"mutationPath: {path}\n\n{payload}\nResponse\n\n{response.getheaders()}\n\n{response.data}")

                    sleep(self.sleepingtime)
            except Exception as exp:
                print(f"[-] {path}", exp)

    def __extractHeaders(self, headerDict):
        obj = {}
        for key, value in headerDict.items():
            obj[key] = value
        return obj
