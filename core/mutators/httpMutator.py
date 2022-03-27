from pprint import pprint
import random
from typing import Dict, List

from core.types import mutationTypes
from core.mutators.mutator import Mutator
from core.types.abnfToken import ABNFToken


class HttpMutator(Mutator):

    def __init__(self, nodes_to_mutate: Dict[str, str], root: ABNFToken, non_terminals: List[ABNFToken], min_count: int = 1, max_count: int = 3, random_seed: int = 32, verbose: bool = False) -> None:

        super().__init__(root, non_terminals, min_count, max_count, random_seed)

        # random.seed(random_seed)

        self.nodes_to_mutate = nodes_to_mutate
        self.mutations_count = random.randint(min_count, max_count)
        self.verbose = verbose

    def mutate(self) -> None:

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

        print("[+] Mutation Info")
        pprint(self.mutations_info)