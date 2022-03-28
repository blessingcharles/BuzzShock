
from collections import deque
from pprint import pprint
from core.parsers.abnfTokenizer import Tokenizer
from core.types.abnfToken import ABNFToken, ABNFTokenDict, ABNFTokenType


class ABNFParser:
    def __init__(self, source_file: str) -> None:
        """ 
            Args:
                source_file: file path to the ABNF grammar
            Return:
                ABNF parser object
        """
        self.src = source_file
        self.abnf_obj: ABNFTokenDict = {}
        self.tokens_count = 0
        self.root: ABNFToken = None
        self.terminal_nodes = []
        self.nonterminal_nodes = []
        self.shocking_nodes = []

    def parse(self):
        """
            Parse the given ABNF grammar file into python grammar object

            Args:
                None
            Return:
                None
        """
        tt = Tokenizer(self.src)
        tt.tokenize()
        self.tokens_count = len(tt.abnf_tokens)

        for idx in tt.field_seperators_idx:
            cur_key = tt.abnf_tokens[idx-1]
            self.abnf_obj[cur_key] = []

            token_vals_idx = idx+1
            """
                Untill next key occur collect all the token and map it to the key
            """
            while token_vals_idx+1 < self.tokens_count and tt.abnf_tokens[token_vals_idx+1].value not in ABNFToken.DELIMETER:
                self.abnf_obj[cur_key].append(tt.abnf_tokens[token_vals_idx])
                token_vals_idx += 1

            if token_vals_idx+1 == self.tokens_count:
                # last token
                self.abnf_obj[cur_key].append(tt.abnf_tokens[token_vals_idx])

        # Build an AST tree with the abnf object

        self.root = ABNFToken(ABNFTokenType.NON_TERMINAL, "start")
        deq = deque()
        self.nonterminal_nodes.append(self.root)

        deq.append(self.root)
        while deq:
            cur_node = deq.pop()
            # explore its expansion nodes and add it to the deque
            for expansion_node in self.abnf_obj[cur_node]:

                cur_node.children.append(expansion_node)

                # if self.__is_already_visited(expansion_node):
                #     continue

                if expansion_node.isTerminal:
                    self.terminal_nodes.append(expansion_node)
                elif expansion_node.type is ABNFTokenType.NON_TERMINAL:
                    deq.append(expansion_node)
                    self.nonterminal_nodes.append(expansion_node)
                elif expansion_node.type is ABNFTokenType.BUZZSHOCK:
                    # append its parent node
                    self.shocking_nodes.append(cur_node)

    def getChildren(self , nodeVal : str):
        
        for node in self.abnf_obj:
            if node.value == nodeVal:
                return self.abnf_obj[node]

        return None

    def __is_already_visited(self, node: ABNFToken):
        return node in self.terminal_nodes or node in self.nonterminal_nodes or node in self.shocking_nodes

    def printTree(self, rootNode):

        d = deque()
        d.append(rootNode)

        alread_visited = []
        alread_visited.append(rootNode)

        while d:
            cur_node = d.pop()
            print("[+] Exploring -------> ", cur_node)

            for neigh_node in cur_node.children:
                # if neigh_node not in alread_visited:
                    print(neigh_node)
                    alread_visited.append(neigh_node)
                    d.append(neigh_node)
            print("-------------------------------")
