import random

from core.mutators.mutator import Mutator
from core.types.abnfToken import ABNFToken

class HttpMutator(Mutator):

    def __init__(self, root: ABNFToken, min_count: int = 0, max_count: int = 0, random_seed: int = 123 , verbose : bool = False) -> None:
        Mutator.__init__(root, min_count, max_count, random_seed)
        random.seed(random_seed)
        self.mutations_count = random.randint(min_count , max_count)
        self.verbose = verbose
        
    def mutate(self) -> None:
        pass
