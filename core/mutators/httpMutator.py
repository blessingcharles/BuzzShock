from pprint import pprint
import random
from typing import Dict, List
from urllib.parse import urlparse, ParseResult

from parso import parse

from core.types import mutationTypes
from core.mutators.mutator import Mutator
from core.types.abnfToken import ABNFToken
from core.types.httpBuzzTokens import CustomTokens, standarBody
from utils.logger import Bzlogger


class HttpMutator(Mutator):

    def __init__(self, url: str, nodes_to_mutate: Dict[str, str], root: ABNFToken, min_count: int = 1, max_count: int = 3, random_seed: int = 132, verbose: bool = False) -> None:

        super().__init__(root, min_count, max_count, random_seed , verbose=verbose)

        # random.seed(random_seed)
        self.url = url
        self.request = b""
        self.nodes_to_mutate = nodes_to_mutate
        self.mutations_count = random.randint(min_count, max_count)
        self.non_terminals = []

    def __get_nonterminals(self , node : ABNFToken ) -> None:
        # get all the non terminals to mutate
        if node.isTerminal:
            return
        self.non_terminals.append(node)
        for child in node.children:
            self.__get_nonterminals(child)

    def mutate(self) -> None:

        self.__get_nonterminals(self.root)
        while self.mutations_count:

            self.mutations_count -= 1

            possible_nodes = [
                node for node in self.non_terminals if node.value in self.nodes_to_mutate]
            if not possible_nodes:
                return
            zoombie_node = random.choice(possible_nodes)

            if self.nodes_to_mutate[zoombie_node.value] not in mutationTypes.types:
                raise(
                    f"Unrecognizable mutation type {self.nodes_to_mutate[zoombie_node.value]} for node {zoombie_node.value}")

            if self.nodes_to_mutate[zoombie_node.value] == mutationTypes.types[0]:
                # point mutation
                point_mutation_variant = random.choice(
                    mutationTypes.pointMutations)

                # randomly select a expansion value for the zoombie node
                zoombie_node.children = [random.choice(zoombie_node.children)]

                # make the node a mutant
                self.__getattribute__(point_mutation_variant)(zoombie_node)

            elif self.nodes_to_mutate[zoombie_node.value] == mutationTypes.types[1]:
                # genetic mutation
                genetic_mutation_variant = random.choice(
                    mutationTypes.geneticMutations)
                self.__getattribute__(genetic_mutation_variant)(zoombie_node)

        if self.verbose:
            Bzlogger.success("Mutation Info")
            for info in self.mutations_info:
                Bzlogger.info(info)

    def zoombieToRequest(self):

        # If a non terminal node expand only to multiple terminal node choose only one terminal
        self.__manipulateTerminal(self.root)
        # expand the mutant tree
        self.__traverseZoombieGene(self.root)

        # to interpret unicode sequence like \n\r
        self.request = self.request.decode()

        host, port, netloc, uri = self.urlParser(self.url)
        self.__replace_symbols(host, uri)

    def __replace_symbols(self, host: str, uri: str):
        """
            Replace the special symbols in the request object
        """

        buzz_id = f"buzzseed-{self.random_seed}"
        self.request = self.request.replace(
            CustomTokens.__BUZZ_ID__, buzz_id
        ).replace(
            CustomTokens.__REQUEST_TARGET__, uri
        ).replace(
            CustomTokens.__HOST__, host
        )

        # if __RANDOM_TEXT__ presents shock the request with random with CL
        if CustomTokens.__RANDOM_TEXT__ in self.request:
            # TODO : random-text with content-length header
            pass

        if CustomTokens.__STANDARD_BODY__ in self.request:
            cl_body = standarBody['cl-body']
            self.request = self.request.replace(
                CustomTokens.__STANDARD_BODY__, cl_body["value"]
            )
            self.__insertCustomHeaders(cl_body["headers"])

    def __insertCustomHeaders(self, header_val: str):
        self.request = self.request.replace(
            CustomTokens.__HEADERS_CRLF__, "\r\n" +
            header_val + CustomTokens.__HEADERS_CRLF__
        )

    def __manipulateTerminal(self, cur_node: ABNFToken):
        """
            Choose a single terminal from a pool of terminals for a non terminal
        """
        if cur_node.isTerminal:
            return

        # check whether this node only contains terminals
        have_non_terminal_children = False

        for children in cur_node.children:
            if not children.isTerminal:
                have_non_terminal_children = True

        if have_non_terminal_children:
            # make it go deep
            for children in cur_node.children:
                self.__manipulateTerminal(children)
        else:
            # choose a random child from the pool
            cur_node.children = [random.choice(cur_node.children)]

    def __traverseZoombieGene(self, cur_node: ABNFToken):
        if cur_node.isTerminal:
            self.request += cur_node.value.encode('utf-8')
        else:
            for children_node in cur_node.children:
                self.__traverseZoombieGene(children_node)

    def urlParser(self, url):

        parser_obj: ParseResult = urlparse(url)
        netloc = parser_obj.netloc
        scheme = parser_obj.scheme
        uri = '/'.join(url.split('/')[3:])

        if ':' not in netloc:
            if scheme == "https":
                port = 443
                host = netloc
            else:
                port = 80
                host = netloc
        else:
            host, port = netloc.split(':')

        return host, port, netloc, uri
