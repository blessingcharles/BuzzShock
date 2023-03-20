from concurrent.futures import ThreadPoolExecutor
from datetime import datetime
from core.engines.coreEngine import CoreEngine
from utils.logger import Bzlogger
from utils.utils import userinput_continuation
from .plugins.ClassicsPlugin import ClassicsPlugin
from .plugins.HttpLaxClPlugin import HttpLaxClPlugin
from .plugins.HttpLaxTePlugin import HttpLaxTePlugin

from core.engines.HttpBuzzEngine import BytesIOSocket
from .engines import discovered_plugins


class HeuristicEngine(CoreEngine):
    def __init__(self, protocol: str, host: str, port: int, output_dir: str, threads: int, endpoint: str = "",
                 verbose: bool = False, timeout: int = 5, buffsize: int = 8192, reuse_socket: bool = False, is_ssl: bool = False,
                 sleepingtime: int = 0.1, log_file: str = None, no_csv: bool = False, max_retry: int = 2) -> None:
        """
            Attributes
            -------------
            protocol : str
            host : str
            port : int
            output_dir : str
            threads : int
            endpoint : str
            verbose : bool
            timeout : int
            buffsize : int
            reuse_socket : bool
            sleepingtime : int
            log_file : str

            Methods
            ----------
            run:
                run heuristics test on websites based on the arguments passed

        """
        super().__init__(host, port, timeout, buffsize,
                         reuse_socket, is_ssl, sleepingtime, log_file)

        self.protocol = protocol
        self.endpoint = endpoint
        self.threads = threads
        self.difftime = timeout
        self.max_retry = max_retry
        self.curr_retry = 0

        self.no_csv = no_csv
        self.output_dir = output_dir
        self.verbose = verbose
        self.normal_req = ""

    def run(self):
        Bzlogger.success("Started heuristic tester")
        pl = ClassicsPlugin(self.endpoint, verbose=self.verbose)
        mutants = pl.generate()
        self.normal_req = mutants["normal-req"]
        self.__timebased(mutants)

        # Trying for Obfuscated Transfer Encoding
        Bzlogger.success(" ---- "*10)
        Bzlogger.info("Trying Obfuscating TE\n")
        LaxTe_CLTE = HttpLaxTePlugin(endpoint=self.endpoint, verbose=self.verbose,
                                     heuruster_body="1\r\nA\r\n0\r\n\r\n", heuruster_headers={"Content-Length": "4"})

        mutants = LaxTe_CLTE.generate()
        self.__timebased(mutants)

        LaxTe_TECL = HttpLaxTePlugin(endpoint=self.endpoint, verbose=self.verbose,
                                     heuruster_body="0\r\n\r\nX", heuruster_headers={"Content-Length": "6"})
        mutants = LaxTe_TECL.generate()
        self.__timebased(mutants)

        # Trying for Obfuscated Content Length
        Bzlogger.success(" ---- "*10)
        Bzlogger.info("Trying Obfuscating CL\n")

        LaxCl_CLTE = HttpLaxClPlugin(endpoint=self.endpoint, verbose=self.verbose,
                                     heuruster_body="1\r\nA\r\n0\r\n\r\n", cl_value=4)

        mutants = LaxCl_CLTE.generate()
        self.__timebased(mutants)

        LaxCl_TECL = HttpLaxClPlugin(endpoint=self.endpoint, verbose=self.verbose,
                                     heuruster_body="0\r\n\r\nX", cl_value=4)
        mutants = LaxCl_TECL.generate()
        self.__timebased(mutants)

    def __timebased(self, mutants):

        for name, payload in mutants.items():
            if self.__heuruster(payload, name=name):
                userinput_continuation(
                    "Do you want to test on more cases?[Y/n]")

    def __heuruster(self, payload, name):
        res = self.__sendMutant(payload)
        Bzlogger.info(f"[{name}] diff time : {res[1]}")
        if self.verbose:
            Bzlogger.warning(payload)

        if res[0] == "Issue":
            # try with normal req
            res = self.__sendMutant(self.normal_req)
            if res[0] == "Issue" or res[0] == "Disconnected":
                self.curr_retry += 1
                # normal req also having an issue , try for more attempts
                if self.curr_retry < self.max_retry:
                    return self.__heuruster(payload, name)
            else:
                # confirmed HRS
                Bzlogger.success("Potential vector found")
                Bzlogger.success(
                    f"{name} Vulnerability confirmed based on timing attacks")
                Bzlogger.info(payload)

                return True
        elif res[0] == "Disconnected":
            if self.curr_retry < self.max_retry:
                # try for few more attempts
                self.curr_retry += 1
                return self.__heuruster(payload, name)
            else:
                Bzlogger.failed("Socket got disconnected")
        self.curr_retry = 0
        return False

    def __sendMutant(self, payload):
        # print(payload)
        start_time = datetime.now()
        result = self.launchCustomPayload(payload)
        end_time = datetime.now()
        diff = (end_time - start_time).seconds

        # Bzlogger.info("Time Diff : ", diff.seconds)
        # Bzlogger.info(result)
        if len(result) > 0:
            resp = BytesIOSocket.response_from_bytes(result)
        else:
            # disconnected within the expected time
            if diff < (self.difftime-1):
                return ("Disconnected", diff)
            elif diff > (self.difftime-1):  # timeout maybe hrs ?
                return ("Issue", diff)

        return (resp, diff)
