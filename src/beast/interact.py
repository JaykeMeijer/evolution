from dataclasses import dataclass
from typing import Optional


class Action:
    pass


@dataclass
class InputSet:
    distance_to_nearest_mate: Optional[float]
    direction_of_nearest_mate: Optional[float]

    def all_none(self):
        return all([val is None for val in vars(self).values()])


class Noop(Action):
    pass


class MoveForward(Action):
    pass


class Turn(Action):
    degrees: int

    def __init__(self, degrees: int):
        self.degrees = degrees
