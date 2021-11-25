from typing import List, cast

import random

from beast.brain.neuron import Connection
from beast.dna.dna import DNA
from beast.dna.gene import NeuronConnectionGene
from beast.interact import Action, Input, MoveForward, Turn


class Brain:
    dna: DNA
    def __init__(self, dna: DNA):
        self.dna = dna
        self.neuron_connections: List[Connection] = [
            Connection(cast(NeuronConnectionGene, self.dna.get_gene("neuron_connection_1"))),
            Connection(cast(NeuronConnectionGene, self.dna.get_gene("neuron_connection_2"))),
        ]

    def step(self, inputs: List[Input]) -> List[Action]:
        actions: List[Action] = []

        if random.randint(0, 1) == 0:
            actions.append(MoveForward(random.randint(0, 5)))
        if random.randint(0, 2) == 0:
            actions.append(Turn(random.randint(-30, 30)))

        return actions
