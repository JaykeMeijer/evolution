import random
from typing import List

import pygame

from beast.brain import Brain
from beast.dna.dna import DNA
from beast.interact import Action, MoveForward, Turn
from world.world import Position, move


class Beast:
    brain: Brain
    dna: DNA
    reproduction_cooldown: int = 0

    position: Position

    def __init__(self, dna: DNA = None, position: Position = None):
        if dna:
            self.dna = dna
        else:
            self.dna = DNA()

        if position:
            self.position = position
        else:
            self.position = Position.random()
        self.rotation = random.randint(0, 360)

        self.brain = Brain(self.dna)

        self.energy = 500 * self.dna.get_genome("base_energy").get_value()
        self.size = self.dna.get_genome("size").get_value()
        self.energy_consumption = self.dna.get_genome("energy_consumption").get_value() * (self.size / 10)
        self.color = self.dna.get_genome("color").get_value()

        # TODO: Make genetic
        self.base_reproduction_cooldown = 100

    def step(self):
        actions = self.brain.step([])
        for action in actions:
            self.energy -= self._apply_action(action)

        self.reproduction_cooldown = max(self.reproduction_cooldown - 1, 0)

    def validate(self) -> bool:
        if self.energy < 0:
            return False
        return True

    def reproduce(self, other: "Beast") -> List["Beast"]:
        # TODO: Use fitness for match up
        if self.reproduction_cooldown == 0 and random.randint(0, 100) == 0:
            new_dna = self.dna.merge(other.dna)
            new_dna.mutate()
            new_beast = Beast(dna=new_dna, position=self.position.copy())
            new_beast.reset_reproduction_cooldown()
            self.reset_reproduction_cooldown()
            other.reset_reproduction_cooldown()
            return [new_beast]

        return []

    def draw(self, screen: pygame.surface.Surface):
        pygame.draw.circle(screen, self.color, (self.position.x, self.position.y), self.size)

    def reset_reproduction_cooldown(self):
        self.reproduction_cooldown = self.base_reproduction_cooldown

    def _apply_action(self, action: Action) -> float:
        if isinstance(action, MoveForward):
            move(self.position, self.rotation, action.distance)
            return self.energy_consumption / 5 * action.distance
        elif isinstance(action, Turn):
            self.rotation = (self.rotation + action.degrees) % 360
            return 0
        else:
            return 0
