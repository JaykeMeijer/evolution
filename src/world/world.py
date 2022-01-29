from dataclasses import dataclass
import math
import random
from typing import Tuple

from simulation.ui_constants import XSIZE, YSIZE
from util.math_helpers import translate

BORDER_BUFFER = 10
XLIMIT = XSIZE - BORDER_BUFFER
YLIMIT = YSIZE - BORDER_BUFFER


@dataclass
class Position:
    x: int = 0
    y: int = 0

    def move(self, direction: int, distance: int):
        new_x, new_y = translate(self.tuple(), direction, distance)
        self.x = max(min(new_x, XLIMIT), BORDER_BUFFER)
        self.y = max(min(new_y, YLIMIT), BORDER_BUFFER)

    def tuple(self) -> Tuple[int, int]:
        return (self.x, self.y)

    def copy(self) -> "Position":
        return Position(self.x, self.y)

    @staticmethod
    def random() -> "Position":
        return Position(random.randint(0, XSIZE), random.randint(0, YSIZE))


def distance(a: Position, b: Position) -> float:
    return math.dist(a.tuple(), b.tuple())
