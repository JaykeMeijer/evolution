import random
from dataclasses import dataclass
from typing import List, Optional, Tuple

import pygame

from evolution.beast.brain.brain import Brain
from evolution.beast.dna.dna import DNA
from evolution.beast.interact import Action, InputSet, MoveForward, Turn
from evolution.datastructures.kdtree import KDTree
from evolution.simulation.render_helpers import draw_dashed_line
from evolution.util.math_helpers import get_direction, rand_int_lower_range
from evolution.world.world import Position, translate

DESPAWN_TIME = 50
FIGHTING_COOLDOWN = 100
NOT_MOVED_LIMIT = 100
beast_counter = 0


class Beast:
    id: int
    brain: Brain
    dna: DNA
    reproduction_cooldown: int = 0
    fight_cooldown: int = 0
    dead: int = 0
    killed: bool = False
    not_moved: int = 0

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

        self.max_turning_rate: int = 90 - self.size * 9

        self.selected: bool = False

        self.input_set: Optional[InputSet] = None
        self.nearest_mate: Optional[Beast] = None

        font = pygame.font.SysFont("Calibri", 10)
        self.name = font.render(str(self.id), True, (0, 0, 0))
        self.name_offset = (self.name.get_width() / 2, self.name.get_height() / 2)
        self.stats = BeastStats()

    def _reset_energy(self):
        self.energy = self.dna.get_gene("base_energy").get_value()

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
            f"nearest_mate: {self.nearest_mate}\n"
            f"inputs: {self.input_set}\n"
            f"-----------------------\n"
            f"stats: {self.stats}"
        )

    def step(self, tree: KDTree):
        if self.dead > 0:
            self.dead += 1
        else:
            self.energy -= self.energy_consumption / 10
            actions = self.brain.step(self._get_inputs(tree))
            prev_pos = self.position.tuple()
            for action in actions:
                self.energy -= self._apply_action(action)

            # TODO temp until better solution found
            if self.position.tuple() == prev_pos:
                self.not_moved += 1
                if self.not_moved > NOT_MOVED_LIMIT:
                    self.dead = 1

            self.reproduction_cooldown = max(self.reproduction_cooldown - 1, 0)
            self.fight_cooldown = max(self.fight_cooldown - 1, 0)

    def validate(self):
        if self.energy < 0 and not self.dead:
            self.dead = 1

    def despawnable(self) -> bool:
        return self.dead > DESPAWN_TIME

    def reproduce(self, other: "Beast") -> List["Beast"]:
        if self._reproduction_succes(other):
            new_dna = self.dna.merge(other.dna)
            new_dna.mutate()
            new_beast = Beast(dna=new_dna, position=self.position.copy(), parents=(self, other))
            self.children.append(new_beast)
            other.children.append(new_beast)
            new_beast.reset_reproduction_cooldown()
            self.reset_reproduction_cooldown()
            other.reset_reproduction_cooldown()
            self.stats.children += 1
            return [new_beast]

        return []

    def _reproduction_succes(self, other: "Beast") -> bool:
        return (
            self._can_reproduce()
            and other._can_reproduce()
            and random.randint(0, self.fertility * other.fertility) == 0
        )

    def _can_reproduce(self) -> bool:
        return not self.dead and self.reproduction_cooldown == 0

    def fight(self, other: "Beast"):
        winner, loser = self._fight_result(other)
        if winner is not None and loser is not None:
            winner._reset_energy()
            loser.dead = 1
            loser.killed = True

    MAX_UPPERHAND_FACTOR = 13

    def _fight_result(self, other: "Beast") -> Tuple[Optional["Beast"], Optional["Beast"]]:
        if self._can_fight() and other._can_fight():
            self.stats.fights += 1

            self.fight_cooldown = FIGHTING_COOLDOWN
            other.fight_cooldown = FIGHTING_COOLDOWN

            upperhand_factor = (self.size - other.size) + ((self.energy - other.energy) / 500)
            fight_conclusion_chance = rand_int_lower_range(0, self.MAX_UPPERHAND_FACTOR, 2)
            if fight_conclusion_chance < abs(upperhand_factor):
                fight_win_chance = rand_int_lower_range(0, self.MAX_UPPERHAND_FACTOR, 2) * random.choice([-1, 1])
                if fight_win_chance < upperhand_factor:
                    self.stats.fights_won += 1
                    return self, other
                else:
                    return other, self
            else:
                self.energy -= self.energy_consumption * 20
                other.energy -= other.energy_consumption * 20
                return None, None
        else:
            return None, None

    def _can_fight(self) -> bool:
        return not self.dead and self.fight_cooldown == 0

    def _get_inputs(self, tree: KDTree) -> InputSet:
        nearest_point, distance = tree.find_nearest_neighbour(self.position.tuple(), self)
        nearest_mate = nearest_point.obj if nearest_point else None
        self.nearest_mate = nearest_mate
        input_set = InputSet(
            distance_to_nearest_mate=(distance if nearest_mate is not None else None),
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

    def draw(self, screen: pygame.surface.Surface, render_nearest_mate: bool = False, render_name: bool = True):
        if self.dead > 0:
            self._draw_dead(screen)
        else:
            self._draw_beast(screen)
            if render_nearest_mate:
                self._draw_to_nearest_mate(screen)
            if render_name:
                self._draw_name(screen)

    def _draw_beast(self, screen: pygame.surface.Surface):
        tail_end = translate(self.position.tuple(), self.rotation - 180, 3 * self.size)
        pygame.draw.line(screen, (0, 0, 0), self.position.tuple(), tail_end, 3)
        if self.selected:
            pygame.draw.circle(screen, (255, 0, 0), self.position.tuple(), self.size + 3)
        else:
            pygame.draw.circle(screen, (0, 0, 0), self.position.tuple(), self.size + 1)
        pygame.draw.circle(screen, self.color, self.position.tuple(), self.size)

    def _draw_name(self, screen: pygame.surface.Surface):
        screen.blit(self.name, (self.position.x - self.name_offset[0], self.position.y - self.name_offset[1]))

    def _draw_dead(self, screen: pygame.surface.Surface):
        c_val = int((255 / DESPAWN_TIME) * (self.dead - 1))
        color = (255, c_val, c_val) if self.killed else (c_val, c_val, c_val)
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
            turn_amount = max(-self.max_turning_rate, min(self.max_turning_rate, action.degrees))
            self.rotation = (self.rotation + turn_amount) % 360
            return 0
        else:
            return 0


@dataclass
class BeastStats:
    fights: int = 0
    fights_won: int = 0
    children: int = 0

    def __str__(self):
        return f"Fights: {self.fights} (won {self.fights_won})\n" f"Children: {self.children}"
