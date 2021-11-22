from typing import List

import random

from beast.interact import Action, Input, Move
from beast.dna.dna import DNA


class Brain:
    dna: DNA

    def __init__(self, dna: DNA):
        self.dna = dna

    def step(self, inputs: List[Input]) -> List[Action]:
        # TODO: For some reason, children make the same moves as their parent?!
        return [Move(random.randint(-5, 5), random.randint(-5, 5))]
