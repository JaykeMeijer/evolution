from typing import List

import random

from beast.interact import Action, Input, MoveForward, Turn
from beast.dna.dna import DNA


class Brain:
    dna: DNA
    def __init__(self, dna: DNA):
        self.dna = dna

    def step(self, inputs: List[Input]) -> List[Action]:
        actions: List[Action] = []

        if random.randint(0, 1) == 0:
            actions.append(MoveForward(random.randint(0, 5)))
        if random.randint(0, 2) == 0:
            actions.append(Turn(random.randint(-30, 30)))

        return actions
