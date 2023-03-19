from concurrent.futures import ThreadPoolExecutor
from datetime import datetime
from core.engines.coreEngine import CoreEngine
from utils.logger import Bzlogger
from plugins.ClassicsPlugin import ClassicsPlugin
from core.engines.HttpBuzzEngine import BytesIOSocket

class HeuristicEngine(CoreEngine):
    def __init__(self, protocol: str, host: str, port: int, output_dir: str, threads: int, endpoint: str = "",
                 verbose: bool = False, timeout: int = 5, buffsize: int = 8192, reuse_socket: bool = False, is_ssl: bool = False,
                 sleepingtime: int = 0.1, log_file: str = None , no_csv : bool = False , difftime: int = 5 , max_retry : int =2) -> None:
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
        self.difftime = difftime
        self.max_retry = max_retry
        self.curr_retry = 0

        self.no_csv = no_csv
        self.output_dir = output_dir
        self.verbose = verbose

    def run(self):
        Bzlogger.success("Started heuristic tester")
        pl = ClassicsPlugin(self.endpoint , verbose=self.verbose)
        mutants = pl.generate()
        self.__timebased(mutants)
    
    def __timebased(self , mutants):
        Bzlogger.info("Timing Based Inferential")

        # CL TE
        if self.__heuruster(mutants , "classics-clte"):
            exit(0)
        # TE CL
        if self.__heuruster(mutants , "classics-tecl"):
            exit(0)

    def __heuruster(self ,mutants , name):
        res = self.__sendMutant(mutants[name])

        if res == "Issue":
            # try with normal req
            res = self.__sendMutant(mutants["normal-req"])
            if res == "Issue" or res == "Disconnected":
                self.curr_retry += 1
                # normal req also having an issue , try for more attempts
                if self.curr_retry < self.max_retry:
                    return self.__heuruster(mutants)
            else:
                # confirmed HRS
                Bzlogger.success("Potential vector found")
                Bzlogger.success(f"{name} Vulnerability confirmed based on timing attacks")
                if self.verbose:
                    Bzlogger.info(mutants["name"])

                return True
        
        self.curr_retry = 0
        return False
    
    def __sendMutant(self , payload):
        start_time = datetime.now()
        result = self.launchCustomPayload(payload)
        end_time = datetime.now()
        diff = end_time - start_time

        if result is not None:
            resp = BytesIOSocket.response_from_bytes(result)
        else:
            if diff < self.difftime: # disconnected within the expected time
                return "Disconnected"
            elif diff > self.difftime: # timeout maybe hrs ?
                return "Issue"

        return resp    
        