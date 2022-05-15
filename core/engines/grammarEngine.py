
from concurrent.futures import ThreadPoolExecutor
import copy
from config import CONFIG
from core.engines.coreEngine import CoreEngine
from core.mutators.httpMutator import HttpMutator
from core.parsers.abnfParsers import ABNFParser


class GrammarEngine(CoreEngine):
    def __init__(self, host: str, port: int, grammar_file: str, mutants_count: int, timeout: int = 5, buffsize: int = 8192,
                 reuse_socket: bool = False, is_ssl: bool = False, sleepingtime: int = 0.5, threads : int = 8 ,
                 log_file: str = None, verbose: bool = False) -> None:
        """


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
            run
                run the engine
        """

        super().__init__(host=host, port=port, reuse_socket=reuse_socket, is_ssl=is_ssl,
                         timeout=timeout, buffsize=buffsize, sleepingtime=sleepingtime, log_file=log_file)

        self.grammar_file = grammar_file
        self.mutants_count = mutants_count
        self.threads = threads
        self.verbose = verbose

    def run(self) -> None:
        p = ABNFParser(self.grammar_file)
        p.parse()

        if "nodes-to-mutate" not in CONFIG:
            raise KeyError(
                "Terminal Nodes should be mentioned in the config for mutation")

        nodes_to_mutate = CONFIG["nodes-to-mutate"]
        url_token = p.getChildren("__URL__")[0]

        with ThreadPoolExecutor(max_workers=self.threads) as exec:
            for _ in range(self.mutants_count):
                root_node = copy.deepcopy(p.root)

                m = HttpMutator(url_token.value, nodes_to_mutate,
                                root_node, verbose=self.verbose)
                m.mutate()
                print("-----------------After Mutations ---------------------")
                m.zoombieToRequest()
                print(m.request)
                # exec.submit(self.__launch , m.request)

    def __launch(self , request : str) -> None:
        resp = self.launchCustomPayload(request)
        print(resp)


