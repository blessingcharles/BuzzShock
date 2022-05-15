import random
from typing import List
from core.types.abnfToken import ABNFToken
from core.shockers import basic

class Mutator:
    def __init__(self, root: ABNFToken, min_count: int, max_count: int, random_seed: int, verbose: bool = False) -> None:
        self.root = root
        self.min_count = min_count
        self.max_count = max_count
        self.random_seed = random_seed
        self.mutations_info = []
        self.verbose = verbose

    def charInsert(self, node: ABNFToken , pref_mutants : List[any] = None):

        pref_mutants = pref_mutants or basic.ASCII

        cur_val = node.children[0].value
        val_len = len(cur_val)
        if not cur_val:
            return
        mutant_point = random.randint(0,val_len-1)
        shocker = random.choice(pref_mutants)
        node.children[0].value = cur_val[:mutant_point] + shocker + cur_val[mutant_point:]
        msg = f"insert point mutation :  mutating {cur_val} to {node.children[0].value}"
        self.mutations_info.append(msg)

    def charDelete(self, node: ABNFToken):

        cur_val = node.children[0].value
        val_len = len(cur_val)
        if not cur_val:
            return
        mutant_point = random.randint(0,val_len-1)

        node.children[0].value = cur_val[:mutant_point] + cur_val[mutant_point+1:]
        msg = f"delete point mutation :  mutating {cur_val} to {node.children[0].value}"
        self.mutations_info.append(msg)

    def charReplace(self, node: ABNFToken  , pref_mutants : List[any] = None):

        pref_mutants = pref_mutants or basic.ASCII

        cur_val = node.children[0].value
        val_len = len(cur_val)
        if not cur_val:
            return
        mutant_point = random.randint(0,val_len-1)
        shocker = random.choice(pref_mutants)

        node.children[0].value = cur_val[:mutant_point] + cur_val[mutant_point+1:]
        msg = f"delete point mutation :  mutating {cur_val} to {node.children[0].value}"
        self.mutations_info.append(msg)

    def nodeInsert(self, node: ABNFToken , mutant_genes : List[str]):
        pass

    def nodeDelete(self, node: ABNFToken ,  mutant_genes : List[str] ):
        pass

    def nodeReplace(self, node: ABNFToken ,  mutant_genes : List[str]):
        pass
