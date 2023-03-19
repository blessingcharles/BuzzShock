from core.engines.coreEngine import CoreEngine
from utils.logger import Bzlogger

class HeuristicEngine(CoreEngine):
    def __init__(self, protocol: str, host: str, port: int, output_dir: str, threads: int, endpoint: str = "",
                 verbose: bool = False, timeout: int = 5, buffsize: int = 8192, reuse_socket: bool = False, is_ssl: bool = False,
                 sleepingtime: int = 0.1, log_file: str = None , no_csv : bool = False) -> None:
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

        self.no_csv = no_csv
        self.output_dir = output_dir
        self.verbose = verbose

    def run(self):
       Bzlogger.success("Starting heuristic tester")