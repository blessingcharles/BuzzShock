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

    def nodeInsert(self,mutant_genes : ABNFToken):
        """
            Randomly Inserts a Non terminal node at random position
        """

        node_to_insert = random.choice(mutant_genes.children)

        index = random.randint(0 , len(mutant_genes.children)-1)
        mutant_genes.children.insert(index , node_to_insert)

        msg = f"Insert gene mutation :  inserting {node_to_insert.value} at index {index}"
        self.mutations_info.append(msg)

    def nodeDelete(self,mutant_genes : ABNFToken):
        """
            Randomly removes a non-terminal token
            eg : request-line : method SP request-target SP HTTP-version CRLF
                    After mutation
                    method SP SP HTTP-version CRLF
        """
        node_to_remove = random.choice(mutant_genes.children)
        
        msg = f"delete gene mutation :  deleting {node_to_remove.value}"
        self.mutations_info.append(msg)

        mutant_genes.children.remove(node_to_remove)

    def nodeReplace(self,mutant_genes : ABNFToken):

        node_to_replace = random.choice(mutant_genes.children)

        index = random.randint(0 , len(mutant_genes.children)-1)
        mutant_genes.children[index] = node_to_replace
        
        msg = f"Replace gene mutation :  Replacing {node_to_replace.value} at index {index}"
        self.mutations_info.append(msg)
