from random import random
from core.types.abnfToken import ABNFToken


class Mutator:
    def __init__(self, root: ABNFToken, min_count: int , max_count: int , random_seed: int , verbose : bool = False) -> None:
        self.root = root
        self.min_count = min_count
        self.max_count = max_count
        self.random_seed = random_seed
        self.mutations_info = []
        self.verbose = verbose

    def charInsert(self , node : ABNFToken):
        pass

    def charDelete(self , node : ABNFToken):
        pass

    def charReplace(self , node : ABNFToken):
        pass

    def nodeInsert(self , node : ABNFToken):
        pass

    def nodeDelete(self , node : ABNFToken):
        pass

    def nodeReplace(self, node :ABNFToken):
        pass