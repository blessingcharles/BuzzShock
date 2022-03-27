import random
from typing import List
from core.types.abnfToken import ABNFToken
from core.shockers import basic

class Mutator:
    def __init__(self, root: ABNFToken, non_terminals: List[ABNFToken], min_count: int, max_count: int, random_seed: int, verbose: bool = False) -> None:
        self.root = root
        self.non_terminals = non_terminals
        self.min_count = min_count
        self.max_count = max_count
        self.random_seed = random_seed
        self.mutations_info = []
        self.verbose = verbose

    def charInsert(self, node: ABNFToken , pref_mutants : List[any] = None):
        
        pref_mutants = pref_mutants or basic.ASCII

        cur_val = node.children[0]
        val_len = len(cur_val)
        if not cur_val:
            return
        mutant_point = random.randint(0,val_len-1)
        shocker = random.choice(pref_mutants)

        node.children[0] = cur_val[:mutant_point] + shocker + cur_val[mutant_point:]

    def charDelete(self, node: ABNFToken):

        cur_val = node.children[0]
        val_len = len(cur_val)
        if not cur_val:
            return
        mutant_point = random.randint(0,val_len-1)

        node.children[0] = cur_val[:mutant_point] + cur_val[mutant_point+1:]

    def charReplace(self, node: ABNFToken  , pref_mutants : List[any] = None):

        pref_mutants = pref_mutants or basic.ASCII

        cur_val = node.children[0]
        val_len = len(cur_val)
        if not cur_val:
            return
        mutant_point = random.randint(0,val_len-1)
        shocker = random.choice(pref_mutants)

        node.children[0] = cur_val[:mutant_point] + cur_val[mutant_point+1:]

    def nodeInsert(self, node: ABNFToken):
        pass

    def nodeDelete(self, node: ABNFToken):
        pass

    def nodeReplace(self, node: ABNFToken):
        pass
