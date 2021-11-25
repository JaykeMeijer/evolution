import random
from typing import List, Tuple, Optional

import pygame

from beast.brain.brain import Brain
from beast.dna.dna import DNA
from beast.interact import Action, Input, MoveForward, Turn
from world.world import Position, translate


DESPAWN_TIME = 50


class Beast:
    brain: Brain
    dna: DNA
    reproduction_cooldown: int = 0
    dead: int = 0

    position: Position

    def __init__(self, dna: DNA = None, position: Position = None, parents: Tuple["Beast", "Beast"] = None):
        self.dna = dna if dna else DNA()
        self.position = position if position else Position.random()

        self.parents: Optional[Tuple[Beast, Beast]] = parents
        self.children: List[Beast] = []

        self.rotation = random.randint(0, 360)

        self.brain: Brain = Brain(self.dna)

        self.energy: float = self.dna.get_gene("base_energy").get_value()
        self.size: int = self.dna.get_gene("size").get_value()
        self.energy_consumption: float = self.dna.get_gene("energy_consumption").get_value() * (self.size / 10)
        self.color: Tuple[int, int, int] = self.dna.get_gene("color").get_value()
        self.base_reproduction_cooldown: int = self.dna.get_gene("reproduction_cooldown").get_value()
        self.fertility: int = self.dna.get_gene("fertility").get_value()

    def _get_inputs(self) -> List[Input]:
        return []

    def step(self):
        if self.dead > 0:
            self.dead += 1
        else:
            actions = self.brain.step(self._get_inputs())
            for action in actions:
                self.energy -= self._apply_action(action)

            self.reproduction_cooldown = max(self.reproduction_cooldown - 1, 0)

    def stats_string(self) -> str:
        return (
            f"energy: {self.energy:.1f}\n"
            f"reproduction_cooldown: {self.reproduction_cooldown}\n"
            f"-----------------------\n"
            f"size: {self.size}\n"
            f"fertility: {self.fertility}\n"
            f"energy_consumption: {self.energy_consumption:.1f}\n"
            f"reproduction_cooldown: {self.base_reproduction_cooldown}\n"
        )

    def validate(self):
        if self.energy < 0 and not self.dead:
            self.dead = 1

    def despawnable(self) -> bool:
        return self.dead > DESPAWN_TIME

    def _can_reproduce(self):
        return not self.dead and self.reproduction_cooldown == 0

    def reproduce(self, other: "Beast") -> List["Beast"]:
        if self._can_reproduce() and random.randint(0, self.fertility * other.fertility) == 0:
            new_dna = self.dna.merge(other.dna)
            new_dna.mutate()
            new_beast = Beast(dna=new_dna, position=self.position.copy(), parents=(self, other))
            self.children.append(new_beast)
            other.children.append(new_beast)
            new_beast.reset_reproduction_cooldown()
            self.reset_reproduction_cooldown()
            other.reset_reproduction_cooldown()
            return [new_beast]

        return []

    def draw(self, screen: pygame.surface.Surface):
        if self.dead > 0:
            self._draw_dead(screen)
        else:
            self._draw_beast(screen)

    def _draw_beast(self, screen: pygame.surface.Surface):
        tail_end = translate(self.position.tuple(), self.rotation - 180, 3 * self.size)
        pygame.draw.line(screen, (0, 0, 0), self.position.tuple(), tail_end, 3)
        pygame.draw.circle(screen, (0, 0, 0), self.position.tuple(), self.size + 1)
        pygame.draw.circle(screen, self.color, self.position.tuple(), self.size)

    def _draw_dead(self, screen: pygame.surface.Surface):
        c_val = int((255 / DESPAWN_TIME) * (self.dead - 1))
        color = (c_val, c_val, c_val)
        pygame.draw.line(screen, color, self.position.tuple(), translate(self.position.tuple(), 180, 10), 3)
        pygame.draw.line(
            screen, color, (self.position.x - 3, self.position.y + 3), (self.position.x + 3, self.position.y + 3), 3
        )

    def reset_reproduction_cooldown(self):
        self.reproduction_cooldown = self.base_reproduction_cooldown

    def _apply_action(self, action: Action) -> float:
        if isinstance(action, MoveForward):
            self.position.move(self.rotation, action.distance)
            return self.energy_consumption / 5 * action.distance
        elif isinstance(action, Turn):
            self.rotation = (self.rotation + action.degrees) % 360
            return 0
        else:
            return 0
