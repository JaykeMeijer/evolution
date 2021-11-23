from dataclasses import dataclass
import math
import random
from typing import Tuple


XSIZE = 1000
YSIZE = 1000


@dataclass
class Position:
    x: int = 0
    y: int = 0

    def move(self, x: int, y: int):
        new_x = self.x + x
        new_y = self.y + y
        if 0 < new_x < XSIZE:
            self.x = new_x
        if 0 < new_y < YSIZE:
            self.y = new_y

    def tuple(self) -> Tuple[int, int]:
        return (self.x, self.y)

    def copy(self) -> "Position":
        return Position(self.x, self.y)

    @staticmethod
    def random() -> "Position":
        return Position(random.randint(0, XSIZE), random.randint(0, YSIZE))


def distance(a: Position, b: Position) -> float:
    return math.dist(a.tuple(), b.tuple())


def move(start: Position, direction: int, distance: int):
    start.x = round(start.x + math.cos(math.radians(direction)) * distance)
    start.y = round(start.y + math.sin(math.radians(direction)) * distance)
