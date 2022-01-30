import math
import random
from typing import List, Optional, Tuple, Union

import pygame

from evolution.beast.brain.brain import Brain
from evolution.beast.dna.dna import DNA
from evolution.beast.interact import Action, InputSet, MoveForward, Turn
from evolution.datastructures.quadtree import QuadTree
from evolution.simulation.render_helpers import draw_dashed_line
from evolution.util.math_helpers import get_direction
from evolution.world.world import Position, translate

DESPAWN_TIME = 50
beast_counter = 0


class Beast:
    id: int
    brain: Brain
    dna: DNA
    reproduction_cooldown: int = 0
    dead: int = 0

    position: Position

    def __init__(self, dna: DNA = None, position: Position = None, parents: Tuple["Beast", "Beast"] = None):
        global beast_counter
        self.id = beast_counter
        beast_counter += 1
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
        self.mate_detection_range: int = 100  # TODO: Make genetic
        self.speed: int = 5  # TODO: Make genetic

        self.selected: bool = False

        self.input_set: Optional[InputSet] = None
        self.nearest_mate: Optional[Beast] = None

    def __str__(self):
        return f"Beast {self.id} (dead status {self.dead})"

    def stats_string(self) -> str:
        return (
            f"Beast {self.id}\n"
            f"-----------------------\n"
            f"energy: {self.energy:.1f}\n"
            f"reproduction_cooldown: {self.reproduction_cooldown}\n"
            f"-----------------------\n"
            f"size: {self.size}\n"
            f"fertility: {self.fertility}\n"
            f"energy_consumption: {self.energy_consumption:.1f}\n"
            f"reproduction_cooldown: {self.base_reproduction_cooldown}\n"
            f"-----------------------\n"
            f"position: {self.position}\n"
            f"rotation: {self.rotation}\n"
            f"speed: {self.speed}\n"
            f"-----------------------\n"
            f"inputs: {self.input_set}\n"
        )

    def step(self, tree: QuadTree):
        if self.dead > 0:
            self.dead += 1
        else:
            self.energy -= self.energy_consumption / 10
            actions = self.brain.step(self._get_inputs(tree))
            for action in actions:
                self.energy -= self._apply_action(action)

            self.reproduction_cooldown = max(self.reproduction_cooldown - 1, 0)

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

    def _get_inputs(self, tree: QuadTree) -> InputSet:
        nearest_mate = self._find_nearest_mate(tree)
        self.nearest_mate = nearest_mate

        input_set = InputSet(
            distance_to_nearest_mate=(
                math.dist(self.position.tuple(), nearest_mate.position.tuple()) if nearest_mate else None
            ),
            direction_of_nearest_mate=(
                self._get_relative_direction(nearest_mate) if nearest_mate is not None else None
            ),
        )
        self.input_set = input_set
        return input_set

    def _get_relative_direction(self, mate: "Beast") -> int:
        relative_direction = get_direction(self.position.tuple(), mate.position.tuple()) - self.rotation
        if relative_direction > 180:
            relative_direction -= 360
        elif relative_direction < -180:
            relative_direction += 360
        return relative_direction

    def _find_nearest_mate(self, tree: QuadTree) -> Optional["Beast"]:
        nearby_mates = tree.points_in_range(self.position.tuple(), 100)
        if len(nearby_mates) <= 1:
            return None
        else:
            nearby_mates_sorted = [
                mate.obj
                for mate, _ in sorted(
                    [(mate, math.dist(self.position.tuple(), mate.coord())) for mate in nearby_mates],
                    key=lambda x: x[1],
                )
            ]
            return nearby_mates_sorted[1]

    def draw(self, screen: pygame.surface.Surface, render_nearest_mate: bool = False):
        if self.dead > 0:
            self._draw_dead(screen)
        else:
            self._draw_beast(screen)
            if render_nearest_mate:
                self._draw_to_nearest_mate(screen)


    def _draw_beast(self, screen: pygame.surface.Surface):

        tail_end = translate(self.position.tuple(), self.rotation - 180, 3 * self.size)
        pygame.draw.line(screen, (0, 0, 0), self.position.tuple(), tail_end, 3)
        if self.selected:
            pygame.draw.circle(screen, (255, 0, 0), self.position.tuple(), self.size + 3)
        else:
            pygame.draw.circle(screen, (0, 0, 0), self.position.tuple(), self.size + 1)
        pygame.draw.circle(screen, self.color, self.position.tuple(), self.size)

    def _draw_dead(self, screen: pygame.surface.Surface):
        c_val = int((255 / DESPAWN_TIME) * (self.dead - 1))
        color = (c_val, c_val, c_val)
        pygame.draw.line(screen, color, self.position.tuple(), translate(self.position.tuple(), 180, 10), 3)
        pygame.draw.line(
            screen, color, (self.position.x - 3, self.position.y + 3), (self.position.x + 3, self.position.y + 3), 3
        )

    def _draw_to_nearest_mate(self, screen: pygame.surface.Surface):
        if self.nearest_mate is not None:
            draw_dashed_line(screen, self.color, self.position.tuple(), self.nearest_mate.position.tuple(), 1)

    def reset_reproduction_cooldown(self):
        self.reproduction_cooldown = self.base_reproduction_cooldown

    def _apply_action(self, action: Action) -> float:
        if isinstance(action, MoveForward):
            self.position.move(self.rotation, self.speed)
            return self.energy_consumption / 5 * self.speed
        elif isinstance(action, Turn):
            self.rotation = (self.rotation + action.degrees) % 360
            return 0
        else:
            return 0
