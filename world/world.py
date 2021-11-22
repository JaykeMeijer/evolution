from dataclasses import dataclass

import random


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

    @staticmethod
    def random() -> "Position":
        return Position(random.randint(0, XSIZE), random.randint(0, YSIZE))


def distance(a: Position, b: Position) -> float:
    return ((((a.x - b.x)**2) + ((a.y-b.y)**2))**0.5)
